# Explanation
1. app.py: Defines a Flask app with a /healthcheck endpoint that returns the application version, description, and last commit SHA in JSON format.
2. Dockerfile: Sets up a Docker image for the Flask app, including dependencies and a command to run it.
3. ci.yml: Automates the process of:
* Checking out the repository code.
* Setting up Python and installing dependencies.
* Running tests (currently, there are none).
* Building the Docker image.
* Optionally pushing the Docker image to DockerHub (replace credentials with your own via GitHub secrets).

4. How to Run:
Build the Docker image locally:

bash

docker build -t my-flask-app .

Run the container:

bash

docker run -p 5000:5000 my-flask-app

You can access the healthcheck endpoint at http://localhost:5000/healthcheck.
Example Response:

json

    {
    "myapplication": [
        {
        "version": "1.0",
        "description": "PI technical example",
        "lastcommitsha": "abc57858585"
        }
    ]
    }

With this setup, the application is containerized and a CI pipeline is ready to automatically test and build the Docker image on every push or pull request to the main branch.

## Key Points in CI/CD Pipeline:

* Unit Testing: Runs tests using pytest before building the Docker image.
* Code Quality Check: Runs flake8 to ensure PEP8 compliance.
* Docker Build: Builds the Docker image with Git metadata injected using --build-arg.
* Image Push: Pushes the Docker image to DockerHub (credentials stored in GitHub secrets).


Using Alpine Linux as a base image for Docker containers can be very beneficial due to its small size (5Mb),but there are some potential issues and challenges you may face. Below are the key pros and cons of using Alpine images:

Pros'
1. very small size - 5Mb 
    compared to Debian/Ubuntu - 100Mb+
    this has the added advantage of fast downloads and deployments
2. Small attack area
   In general, because of this,  it tends to be more secure
3. Pulling it from different repo's (Docker hub, GCR, ECR) is very fast
4. minimal packages installed, results in less conflicts and changes

Cons
1. Internal Library
    Alpine uses musl Libc and busybox (with symbolic links), this often leads to compatibility issues
2. Technical library for python (NumPy, Pandas, TensorFlow) requires lots of work arounds, resulting addional libraries thereby increasing the base image size
3. being a minimal image it does not have many development tools so results in much longer build times
4. numerical ops tend to be much slower
5. great care needs to be taken if you are developing under different Linux distrubutions if you are later deploying to Alpine
6.  there are a lack of pre-built libraries
7. Be very care tied you version to the latest. At the current time Alpine is going under a lot of changes and this is resulting lots of failures and compability issues, resulting in some cases reviewing the builds weekly

If you are doing lots of python, or building apps requiring  alots of different functionalilty you may wish to consider looking at Debian slim. It relies on Glibc and you can leverage its own repository

### Local testing
As this example is basically a simple web app with single end point, without parameters you can use curl to validate that it is working

1. fire up the container


    docker run -rm -it -p 5000:5000 my-flask-app

2. hit the end point with a http get

    curl http://localhost:5000/healthcheck

and it should return something similar to 
    {
    "myapplication": [
                {
                    "version": APP_VERSION,
                    "description": DESCRIPTION,
                    "lastcommitsha": LAST_COMMIT_SHA
                }
            ]
    }

    where the Uppercase words are what were passed in.

    In addition to this, you should also test that the http return code is 200

    e.g. curl -I http://localhost:5000/healthcheck 
    this will print the headers and the first line should be

    HTTP/1.1 200 OK


Key Steps:

* **AWS Credentials**: Store AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION) in GitHub secrets.
* **AWS Elastic Beanstalk**: We’ll use the Elastic Beanstalk CLI to deploy the application.

GitHub Secrets Setup

* Go to your GitHub repository → Settings → Secrets and add the following secrets:
    * AWS_ACCESS_KEY_ID
    * AWS_SECRET_ACCESS_KEY
    * AWS_REGION
    * EB_APP_NAME: Your Elastic Beanstalk application name
    * EB_ENV_NAME: Your Elastic Beanstalk environment name

#### Update CI Pipeline for AWS Deployment

Add an additional deployment step to the CI pipeline (.github/workflows/ci.yml) for AWS Elastic Beanstalk: - see extras/.github/workflows/ci.yml


### Deployment to GCP (Google Cloud Run)

To deploy to Google Cloud Run, (or  GKE) the CI/CD pipeline can be adjusted to build and deploy using gcloud:
Prerequisites:

* Google Cloud Project: Create a project in GCP.
* Container Registry: Enable Container Registry and Cloud Run in GCP.
* GitHub Secrets: Store GCP_PROJECT_ID, GCP_SERVICE_KEY (as JSON), and GCP_REGION in GitHub secrets.

#### CI Pipeline for GCP Deployment

To deploy an application to Google Cloud Platform (GCP), particularly to a service you have to common approaches Google Cloud Run or Google Kubernetes Engine (GKE),

Google Cloud Run,  is a fully managed platform for containerized applications.


Here's a step-by-step guide to deploying a Python web application (suing a Flask app) to Google Cloud Run on GCP, covering prerequisites, creating a container, pushing to GCP, and automating the process using GitHub Actions.

