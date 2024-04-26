pipeline {
  agent any
  stages {
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/PrathaGautam/NEWSconnect', branch: 'main')
      }
    }

    stage('Log') {
      parallel {
        stage('Log') {
          steps {
            sh '''ls -la
'''
          }
        }

        stage('test_code') {
          steps {
            sh 'pytest test_main.py'
          }
        }

      }
    }

  }
}