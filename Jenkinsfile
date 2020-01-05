pipeline {
  agent any
  environment {
    PATH="/usr/local/bin:$PATH"
    PROJECT_NAME="draught-picks-backend"
    # MAke sure Python uses UTF-8
    LANG="en_US.UTF-8"
    PYTHONIOENCODING="UTF-8"
  }
  stages {
    stage('env') {
      steps {
        load "${JENKINS_HOME}/project_props/draught-picks-backend.properties"
        script {
          if (env.BRANCH_NAME.startsWith('PR')) {
            env.JOB_BASE_NAME = "${env.CHANGE_BRANCH}"
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
        pip install python-coveralls coverage
        cd draught_picks/ && python manage.py migrate
        coverage run --source=beers,draught_picks,rest_api,users,description_parser --omit=manage.py,draught_picks/wsgi.py,tf_model/ manage.py test
        '''
      }
    }

    stage('coveralls') {
      steps {
        sh '''
        #!/bin/bash
        source .envs/draught-picks-backend/bin/activate
        echo "repo_token: $COVERALLS_TOKEN" > .coveralls.yml
        coveralls
        '''
      }
    }
  }
}
