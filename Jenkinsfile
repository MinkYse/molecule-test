pipeline {
  agent {
    docker {
      alwaysPull true
      image 'alainchiasson/docker-molecule'
      args '--privileged -v /DATA/docker-cache:/docker-cacheargs -u root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }
  stages {
    stage('run test') {
      steps {
        sh 'MOLECULE_NO_LOG="false"'
        sh 'molecule --debug test'
      }
    }
  }
}
