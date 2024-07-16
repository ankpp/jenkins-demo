pipeline {
    agent any
    stages {
        stage('CloneRepository') {
            steps {
                git branch: 'main', credentialsId: '01105d51-6f45-48e7-89e6-722d5d9f14d2', poll: false, url: 'https://github.com/ankpp/jenkins-demo'
            }
        }
        stage("Build") {
            steps {
                sh "python3 -m venv venv"
                sh ". venv/bin/activate"
                sh "pip3 install -r requirements.txt"
            }
        }
        stage("Lint&Test") {
            steps {
                sh "flake8"
                sh "python3 -m pytest"
            }
        }
    }
    post {
        always {
            sh 'python3 gchat_notifications.py "Build has changed status:"'
        }
        success {
            sh 'python3 gchat_notifications.py "Build has successfully completed. Status PASSED!"'
        }
        failure {
            sh 'python3 gchat_notifications.py "Build ran with some errors. Status FAILED!"'
        }
    }
}
// node {
//     stage('ChekoutSCM') {
//         checkout scm
//     }
//     stage('lint-flake8') {
//         def testImage = docker.build('test-container')

//         testImage.inside {
//             sh 'flake8'
//     }
//     }
//     stage("unit-testing") {
//         def testImage = docker.build('test-container')

//         testImage.inside {
//             sh 'pytest'
//         }
//     }
//     post {
//         always {
//             sh 'python3 gchat_notifications.py Build has changed status:'
//         }
//         success {
//             sh 'python3 gchat_notifications.py Build has successfully completed. Status PASSED!'
//         }
//         failure {
//             sh 'python3 gchat_notifications.py Build ran with some errors. Status FAILED!'
//         }
//     }
// }