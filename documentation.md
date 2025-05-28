# BlueberryBlog Application Documentation

## Application Overview

BlueberryBlog is a Flask-based web application that allows users to register, log in, create blog posts, and comment on posts. It uses PostgreSQL as the database and SQLAlchemy as the ORM. The application is containerized using Docker and can be deployed locally, with Docker Compose, or on Kubernetes. CI/CD is managed via GitHub Actions, including code quality and coverage checks with SonarCloud.

---

## Local Development Setup

### 1. Clone the Repository
```pwsh
git clone <your-repo-url>
cd BlueberryBlog-main
```

### 2. Set Up Python Virtual Environment
```pwsh
python -m venv venv
.\venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
```pwsh
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Application Locally
```pwsh
python run.py
```
The app will be available at http://127.0.0.1:5000

---

## Using Docker

### 1. Build the Docker Image
```pwsh
docker build -t blueberryblog .
```

### 2. Run the Docker Container
```pwsh
docker run -p 5000:5000 --env-file .env blueberryblog
```
Or set environment variables directly with `-e` flags.

---

## Using Docker Compose

If you want to run the app with PostgreSQL using Docker Compose:

```pwsh
docker-compose up --build
```
This will start both the app and the database. The app will be available at http://localhost:5000

---

## Kubernetes Deployment

### 1. Deploy Resources
Apply the deployment and service manifests:
```pwsh
kubectl apply -f k8s/k8s-deployment.yaml
kubectl apply -f k8s/k8s-services.yaml
```
If you have an ingress controller, also apply:
```pwsh
kubectl apply -f k8s/k8s-ingress.yaml
```

### 2. Check Status
```pwsh
kubectl get pods
kubectl get svc
```

---

## Running Tests

### 1. Run All Tests
```pwsh
pytest
```

### 2. Run Tests with Coverage
```pwsh
pytest --cov=app --cov-report=term --cov-report=xml:coverage.xml
```

---

## CI/CD Pipeline (GitHub Actions)

- **Test Job:** Installs dependencies, runs tests, and generates a coverage report.
- **SonarQube Job:** Downloads the coverage report and runs a SonarCloud scan for code quality and coverage.
- **Docker Job:** Builds and pushes the Docker image to Docker Hub.
- **Deploy Job:** Uses kubectl to deploy the application to a Kubernetes cluster using the manifests in the `k8s/` directory.

Artifacts (like coverage.xml) are passed between jobs using upload/download actions.

---

## Important Commands Summary

- **Start Flask app locally:** `python run.py`
- **Run tests:** `pytest`
- **Build Docker image:** `docker build -t blueberryblog .`
- **Run Docker container:** `docker run -p 5000:5000 blueberryblog`
- **Start with Docker Compose:** `docker-compose up --build`
- **Kubernetes deploy:** `kubectl apply -f k8s/k8s-deployment.yaml && kubectl apply -f k8s/k8s-services.yaml`

---

## Notes
- Update environment variables and secrets for production use.
- Replace `<DOCKERHUB_USERNAME>` in Kubernetes manifests with your Docker Hub username.
- For production, use a secrets manager for sensitive data.

---

For any issues, check logs using Docker/Kubernetes commands or GitHub Actions logs for CI/CD troubleshooting.
