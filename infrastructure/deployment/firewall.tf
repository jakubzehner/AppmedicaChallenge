resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  target_tags   = ["http-server"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_http_server" {
  name    = "allow-http-server"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }

  target_tags   = ["http-server"]
  source_ranges = ["0.0.0.0/0"]
}


resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags   = ["ssh-server"]
  source_ranges = ["0.0.0.0/0"]
}
