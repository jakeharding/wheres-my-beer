pipeline {
  agent any
  environment {
    PATH="/usr/local/bin:$PATH"
    PROJECT_NAME="draught-picks-backend"
  }
  stages {
    stage('env') {
      steps {
        script {
          if (env.BRANCH_NAME.startsWith('PR')) {
            currentBuild.displayName = "${env.CHANGE_BRANCH}"
          } else {
            currentBuild.displayName = "${env.BRANCH_NAME}"
          }
        }
        sh '''
        #!/bin/bash        
        virtualenv .envs/draught-picks-backend -p /usr/local/bin/python3
        '''
      }
    }
    stage('deps') {
      steps {
        sh '''
        #!/bin/bash
        source .envs/draught-picks-backend/bin/activate
        pip install -r requirements.txt
        '''
      }
    }
    
    stage('test') {
      steps {
        sh '''
        #!/bin/bash
        source .envs/draught-picks-backend/bin/activate
        cd draught_picks && python manage.py test
        '''
      }
    }
  }
}
