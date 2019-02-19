pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''psql -c "CREATE DATABASE travisdb;" -U postgres
export DJANGO_SETTINGS_MODULE="draught_picks.travis_settings"
mkvirtualenv draught --python=python3.6'''
      }
    }
    stage('install deps') {
      steps {
        sh 'echo "ready"'
      }
    }
  }
}