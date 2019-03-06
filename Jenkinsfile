pipeline {
  agent any
  environment {
    PATH="/usr/local/bin:$PATH"
    PROJECT_NAME="draught-picks-backend"
  }
  stages {
    stage('env') {
      steps {
        sh '''
        #!/bin/bash        
        virtualenv .envs/draught-picks-backend
        echo "Branch name: ${env.BRANCH_NAME}"
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
