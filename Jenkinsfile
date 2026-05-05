pipeline {
    agent any

    environment {
        DOCKER_USER = "mistwake"
        GIT_REPO_URL = "https://github.com/mistwake/praktikum-kantin-app.git"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // mengambil kode terbaru dari github
                git branch: 'main', url: "${GIT_REPO_URL}"
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    // membangun image docker
                    // catatan: menggunakan sh karena berjalan di jenkins aks linux
                    sh "docker build -t ${USER}/kantin-backend:latest ./backend"
                    sh "docker build -t ${USER}/kantin-frontend:latest ./frontend"
                    
                    // login dan push ke docker hub
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${USER}/kantin-backend:latest"
                    sh "docker push ${USER}/kantin-frontend:latest"
                }
            }
        }

        stage('Deploy ke Azure AKS') {
            steps {
                // menggunakan file kubeconfig yang tersimpan di kredensial jenkins
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    // menerapkan file konfigurasi kubernetes
                    sh "kubectl apply -f kantin-k8s.yaml"
                    sh "kubectl apply -f kantin-ingress.yaml"
                    
                    // merestart deployment agar mengambil image terbaru
                    sh "kubectl rollout restart deployment backend-kantin"
                    sh "kubectl rollout restart deployment frontend-kantin"
                }
            }
        }
    }
}
