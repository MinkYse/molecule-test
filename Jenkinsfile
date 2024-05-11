pipeline {
  agent {
    docker {
      alwaysPull false
      image 'molecule-test'
      args '--privileged -v /DATA/docker-cache:/docker-cacheargs -u root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }
  stages {
    stage('run test') {
      steps {
        sh 'rm -rf /tmp/molecule/test/default'
        sh 'molecule test'
      }
    }
  }
}
