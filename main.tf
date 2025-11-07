# You can tell Terraform to save its state in a Google Cloud Storage bucket.
# That way, it always remembers what it created — even when GitHub runs in a new environment.
terraform {
  backend "gcs" {
    bucket = "vit-project-terraform-state"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.8.0"
    }
  }
}

provider "google" {
  project = "terraform-project-476110"
  region  = "us-central1"
}

//creating storage bucket
resource "google_storage_bucket" "my-bucket" {
  name                     = "vit-project-githubdemo-bucket"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}

//creating compute engine instance
resource "google_compute_instance" "vm-from-terraform" {
  name = "vm-from-terraform"

  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = {
        my_label = "value"
      }
    }
  }

  network_interface {
    network = "default"
  }

  metadata_startup_script = "echo hi > /test.txt"
}

