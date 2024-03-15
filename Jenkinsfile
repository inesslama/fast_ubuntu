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
       sh 'curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/kubectl'       
       sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" '
       sh 'sudo cp kubectl /usr/bin' 
       sh 'sudo chmod +x /usr/bin/kubectl'
       sh 'wget https://get.helm.sh/helm-v3.6.1-linux-amd64.tar.gz'
       sh 'ls -a'
       sh 'tar -xvzf helm-v3.6.1-linux-amd64.tar.gz'
       sh 'sudo cp linux-amd64/helm /usr/bin'
     }
    }
      stage('Deploying application on k8s cluster') {
            steps {
               script{
                   withCredentials([kubeconfigContent(credentialsId: 'nv', variable: 'KUBECONFIG')]) {
                       dir('kubechart/') {
 
                        sh 'helm upgrade --install --set image.repository="docker1299999/crud_app " --set image.tag="1.0" myrelease kubechart/ ' 
                      }
                    }
               }
            }
        }
  }

}