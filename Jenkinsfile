pipeline {
    agent any

    environment {
        REGISTRY = "rsharoni"                 // your Docker Hub username
        IMAGE = "hello-world"                 // your Docker Hub repo name
        TAG = "1.0.0"                         // or "latest"
    }

    stages {

        stage('Checkout from GitHub') {
            steps {
                git url: 'https://github.com/rsharoni/hello-world-project.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $REGISTRY/$IMAGE:$TAG ./phase1'
            }
        }

       stage('Test') {
            steps {
                sh '''
                    echo "Running simple container health test..."

                    # Start the container in the background
                    docker run -d --name test_container $REGISTRY/$IMAGE:$TAG

                    # Wait 3 seconds to see if it crashes
                    sleep 3

                    # Check if the container is still running
                    if [ "$(docker ps -q -f name=test_container)" ]; then
                        echo "Container is healthy"
                        docker rm -f test_container
                        exit 0
                    else
                        echo "Container crashed!"
                        docker logs test_container || true
                        docker rm -f test_container || true
                        exit 1
                    fi
                '''
            }
        }


        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $REGISTRY/$IMAGE:$TAG'
                }
            }
        }

        stage('Debug Tools') {
            steps {
                sh 'which kubectl || echo "kubectl NOT FOUND"'
                sh 'which helm || echo "helm NOT FOUND"'
                sh 'kubectl version --client || echo "kubectl BROKEN"'
                sh 'helm version || echo "helm BROKEN"'
            }
        }

        stage('Deploy with Helm') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig-cred']) {
                   sh '''
                    kubectl get namespace dev || kubectl create namespace dev
                    kubectl apply -n dev -f ./phase3/pv.yaml
                    helm upgrade --install hello-world ./phase3/hello-world-chart --namespace dev --create-namespace
                    '''
                }
            }
        }
    }
}
