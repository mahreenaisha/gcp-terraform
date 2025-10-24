//creating storage bucket
resource "google_storage_bucket" "my-bucket" {
  name          = "vit-project-githubdemo-bucket"
  location      = "US"
  force_destroy = true

  public_access_prevention = "enforced"
}