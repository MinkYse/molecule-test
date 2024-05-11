pipeline {
  agent {
    docker {
      alwaysPull true
      image 'retr0h/molecule'
      args '--privileged -v /DATA/docker-cache:/docker-cacheargs -u root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }
  stages {
    stage('run test') {
      steps {
        sh 'rmdir  -rf /tmp/molecule/test/default'
        sh 'molecule --debug test'
      }
    }
  }
}
