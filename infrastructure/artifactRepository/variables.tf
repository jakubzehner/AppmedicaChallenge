variable "region" {
  description = "GCP region (Note: in free tier only us reagions are available)"
  default     = "us-east1"
}

variable "project_id" {
  description = "GCP project ID"
  default     = "appmedica-476409"
}

variable "repository_id" {
  description = "Repository name for Docker images"
  default     = "appmedica-docker-repo"
}

locals {
  envs = { for tuple in regexall("(.*)=(.*)", file("../../.env")) : tuple[0] => sensitive(tuple[1]) }
}
