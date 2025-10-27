pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/jacoisrael2"
        IMAGE_NAME = "travel-budget-app"
        IMAGE_TAG = "latest"
        K8S_NAMESPACE = "travel"
        DEPLOY_REPO = "https://github.com/jacoisrael2/travel-budget-app-deploy.git"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-creds', url: 'https://github.com/jacoisrael2/travel-budget-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Image to Registry') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    sh """
                    echo "$DOCKERHUB_TOKEN" | docker login -u jacoisrael2 --password-stdin
                    docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Update K8s manifests (GitOps)') {
            steps {
                script {
                    sh """
                    git clone ${DEPLOY_REPO} deploy-repo
                    cd deploy-repo/k8s
                    yq e -i '.spec.template.spec.containers[0].image = "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"' deployment.yaml
                    git config --global user.email "jenkins@ntt.com"
                    git config --global user.name "Jenkins CI"
                    git commit -am "Update image to ${IMAGE_TAG}"
                    git push origin main
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Build and Push successful!'
        }
        failure {
            echo '❌ Build failed!'
        }
    }
}

