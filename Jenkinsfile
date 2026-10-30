pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE = "hello-uat:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                retry(3) {
                    checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker build -t ${env.DOCKER_IMAGE} ."
                    } else {
                        bat "docker build -t ${env.DOCKER_IMAGE} ."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker run --rm ${env.DOCKER_IMAGE} python -m pytest -v"
                    } else {
                        bat "docker run --rm ${env.DOCKER_IMAGE} python -m pytest -v"
                    }
                }
            }
        }

        stage('Run Application') {
            steps {
                script {
                    if (isUnix()) {
                        sh "docker run --rm ${env.DOCKER_IMAGE}"
                    } else {
                        bat "docker run --rm ${env.DOCKER_IMAGE}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            script {
                if (isUnix()) {
                    sh "docker rmi ${env.DOCKER_IMAGE} || true"
                } else {
                    bat "docker rmi ${env.DOCKER_IMAGE} || exit 0"
                }
            }
        }
    }
}
