pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''
        #!/bin/bash
        export PATH=${PATH}:/usr/local/bin:/usr/bin
        source /Users/jakeharding/.bash_profile
        which pip
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
