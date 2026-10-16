# Django Stock Inventory Manager — Docker & Kubernetes

Application de gestion de stock (Django, MySQL), conteneurisée avec Docker et déployée sur Kubernetes (k3s).

## Docker Compose
    cp .env.example .env     # puis modifier les mots de passe
    docker compose up -d --build
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py createsuperuser

## Kubernetes (k3s)
    kubectl create secret generic stock-secret \
      --from-literal=SECRET_KEY="change-me" \
      --from-literal=DB_PASSWORD='change-me' \
      --from-literal=MYSQL_ROOT_PASSWORD='change-me'
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/mysql.yaml
    kubectl apply -f k8s/job-migrate.yaml
    kubectl apply -f k8s/web.yaml

Objets utilisés : Deployment, StatefulSet, Service, ConfigMap, Secret, Job, probes.
Démos : scaling, auto-guérison, rolling update, rollback.
