pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''
        #!/bin/bash
        export PATH=${PATH}:/usr/local/bin:/usr/bin
        pip freeze
        '''
      }
    }
    stage('install deps') {
      steps {
        sh 'echo "ready"'
      }
    }
  }
}