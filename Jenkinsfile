pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/israelrop4"
        IMAGE_NAME = "travel-app"
        DEPLOY_REPO = "https://github.com/jacoisrael2/travel_budget_app_deploy.git"
        DEPLOY_BRANCH = "main"
        DEPLOY_PATH = "k8s/deployment.yaml"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔹 Clonando repositório da aplicação..."
                git credentialsId: 'github-creds', url: 'https://github.com/jacoisrael2/travel_budget_app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🏗️ Construindo imagem Docker..."
                    sh """
                        docker build -t ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} .
                        docker tag ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "📦 Enviando imagem para Docker Hub..."
                    withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                        sh """
                            echo "$DOCKER_TOKEN" | docker login -u israelrop4 --password-stdin
                            docker push ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                            docker push ${REGISTRY}/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }

        stage('Update ArgoCD GitOps Repo') {
            steps {
                script {
                    echo "🧩 Atualizando repositório de deploy com a nova imagem..."
                    withCredentials([
                        string(credentialsId: 'GITHUB_TOKEN', variable: 'GIT_TOKEN')
                    ]) {
                        sh """
                            rm -rf deploy-repo || true
                            git clone https://x-access-token:${GIT_TOKEN}@github.com/jacoisrael2/travel_budget_app_deploy.git deploy-repo
                            cd deploy-repo

                            # Atualiza a imagem no manifest YAML
                            yq e -i '.spec.template.spec.containers[0].image = "${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"' ${DEPLOY_PATH}

                            git config --global user.email "jenkins@nttdata.com"
                            git config --global user.name "Jenkins CI"
                            git add ${DEPLOY_PATH}
                            git commit -m "🚀 Atualiza imagem para build ${BUILD_NUMBER}"
                            git push origin ${DEPLOY_BRANCH}
                        """
                    }
                }
            }
        }

        stage('Deploy Trigger') {
            steps {
                echo "🔄 ArgoCD detectará o commit e sincronizará automaticamente o cluster."
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completo: imagem publicada e ArgoCD será sincronizado!"
        }
        failure {
            echo "❌ Falha no pipeline. Verifique logs no Jenkins."
        }
    }
}

