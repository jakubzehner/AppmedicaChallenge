# Appmedica Challenge

## Author: Jakub Zehner

### Overview

This project was created as part of the **Appmedica Fullstack Developer Challenge**.
It implements a fully containerized web application that periodically retrieves emails from a mailbox, summarizes attachments using an LLM, and displays the results in a simple public web interface.

The goal was to deliver a **clean, production-ready, and maintainable solution** with focus on reliability, simplicity, and infrastructure automation.

---

## 🧩 Technologies Used

### **Backend – FastAPI (Python)**

The backend is implemented using **FastAPI**, chosen for its speed and clean design.
Additional tools and libraries:

* **uv** – modern package and project manager for Python
* **ruff** – integrated linter and formatter
* **SQLModel** – ORM for PostgreSQL, combining SQLAlchemy and Pydantic
* **IMAP** – used to fetch incoming emails and attachments
* **Gemini API** – used as the LLM to generate concise Polish summaries of attachment contents

### **Database – PostgreSQL**

A PostgreSQL instance is used for structured storage of email metadata and generated summaries.

### **Frontend – React + Vite**

The frontend is a lightweight **React** single-page application built with **Vite**.
It communicates with the backend API and displays the list of email summaries.
Additional tools:

* **zod** – for runtime data validation and type-safe integration with the backend

### **Other Components**

* Entire application is containerized with **Docker**
* **Docker Compose** simplifies local development and orchestration
* **Google Cloud Platform (GCP)** used for deployment
* **Terraform** manages cloud infrastructure (Infrastructure as Code approach)

---

## ⚙️ Development Setup

### **Requirements**

* Docker installed on your machine

### **Before You Start**

Create a `.env` file by copying the provided template:

```bash
cp .env.template .env
```

Then fill in the following values:

| Variable             | Description                                               |
| -------------------- | --------------------------------------------------------- |
| `GEMINI_API_KEY`     | API key for Google Gemini used to summarize attachments   |
| `IMAP_SERVER`        | IMAP server address for the email account                 |
| `IMAP_PORT`          | IMAP server port (typically 993 for SSL)                  |
| `EMAIL_ACCOUNT`      | Email address of the mailbox monitored by the app         |
| `EMAIL_APP_PASSWORD` | Application password or IMAP access token for the mailbox |

### **Run in Development Mode**

```bash
docker compose up --build
```

This will start:

* the FastAPI backend,
* the PostgreSQL database, and
* the React frontend.

The app will be accessible at `http://localhost:3000`.

---

## ☁️ Deployment

Deployment is automated using **Terraform** and a few helper shell scripts.

### **Requirements**

* Terraform
* Docker
* Google Cloud CLI (`gcloud`)
* Google Cloud account with billing enabled and a configured project

---

### **Before Deployment**

Ensure your `.env` file is correctly filled in.
For simplicity, the `.env` values are passed into the deployed `docker-compose.yml`.

> Note: In a real production environment, secrets should be stored securely (e.g., via **Google Secret Manager**), not directly in environment files.

---

### **Deployment Steps**

#### 1. Configure Google Cloud CLI

Make sure you are logged in and your project is set up correctly.
> Note: This process assumes you have an SSH RSA key located at `~/.ssh/id_rsa`.

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project PROJECT_ID
gcloud services enable artifactregistry.googleapis.com
gcloud services enable compute.googleapis.com
```

Create a service account to allow the VM to pull Docker images:

```bash
gcloud iam service-accounts create vm-docker-sa \
  --display-name "VM Docker Pull Service Account"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:vm-docker-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

Make sure `PROJECT_ID` is also set in:

* `infrastructure/artifactRepository/variables.tf`
* `infrastructure/deployment/variables.tf`

---

#### 2. Create the Artifact Repository

This repository will host your Docker images.

```bash
cd infrastructure/artifactRepository
terraform init
terraform plan
terraform apply
```

---

#### 3. Create the Virtual Machine and Networking

Deploy the GCP VM and related resources (firewall rules, service account, etc.):

```bash
cd infrastructure/deployment
terraform init
terraform plan
terraform apply
```

---

#### 4. Build and Push Docker Images

During the repository setup, Terraform generates a helper script (`push_images.sh`)
that automates building and pushing Docker images to Artifact Registry.

```bash
cd infrastructure/artifactRepository
./push_images.sh
```

---

#### 5. Deploy the Application

Once the VM is up and configured (allow a few minutes for initialization),
deploy the application by providing the VM’s IP address:

```bash
cd infrastructure/deployment
./deploy VM_IP
```

After successful deployment, the application should be available at the public IP of the VM.
