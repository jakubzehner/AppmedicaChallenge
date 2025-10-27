resource "local_file" "push_image_script" {
  content  = <<-EOT
    #!/bin/bash

    gcloud auth configure-docker us-east1-docker.pkg.dev
    docker build -t backend ../../backend
    docker build -t frontend ../../frontend
    docker tag backend:latest ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/backend:latest
    docker tag frontend:latest ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/frontend:latest
    docker push ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/backend:latest
    docker push ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/frontend:latest
    EOT
  filename = "push_images.sh"
}

resource "local_file" "compose-prod" {
  content  = <<-EOT
    services:
        frontend:
            image: ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/frontend:latest

            ports:
                - "3000:80"

        backend:
            image: ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/backend:latest
            environment:
                LOGGER_LEVEL: 20
                DATABASE_URL: postgresql://appmedica:appmedica@postgres:5432/appmedica
                CORS_ALLOWED_ORIGINS: "*"
                GEMINI_API_KEY: ${local.envs["GEMINI_API_KEY"]}
                IMAP_SERVER: ${local.envs["IMAP_SERVER"]}
                IMAP_PORT: ${local.envs["IMAP_PORT"]}
                EMAIL_ACCOUNT: ${local.envs["EMAIL_ACCOUNT"]}
                EMAIL_APP_PASSWORD: ${local.envs["EMAIL_APP_PASSWORD"]}

            ports:
                - "8000:8000"

            healthcheck:
                interval: 10s
                timeout: 3s
                retries: 5
                start_period: 3s

            depends_on:
                postgres:
                    condition: service_healthy

        postgres:
            image: postgres:17
            environment:
                POSTGRES_USER: appmedica
                POSTGRES_PASSWORD: appmedica
                POSTGRES_DB: appmedica

            ports:
                - "5432:5432"

            volumes:
                - postgres_data:/var/lib/postgresql/data

            healthcheck:
                test: ["CMD", "pg_isready", "-U", "appmedica"]
                interval: 10s
                timeout: 3s
                retries: 5
                start_period: 3s

    volumes:
        postgres_data:
            driver: local
    EOT
  filename = "../compose-prod.yml"

}
