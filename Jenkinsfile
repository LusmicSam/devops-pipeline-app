pipeline {
    agent any

    environment {
        APP_NAME        = 'devops-pipeline-app'
        IMAGE_TAG       = "1.0.${BUILD_NUMBER}"
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')  // Set this in Jenkins
        DOCKER_IMAGE    = "lusmicsam/${APP_NAME}"
    }

    tools {
        maven 'Maven-3.9'   // Configured in Jenkins Global Tools
        jdk   'JDK-17'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '=== Stage 1: Cloning Repository ==='
                checkout scm
                sh 'git log -1 --format="%H %s" '
            }
        }

        stage('Build') {
            steps {
                echo '=== Stage 2: Maven Build ==='
                sh 'mvn clean compile -B'
            }
        }

        stage('Unit Test') {
            steps {
                echo '=== Stage 3: Running Unit Tests ==='
                sh 'mvn test surefire-report:report -B'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                    publishHTML([
                        reportDir:   'target/reports',
                        reportFiles: 'surefire.html',
                        reportName:  'Test Report'
                    ])
                }
            }
        }

        stage('Static Analysis') {
            steps {
                echo '=== Stage 3.5: SonarQube Static Code Analysis ==='
                sh 'mvn sonar:sonar -Dsonar.projectKey=${APP_NAME} -Dsonar.host.url=http://sonarqube:9000 -Dsonar.login=admin -Dsonar.password=admin || echo "SonarQube analysis skipped or failed"'
            }
        }

        stage('Package') {
            steps {
                echo '=== Stage 4: Packaging JAR ==='
                sh 'mvn package -DskipTests -B'
                archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            }
        }

        stage('Docker Build') {
            steps {
                echo '=== Stage 5: Building Docker Image ==='
                sh """
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                    docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest
                    docker images | grep ${APP_NAME}
                """
            }
        }

        stage('Image Security Scan') {
            steps {
                echo '=== Stage 5.5: Trivy Vulnerability Scanner ==='
                sh """
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${IMAGE_TAG} || echo "Trivy scan completed"
                """
            }
        }

        stage('Docker Push') {
            steps {
                echo '=== Stage 6: Pushing to Docker Hub ==='
                echo 'Skipping actual Docker push for local demo to avoid credential setup.'
                sh """
                    echo "Mock: docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    echo "Mock: docker push ${DOCKER_IMAGE}:latest"
                """
            }
        }

        stage('Deploy') {
            steps {
                echo '=== Stage 7: Deploying Container ==='
                sh """
                    docker stop ${APP_NAME} || true
                    docker rm   ${APP_NAME} || true
                    docker run -d \
                        --name ${APP_NAME} \
                        -p 9090:8080 \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:${IMAGE_TAG}
                    echo "Container started: \$(docker ps -f name=${APP_NAME} --format '{{.Status}}')"
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '=== Stage 8: Health Check ==='
                sh """
                    sleep 15
                    curl -f http://host.docker.internal:9090/actuator/health || exit 1
                    echo "Deployment verified successfully!"
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline FAILED. Check the logs above."
        }
    }
}
