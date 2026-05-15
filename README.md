# INT332 DevOps Pipeline Project
## Enterprise DevSecOps Pipeline: Docker + Kubernetes + Terraform + Jenkins + Prometheus + Grafana + SonarQube

---

## 🛠️ Tech Stack & Tools Used
* **App:** Java Spring Boot
* **Build:** Maven
* **CI/CD:** Jenkins & GitHub Actions
* **Containerization:** Docker & Docker Compose
* **Orchestration:** Kubernetes (k8s manifests)
* **Infrastructure as Code:** Terraform (AWS provisioning)
* **Static Analysis:** SonarQube
* **Vulnerability Scanning:** Trivy
* **Observability:** Prometheus & Grafana

---

## Prerequisites (Install These First)

| Tool         | Version | Download |
|--------------|---------|----------|
| Java JDK 17  | 17+     | https://adoptium.net |
| Maven        | 3.9+    | https://maven.apache.org |
| Docker       | Latest  | https://docker.com |
| Git          | Latest  | https://git-scm.com |

---

## Step-by-Step Local Setup Commands

### 1. Clone / Initialize Repository
```bash
git clone https://github.com/YOUR_USERNAME/devops-pipeline-app.git
cd devops-pipeline-app

# OR initialize fresh
git init
git add .
git commit -m "Initial commit: INT332 DevOps Project"
```

### 2. Build with Maven
```bash
# Clean and compile
mvn clean compile

# Run unit tests
mvn test

# Package into JAR
mvn clean package

# See the generated JAR
ls -lh target/devops-pipeline-app.jar
```

### 3. Run Locally (without Docker)
```bash
java -jar target/devops-pipeline-app.jar

# Test endpoints
curl http://localhost:8080/
curl http://localhost:8080/health
```

### 4. Build Docker Image
```bash
# Build the image
docker build -t devops-pipeline-app:1.0.0 .

# Verify image was created
docker images | grep devops-pipeline-app

# Inspect image layers
docker history devops-pipeline-app:1.0.0
```

### 5. Run with Docker
```bash
# Run container
docker run -d --name devops-app -p 8080:8080 devops-pipeline-app:1.0.0

# Check running containers
docker ps

# View logs
docker logs devops-app

# Test the app
curl http://localhost:8080/health

# Stop and remove
docker stop devops-app && docker rm devops-app
```

### 6. Run with Docker Compose (App + Jenkins)
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
docker-compose logs -f jenkins

# Stop all services
docker-compose down
```

### 7. Push to Docker Hub
```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag devops-pipeline-app:1.0.0 YOUR_DOCKERHUB_USERNAME/devops-pipeline-app:1.0.0
docker tag devops-pipeline-app:1.0.0 YOUR_DOCKERHUB_USERNAME/devops-pipeline-app:latest

# Push
docker push YOUR_DOCKERHUB_USERNAME/devops-pipeline-app:1.0.0
docker push YOUR_DOCKERHUB_USERNAME/devops-pipeline-app:latest
```

### 8. Access Jenkins
```bash
# Jenkins is running on port 8082 (via docker-compose)
# Open: http://localhost:8082

# Get initial admin password
docker exec devops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 9. Configure Jenkins Pipeline
1. Open Jenkins at http://localhost:8082
2. Install suggested plugins
3. Create new Pipeline job → name it "devops-pipeline"
4. Under Pipeline → Definition → "Pipeline script from SCM"
5. SCM: Git → enter your repo URL
6. Script Path: `Jenkinsfile`
7. Save and click "Build Now"

### 10. GitHub Actions (Automatic)
```bash
# Push to GitHub — CI/CD runs automatically
git add .
git commit -m "feat: add feature XYZ"
git push origin main

# Check Actions tab on GitHub for pipeline status
```

---

## Project Endpoints

| Endpoint        | Description              |
|-----------------|--------------------------|
| `GET /`         | App status and version   |
| `GET /health`   | Health check             |

---

## Useful Commands Reference

```bash
# List all containers (running + stopped)
docker ps -a

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Check Docker network
docker network ls

# Exec into running container
docker exec -it devops-app sh

# Maven skip tests
mvn package -DskipTests

# Maven verbose output
mvn clean install -X
```
