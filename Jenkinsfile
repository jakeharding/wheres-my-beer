pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''
        #!/bin/bash
        export PATH=${PATH}:/usr/local/bin:/usr/bin
        pwd
        mkvirtualenv draught-pick-jenkin --python=python3.6
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
