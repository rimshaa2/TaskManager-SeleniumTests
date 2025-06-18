pipeline {
    agent any

    environment {
        TEST_IMAGE = 'selenium-tests'
    }

    stages {
        stage('Clone Test Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/rimshaa2/TaskManager-SeleniumTests.git'
            }
        }

        stage('Build Test Container') {
            steps {
                sh 'docker build -t $TEST_IMAGE .'
            }
        }

        stage('Run Headless Tests') {
            steps {
                sh 'docker run --rm --network=host $TEST_IMAGE'
            }
        }
    }

    post {
        always {
            echo 'Test pipeline completed.'
        }
    }
}
