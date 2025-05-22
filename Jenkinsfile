pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'superlike1'
        IMAGE_FRONTEND = "${DOCKER_HUB_USER}/frontend-app"
        IMAGE_BACKEND  = "${DOCKER_HUB_USER}/backend-app"
        IMAGE_GERADOR  = "${DOCKER_HUB_USER}/gerador-app"
        IMAGE_MYSQL    = "${DOCKER_HUB_USER}/mysql-app"
        IMAGE_RSCRIPT  = "${DOCKER_HUB_USER}/rscript-app"
        IMAGE_FLASKAPI = "${DOCKER_HUB_USER}/flask-app"
    }

    stages {
        stage('Build Imagens Base') {
            steps {
                script {
                    echo "Construindo imagens base..."
                    sh "docker build -t ${IMAGE_FRONTEND}:latest ./frontend"
                    sh "docker build -t ${IMAGE_BACKEND}:latest ./backend"
                    sh "docker build -t ${IMAGE_GERADOR}:latest ./backend"
                    sh "docker build -t ${IMAGE_MYSQL}:latest ./mysql"
                    sh "docker build -t ${IMAGE_FLASKAPI}:latest ./api"
                }
            }
        }

        stage('Subir DB e Executar Gerador para criar CSV') {
            steps {
                script {
                    echo "Criando diretório backend no workspace e ajustando permissões..."
                    sh """
                        mkdir -p "${env.WORKSPACE}/backend"
                        chmod 777 "${env.WORKSPACE}/backend"
                    """

                    echo "Subindo banco de dados MySQL..."
                    sh 'docker-compose up -d db'

                    echo "Aguardando banco de dados ficar pronto..."
                    sh 'sleep 15'

                    echo "Executando container gerador para criar arquivo CSV..."
                    sh 'docker-compose run --rm gerador'

                    echo "Verificando se arquivo alunos_com_erros.csv foi criado..."
                    sh """
                        if [ -f "${env.WORKSPACE}/backend/alunos_com_erros.csv" ]; then
                            echo "Arquivo alunos_com_erros.csv encontrado."
                        else
                            echo "Arquivo alunos_com_erros.csv NÃO encontrado! Abortando pipeline."
                            exit 1
                        fi
                    """
                }
            }
        }

        stage('Build Imagem RScript') {
            steps {
                script {
                    echo "Construindo imagem do RScript..."
                    sh "docker build -t ${IMAGE_RSCRIPT}:latest ./rscript"
                }
            }
        }

        stage('Executar Script R com Volume') {
            steps {
                script {
                    echo "Executando o script R dentro do contêiner, com volume mapeado para dados..."
                    sh """
                        docker run --rm \
                            -v "${env.WORKSPACE}/rscript:/app/rscript" \
                            -v "${env.WORKSPACE}/backend/data:/app" \
                            ${IMAGE_RSCRIPT}:latest \
                            Rscript /app/rscript/limpeza.r
                    """

                    echo "Verificando se arquivo alunos_corrigido.csv foi gerado..."
                    sh """
                        if [ -f "${env.WORKSPACE}/backend/data/alunos_corrigido.csv" ]; then
                            echo "Arquivo alunos_corrigido.csv gerado com sucesso!"
                        else
                            echo "Arquivo alunos_corrigido.csv NÃO encontrado! Abortando pipeline."
                            exit 1
                        fi
                    """
                }
            }
        }

        stage('Push Imagens para Docker Hub') {
            steps {
                script {
                    echo "Logando no Docker Hub e enviando imagens..."
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-token',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${IMAGE_FRONTEND}:latest
                            docker push ${IMAGE_BACKEND}:latest
                            docker push ${IMAGE_GERADOR}:latest
                            docker push ${IMAGE_MYSQL}:latest
                            docker push ${IMAGE_RSCRIPT}:latest
                            docker push ${IMAGE_FLASKAPI}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy com Docker Compose') {
            steps {
                script {
                    echo "Finalizando e removendo containers antigos..."
                    sh 'docker-compose down --remove-orphans'

                    echo "Subindo containers atualizados em background..."
                    sh 'docker-compose up -d --force-recreate'
                }
            }
        }

        stage('Start Grafana') {
            steps {
                sh '''
                    docker run -d --name grafana \
                        -p 3000:3000 \
                        -v grafana-storage:/var/lib/grafana \
                        grafana/grafana-oss
                '''
            }
        }

        stage('Start Prometheus') {
            steps {
                sh '''
                    docker run -d --name prometheus \
                        -p 9090:9090 \
                        -v prometheus-storage:/prometheus \
                        prom/prometheus
                '''
            }
        }

        stage('Start Loki') {
            steps {
                sh '''
                    docker run -d --name loki \
                        -p 3100:3100 \
                        -v loki-storage:/loki \
                        grafana/loki
                '''
            }
        }

        stage('Start Stack') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            echo "Limpeza pós-build..."
            sh """
                docker system prune -f || true
                rm -f "${env.WORKSPACE}/backend/alunos_com_erros.csv" || true
            """
        }
    }
}
// Fim do pipeline