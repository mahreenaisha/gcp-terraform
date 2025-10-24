//provider block 
terraform {
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
  name          = "vit-project-githubdemo-bucket"
  location      = "US"
  force_destroy = true
  public_access_prevention = "enforced"
}

//creating second bucket
resource "google_storage_bucket" "my-second-bucket" {
  name                     = "vit-project-githubdemo-bucket-2"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}
