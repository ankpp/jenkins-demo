pipeline {
    agent any

    stages {
        stage('CloneRepository') {
            steps {
                git branch: 'main', credentialsId: '01105d51-6f45-48e7-89e6-722d5d9f14d2', poll: false, url: 'https://github.com/ankpp/jenkins-demo'
            }
        }
    }
    post {
        always {
            sh 'python3 gchat_notifications.py Build has changed status:'
        }
        success {
            sh 'python3 gchat_notifications.py Build has successfully completed. Status PASSED!'
        }
        failure {
            sh 'python3 gchat_notifications.py Build ran with some errors. Status FAILED!'
        }
    }
}