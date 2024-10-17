# Flask Healthcheck API
This is a simple Python Flask web application that provides a /healthcheck endpoint. The endpoint returns information about the application such as version, description, and the last commit SHA in JSON format. The application is containerized using Docker, and a CI pipeline is implemented using GitHub Actions.



## Directory structure
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline
├── my_flask_app/
│   ├── __init__.py             # Initializes the Flask application package
│   ├── app.py                   # Main application file with Flask setup
│   ├── requirements.txt         # Python dependencies
│   └── tests/
│       ├── __init__.py         # Initializes the tests package
│       └── test_app.py          # Unit tests for the application
├── Dockerfile                   # Dockerfile for containerizing the application
├── helm/
│   └── my-flask-app/
│       ├── Chart.yaml          # Helm chart metadata
│       ├── values.yaml         # Default values for the Helm chart
│       └── templates/
│           ├── deployment.yaml  # Kubernetes Deployment template
│           └── service.yaml     # Kubernetes Service template
├── README.md                    # Project documentation
├── technical_notes.md           # Project documentation
└── .dockerignore                # Docker ignore file


## Features
* A /healthcheck API endpoint that returns:

    * Application version
    * Description
    * Last commit SHA

* Dockerized for easy deployment
* Continuous Integration (CI) using GitHub Actions

## Example API Response
json 

    {
      "myapplication": [
        {
        "version": "1.0",
        "description": "pre-interview technical test",
        "lastcommitsha": "abc12345678"
        }
        ]
    }

## Requirements
* Python 3.9+
* Docker (for containerization)
* GitHub account (for CI pipeline and secrets)

## Setup and Usage
### 1. Clone the repository

bash

    git clone <repository-url>
    cd <repository-name>

### 2. Install dependencies

If you wish to run the application locally without Docker, you need to install the dependencies using pip:

bash

    pip install -r requirements.txt

### 3. Run the Flask Application Locally

bash

    python app.py

This will start the Flask server at http://localhost:5000/. You can access the healthcheck endpoint at:

bash

    http://localhost:5000/healthcheck

### 4. Docker Setup

To containerize the application, follow the steps below:

#### Build the Docker image  

bash (note the fullstop at the end)

    docker build -t my-flask-app .

#### Run the Docker container

bash  

Notes:
    
* -p - this is will forward data locally on port 5000 to 5000 inside the container
* -rm - remove the container image on termination (cleanup)
* -it - interactive
* -d - run it detact mode

    docker run -it -d -rm -p 5000:5000 my-flask-app


This will start the containerized application, and you can access the healthcheck endpoint at:

bash

    http://localhost:5000/healthcheck

To confirm it is actually running a number other options are available (especially if there is no response)


    docker ps  # to get the container id
    docker logs --since=1h  container_id   #check if there are any errors

### 5. Continuous Integration (CI)

 A GitHub Actions workflow is set up to automate the process of building the application and running checks on each push to the main branch. Note, the main (master) branch should be protected and will need two approvers


 #### GitHub Secrets

If you want to push your Docker image to DockerHub as part of the CI pipeline, make sure to add the following secrets to your GitHub repository:

    * DOCKER_USERNAME: Your DockerHub username
    * DOCKER_PASSWORD: Your DockerHub password or personal access token

The workflow will:

    * Build the application
    * Optionally push the Docker image to DockerHub

### CI Pipeline

The CI workflow is located in .github/workflows/ci.yml. It triggers on every push or pull request to the main branch. It does include additional steps like running tests or deployment to different platforms (AWS, GCP). You can comment out the platforms you do not need

The pipeline also does some code analysis such as isort, black and bandit. this can be extended by following the same pattern.

### 6. Testing

Basic python (pytests/curl tests exist to confirm that it is working. These check the return json payload and the HTML return code.


### 7. Security considerations
* **Input Validation**: For now, since the /healthcheck endpoint doesn't accept input, validation is not required. For future endpoints, use libraries like marshmallow for input validation.
* **Output Encoding**: Always ensure that your output is properly encoded, especially for user-generated content. Flask handles most of this by default.
* **Secrets Handling**: Use environment variables for sensitive information like API keys, database credentials, and Docker secrets.
* **External Images** Whenever using external images or libraries do follow the DevSecOps principles and to vulberability checks in the left of the pipeline

### 8. Monitoring Setup

For monitoring, you can integrate tools like Prometheus and Grafana to track the application's performance and health. A simple setup with Flask can use the prometheus_flask_exporter.

To add basic monitoring:
* Install the prometheus_flask_exporter in requirements.txt

   prometheus-flask-exporter==0.18.3

* Modify app.py to include:
    from prometheus_flask_exporter import PrometheusMetrics

    metrics = PrometheusMetrics(app)

This will expose metrics at /metrics by default, which can be scraped by Prometheus.
## GitHub secrets
Make sure the following secrets are set up in your GitHub repository:

    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_REGION
    GCP_PROJECT_ID
    GCP_SERVICE_ACCOUNT_KEY
    DOCKERHUB_USERNAME and DOCKERHUB_PASSWORD
    KUBE_CONFIG_DATA (base64-encoded Kubernetes config file for authenticating kubectl).

    
## AWS / GCP
If you wish to deploy to these platform is is assumed you already have an existing account as it is outside the context of this example. However, some guideines are provided to deploy to these platforms from outside the pipeline

This example will focus on deploying to AWS Elastic Beanstalk.

AWS Elastic Beanstalk is a Platform-as-a-Service (PaaS) offered by Amazon Web Services (AWS) that simplifies the deployment, management, and scaling of web applications and services. It allows developers to focus on writing code without worrying about the underlying infrastructure, such as servers, load balancers, and networking. Elastic Beanstalk automatically handles the provisioning, scaling, and monitoring of these resources.

(for more complex scenarios you could use fargate, and kubernetes (AKE) on AWS)


### Local Testing of Deployments
#### AWS Elastic Beanstalk
bash
    pip install awsebcli
    eb init -p docker my-flask-app --region <region>
    eb create flask-env
    eb deploy

#### GCP Cloud Run
bash
note, you will need to substitute your own project id and and region
    gcloud auth login
    gcloud config set project <your-project-id>
    docker build -t gcr.io/<your-project-id>/my-flask-app .
    docker push gcr.io/<your-project-id>/my-flask-app
    gcloud run deploy my-flask-app \
    --image gcr.io/<your-project-id>/my-flask-app:latest \
    --platform managed \
    --region <region>> \
    --allow-unauthenticated


#### Locally (and potentially) remote K8s instant via Hekm
bash
    kubectl config use-context <your-cluster>
    helm upgrade --install my-flask-app ./my-flask-app --set image.repository=<your-dockerhub-username>/my-flask-app --set image.tag=latest


### Other considerations.
1. Look at the technical_notes.md
2. this code is subject to change without warning and is provided as it.
3. For the k8s deployment see NOTES.txt.
   It is a simple example of a deployment, a few variables (values.yml), and runs as a service to live/ready probes (similar to prometheus/datadog)

### License
This project is licensed under the MIT License - see the LICENSE file for details.