1. Prerequisites
#### Create a GCP Project:

    1. Sign up / Login: Go to the Google Cloud Console.
    2. Create a Project:
        In the console, create a new project.
        Give your project a name and note the Project ID (you'll need this later).

#### Enable Required APIs:

    1. Enable Cloud Run, Cloud Build, and Container Registry APIs.
        * In the Google Cloud Console, navigate to the APIs & Services > Library, and enable the following APIs:
            * Cloud Run API
            * Cloud Build API
            * Container Registry API

#### Install Google Cloud SDK:

    Install the Google Cloud SDK, which includes the gcloud CLI, to interact with GCP from your local machine.

Authentication and Setup:

1. Authenticate: After installing the SDK, authenticate using:

bash

    gcloud auth login

Set your GCP project:

bash

    gcloud config set project <your-project-id>

Optional: Create a Google Cloud Service Account Key:

If using GitHub Actions for deployment, you'll need to create a Service Account Key:

1. Navigate to IAM & Admin > Service Accounts in the Google Cloud Console.
2. Create a new service account and give it the Cloud Run Admin and Viewer roles.
3. Create a JSON key for the service account and download it. You’ll use this in your GitHub Actions pipeline.

2. Dockerize the Application

Your Python web app (e.g., Flask) needs to be containerized using Docker before it can be deployed to Cloud Run.
Sample Dockerfile (Alpine-Based): extrasgcp/Dockerfile

3. Push the Docker Image to Google Container Registry (GCR)

Cloud Run works by deploying container images stored in Google Container Registry (GCR).
Build and Push the Docker Image:

1. Tag the image:

    docker build -t gcr.io/<your-project-id>/flask-app .
2. Push the image to GCR: (This is similar to images on dockerhub)

    docker push gcr.io/<your-project-id>/flask-app

This will push the Docker image to the Google Container Registry (GCR), which Cloud Run will use.

4. Deploy the Container Image to Google Cloud Run

With the image stored in GCR, you can now deploy it to Google Cloud Run.
Command to Deploy: (deploy.sh)

    --platform managed: This option tells GCP to use the fully managed Cloud Run platform.
    --allow-unauthenticated: Allows the service to be publicly accessible.

Key Steps:

    Service Name: The service will be named flask-app (or whatever you choose).
    Region: Replace <your-region> with the desired GCP region (e.g., europe-west2-a).

you can either hardcode the project_id and regions, or pass it in as a parameter to give you more flexibility. If this is required change the parameters to $1 and $2. IF you take this route ensure to test that a parameter is being passed in


Once deployed, GCP will give you a public URL for your Cloud Run service. You can now access your Flask app from this URL.

5. Automate Deployment Using GitHub Actions

To automate the build and deployment process using GitHub Actions, you need to set up a workflow file. This will automatically build the Docker image, push it to GCR, and deploy it to Cloud Run whenever you push to your repository.
Setup GitHub Secrets:

    In your GitHub repository, go to Settings → Secrets and add:
        GCP_PROJECT_ID: Your GCP Project ID.
        GCP_REGION: The GCP region for deployment (e.g., us-central1).
        GCP_SERVICE_KEY: The service account JSON key (as a base64-encoded string).

        (see extras/.githib/workflow/deploy.yml)

#### Workflow Steps:

* Checkout Code: The repository is checked out to get the source code.
* Set Up Google Cloud SDK: The action sets up the Google Cloud SDK and authenticates using the service account key.
* Authenticate Docker: Authenticates Docker to push images to Google Container Registry (GCR).
* Build and Push Docker Image: The Docker image is built and pushed to GCR.
* Deploy to Cloud Run: The Docker image is deployed to Cloud Run.

Now, whenever you push changes to the main branch, this workflow will automatically build the Docker image, push it to GCR, and deploy it to Google Cloud Run.


6. Monitoring and Scaling

* Auto-scaling: Google Cloud Run automatically scales up or down based on the traffic to your service, meaning it can handle large traffic spikes without manual intervention.
* Monitoring: You can monitor the service using Google Cloud Monitoring, which integrates with Cloud Run to track metrics like request count, response times, and errors.



## Recommendations.
1. if you extend yoo build a more functional python application consider using poetry as it offer more functionality around package management - https://python-poetry.org/

It works well with many tools include black, isort
here is a pyproject.toml to get you started

[tool.black]
line-length = 88
target-version = ['py39']
skip-string-normalization = true

[tool.isort]
profile = "black"



2. as mentioned before, Alpine is under alot of flux so if you pin a version, it probably not a good idea to pull images remotely. 

3. It is good practice to use pre-commit hooks that check code before pushing to a repo to ensure compliance (both code styles and security vulnerabilities ). 
    * This ensures consistent code formatting and proper import ordering.
    * This helps maintain clean code, prevents formatting issues, and improves collaboration between team members.
    * The automated checks in the pipeline guarantee that no unformatted or improperly ordered imports are committed to the repository.

Adding these tools improves code quality and can catch errors early in the development process.

e.g. for black and isort
   pip install pre-commit
   Create a .pre-commit-config.yaml file:

    repos:
    - repo: https://github.com/psf/black
        rev: 23.7.0
        hooks:
        - id: black
    - repo: https://github.com/PyCQA/isort
        rev: 5.10.1
        hooks:
        - id: isort

and install it
pre-commit install

now this will run everytime prior to commit/
You can do similar security checks with checkov


4. add SAST and DAST to your pipeline
