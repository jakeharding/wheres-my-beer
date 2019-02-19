pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''export DJANGO_SETTINGS_MODULE="draught_picks.travis_settings"
pip freeze'''
      }
    }
    stage('install deps') {
      steps {
        sh 'echo "ready"'
      }
    }
  }
}
