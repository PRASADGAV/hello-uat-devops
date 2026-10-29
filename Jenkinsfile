pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE = "hello-uat-python:${env.BUILD_NUMBER}"
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
                        sh 'git --version'
                        sh 'docker --version'
                        sh 'docker info'
                    } else {
                        bat 'git --version'
                        bat 'docker --version'
                        bat 'docker info'
                    }
                }
            }
        }

        stage('Build Docker image with dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker pull python:3.12-slim'
                        sh "docker build --network=host --build-arg PIP_DEFAULT_TIMEOUT=300 -t ${env.DOCKER_IMAGE} ."
                    } else {
                        bat 'docker pull python:3.12-slim'
                        bat "docker build --network=host --build-arg PIP_DEFAULT_TIMEOUT=300 -t ${env.DOCKER_IMAGE} ."
                    }
                }
            }
        }

        stage('Run tests in Docker') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'mkdir -p reports'
                        sh "docker run --rm -v \$(pwd)/reports:/app/reports ${env.DOCKER_IMAGE} python -m pytest -q --junitxml=/app/reports/pytest.xml"
                    } else {
                        bat 'if not exist reports mkdir reports'
                        bat "docker run --rm -v %CD%\\reports:/app/reports ${env.DOCKER_IMAGE} python -m pytest -q --junitxml=/app/reports/pytest.xml"
                    }
                }
            }
        }

        stage('Run application in Docker') {
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

        stage('Generate monitoring report in Docker') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'mkdir -p reports'
                        sh "docker run --rm -v \$(pwd)/reports:/app/reports -v \$(pwd)/monitor.py:/app/monitor.py -v \$(pwd)/requirements-monitoring.txt:/app/requirements-monitoring.txt ${env.DOCKER_IMAGE} bash -c 'pip install -r requirements-monitoring.txt && python monitor.py'"
                    } else {
                        bat 'if not exist reports mkdir reports'
                        bat "docker run --rm -v %CD%\\reports:/app/reports -v %CD%\\monitor.py:/app/monitor.py -v %CD%\\requirements-monitoring.txt:/app/requirements-monitoring.txt ${env.DOCKER_IMAGE} python -c \"import subprocess; subprocess.run(['pip', 'install', '-r', 'requirements-monitoring.txt']); exec(open('monitor.py').read())\""
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
