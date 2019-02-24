pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''
        #!/bin/bash
        
        #source ~/.jenkins_profile
        virtualenv draught-pick-jenkin --python=python3.6
        which pip
        which python
        #pip install -r requirements.txt
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
