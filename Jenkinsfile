pipeline {
  agent any
  stages {
    stage('env setup') {
      steps {
        sh '''export DJANGO_SETTINGS_MODULE="draught_picks.travis_settings"
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
