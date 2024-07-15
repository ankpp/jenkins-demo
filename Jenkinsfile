pipeline {
    agent any

    stages {
        stage('CloneRepository') {
            steps {
                git branch: 'main', credentialsId: '01105d51-6f45-48e7-89e6-722d5d9f14d2', poll: false, url: 'https://github.com/ankpp/jenkins-demo'
            }
        }
    }
}