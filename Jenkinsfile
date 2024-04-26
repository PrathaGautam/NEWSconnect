pipeline {
  agent any
  stages {
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/PrathaGautam/NEWSconnect', branch: 'main')
      }
    }

    stage('Log') {
      steps {
        sh '''ls -la
'''
      }
    }

  }
}