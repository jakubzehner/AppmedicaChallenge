terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_address" "vm_ip" {
  name   = "app-static-ip"
  region = var.region
}
