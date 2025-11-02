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




