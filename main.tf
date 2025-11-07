# You can tell Terraform to save its state in a Google Cloud Storage bucket.
# That way, it always remembers what it created — even when GitHub runs in a new environment.
terraform {
  backend "gcs" {
    bucket = "state-bucket-79-1"
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
resource "google_storage_bucket" "my-bucket-79-1" {
  name                     = "storage-bucket-79-1"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}




//creating storage bucket 2
resource "google_storage_bucket" "my-bucket-79-2" {
  name                     = "storage-bucket-79-2"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}
