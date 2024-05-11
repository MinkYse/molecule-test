pipeline {
  agent {
    docker {
      alwaysPull true
      image 'alainchiasson/docker-molecule'
      args '--privileged -v /DATA/docker-cache:/docker-cache'
    }
  }
  stages {
    stage('run test') {
      steps {
        sh 'molecule test'
      }
    }
  }
}
