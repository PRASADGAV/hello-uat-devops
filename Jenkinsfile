pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout from Git') {
            steps {
                checkout scm
            }
        }

        stage('Tool preflight') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 --version'
                        sh 'git --version'
                        sh 'docker --version'
                        sh 'docker info'
                    } else {
                        bat 'py -3 --version'
                        bat 'git --version'
                        bat 'docker --version'
                        bat 'docker info'
                    }
                }
            }
        }

        stage('Install dependencies and run pytest') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv .venv'
                        sh '.venv/bin/python -m pip install --upgrade pip'
                        sh '.venv/bin/python -m pip install -r requirements.txt -r requirements-monitoring.txt'
                        sh 'mkdir -p reports'
                        sh '.venv/bin/python -m pytest -q --junitxml=reports/pytest.xml'
                    } else {
                        bat 'py -3 -m venv .venv'
                        bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                        bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt -r requirements-monitoring.txt'
                        bat 'if not exist reports mkdir reports'
                        bat '.venv\\Scripts\\python.exe -m pytest -q --junitxml=reports/pytest.xml'
                    }
                }
            }
        }

        stage('Build and run Docker image') {
            steps {
                script {
                    def imageTag = "hello-uat:${env.BUILD_NUMBER}"
                    if (isUnix()) {
                        sh "docker pull python:3.12-slim"
                        sh "docker build -t ${imageTag} ."
                        sh "docker run --rm ${imageTag}"
                        sh "docker run --rm ${imageTag} python -m pytest -q"
                    } else {
                        bat 'docker pull python:3.12-slim'
                        bat "docker build -t ${imageTag} ."
                        bat "docker run --rm ${imageTag}"
                        bat "docker run --rm ${imageTag} python -m pytest -q"
                    }
                }
            }
        }

        stage('Evidently monitoring report') {
            steps {
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python monitor.py'
                    } else {
                        bat '.venv\\Scripts\\python.exe monitor.py'
                    }
                }
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/pytest.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
