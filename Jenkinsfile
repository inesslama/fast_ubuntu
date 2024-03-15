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
    stage("helm install"){
    steps{
       echo "Helm install"             
       sh 'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3'
       sh  'chmod 700 get_helm.sh'
       sh   './get_helm.sh'
     }
    }
      stage('Deploying application on k8s cluster') {
            steps {
               script{
                   withCredentials([file(credentialsId: 'TEST', variable: 'KUBECONFIG')])  {
                       dir('kubechart/') {
 
                        sh 'helm upgrade --install --set image.repository="docker1299999/crud_app " --set image.tag="1.0" myrelease kubechart/ ' 
                      }
                    }
               }
            }
        }
  }

}