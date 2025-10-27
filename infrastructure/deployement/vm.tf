resource "google_compute_instance" "app_vm" {
  name         = "app-vm"
  machine_type = "e2-micro"
  zone         = var.zone

  service_account {
    email  = "vm-docker-sa@${var.project_id}.iam.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 10
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.vm_ip.address
    }
  }

  metadata = {
    ssh-keys = "${var.ssh_user}:${file(var.public_key_path)}"
  }

  tags = ["http-server", "ssh-server"]

  metadata_startup_script = <<-EOF
    #!/bin/bash
    DEBIAN_FRONTEND=noninteractive
    apt update -y
    echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
    echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections
    apt install -y ca-certificates curl gnupg lsb-release iptables-persistent

    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt update -y
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    systemctl enable docker
    systemctl start docker

    iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000
    netfilter-persistent save

    gcloud auth configure-docker ${var.region}-docker.pkg.dev --quiet
  EOF
}


output "vm_ip" {
  value = google_compute_address.vm_ip.address
}

output "ssh_command" {
  value = "ssh ${var.ssh_user}@${google_compute_address.vm_ip.address} -i ${var.private_key_path}"
}

output "deploy_script" {
  value = "To deploy app run: ./deploy.sh ${google_compute_address.vm_ip.address}"
}
