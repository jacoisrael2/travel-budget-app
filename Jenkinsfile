pipeline {
    agent none

    environment {
        IMAGE_NAME = "israelrop4/travel-app"
    }

    stages {
        stage('Checkout') {
            agent { label 'dind' }
            steps {
                git branch: 'main', url: 'https://github.com/jacoisrael2/travel-budget-app.git'
                echo "✅ Código clonado com sucesso!"
            }
        }

        stage('Build Docker Image') {
            agent { label 'dind' }
            steps {
                script {
                    echo "🏗️ Construindo imagem Docker..."
                    sh 'docker info'
                    sh 'docker build -t $IMAGE_NAME:${BUILD_NUMBER} .'
                }
            }
        }

        stage('Push to Docker Hub') {
            agent { label 'dind' }
            steps {
                script {
                    echo "📦 Enviando imagem para Docker Hub..."
                    withDockerRegistry([credentialsId: 'dockerhub-creds', url: 'https://index.docker.io/v1/']) {
                        sh 'docker push $IMAGE_NAME:${BUILD_NUMBER}'
                    }
                }
            }
        }

        stage('Deploy Trigger (GitOps)') {
            agent any
            steps {
                echo "🚀 Atualizando repositório de deploy para ArgoCD..."
            }
        }
    }

    post {
        success {
            echo "✅ Build e Push concluídos com sucesso!"
        }
        failure {
            echo "❌ Falha no pipeline. Verifique os logs no Jenkins."
        }
    }
}

