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
                        reportDir:   'target/site',
                        reportFiles: 'surefire-report.html',
                        reportName:  'Test Report'
                    ])
                }
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

        stage('Docker Push') {
            steps {
                echo '=== Stage 6: Pushing to Docker Hub ==='
                sh """
                    echo ${DOCKERHUB_CREDS_PSW} | docker login -u ${DOCKERHUB_CREDS_USR} --password-stdin
                    docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    docker push ${DOCKER_IMAGE}:latest
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
                        -p 8080:8080 \
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
                    curl -f http://localhost:8080/health || exit 1
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
            // emailext to: 'your-email@example.com', subject: "Build Failed: ${JOB_NAME}", body: "Build #${BUILD_NUMBER} failed."
        }
        always {
            sh 'docker logout || true'
        }
    }
}
