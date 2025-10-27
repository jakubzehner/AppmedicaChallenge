variable "region" {
  description = "GCP region (Note: in free tier only us reagions are available)"
  default     = "us-east1"
}

variable "zone" {
  description = "GCP zone (Note: in free tier only us zones are available)"
  default     = "us-east1-b"
}

variable "project_id" {
  description = "GCP project ID"
  default     = "appmedica-476409"
}

variable "ssh_user" {
  default     = "debian"
  description = "Username for SSH"
}

variable "public_key_path" {
  description = "Path to your SSH public key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "private_key_path" {
  description = "Path to your SSH private key"
  default     = "~/.ssh/id_rsa"
}
