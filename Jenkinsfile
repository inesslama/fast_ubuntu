pipeline {

  environment {
    dockerimagename = "docker1299999/crud_app:1.0"
    dockerImage = "docker1299999/crud_app:1.0"
  }

  agent any

  stages {

    stage('Checkout Source') {
      steps {
        git branch: 'main', url: 'https://github.com/inesslama/fast_ubuntu.git'
      }
    }

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build dockerImage
        }
      }
    }

    stage('Pushing Image') {
      environment {
               registryCredential = 'dockerhublogin'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("1.0")
          }
        }
      }
    }

   /*  stage('Deploying App to Kubernetes') {
      steps {
        script {
          kubernetesDeploy (configs: 'deploymentservice.yml', kubeconfigId: 'nv')
        }
      }
    } */
      stage('Deploying application on k8s cluster') {
            steps {
               script{
                   withCredentials([kubeconfigContent(credentialsId: 'nv', variable: 'KUBECONFIG')]) {
                       dir('kubernetes/') {
 
                        sh 'helm upgrade --install --set image.repository="docker1299999/crud_app " --set image.tag="1.0" myrelease kubechart/ ' 
                      }
                    }
               }
            }
        }
  }

}