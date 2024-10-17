# Use Python 3.9 Alpine as the base image
FROM python:3.9-alpine

# Set environment variables to minimize output and handle Python buffering
ENV PYTHONUNBUFFERED=1 \
    APP_VERSION="local-docker" \
    APP_DESCRIPTION="local docker build" \
    APP_COMMIT_SHA="unknown"

# Set working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install necessary dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
