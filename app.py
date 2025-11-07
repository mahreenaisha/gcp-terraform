from fastapi import FastAPI
import subprocess
from git import Repo
import os

app = FastAPI()

# Path to your Terraform repo
TERRAFORM_PATH = r"C:\Users\Mahreen Aisha\Desktop\Coding\gcp-terraform"
repo = Repo(TERRAFORM_PATH)

# Terraform resource templates
VM_RESOURCE = """
resource "google_compute_instance" "vm_from_api" {
  name         = "vm-from-api"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
"""

BUCKET_RESOURCE = """
resource "google_storage_bucket" "bucket_from_api" {
  name     = "my-bucket-from-api"
  location = "US"
}
"""

# Helper functions
def modify_tf_file(add_code=None, remove_key=None):
    tf_file = os.path.join(TERRAFORM_PATH, "main.tf")

    with open(tf_file, "r") as f:
        lines = f.readlines()

    if remove_key:
        new_lines = []
        skip = False
        for line in lines:
            if remove_key in line:
                skip = True
            if not skip:
                new_lines.append(line)
            if skip and line.strip() == "}":
                skip = False
        lines = new_lines

    if add_code:
        lines.append("\n" + add_code + "\n")

    with open(tf_file, "w") as f:
        f.writelines(lines)

def push_to_github(commit_message):
    repo.git.add(A=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()

# API routes
@app.post("/create-vm")
def create_vm():
    modify_tf_file(add_code=VM_RESOURCE)
    push_to_github("Added VM resource via API")
    return {"status": "VM resource added and pushed to GitHub"}

@app.post("/delete-vm")
def delete_vm():
    modify_tf_file(remove_key="resource \"google_compute_instance\" \"vm_from_api\"")
    push_to_github("Deleted VM resource via API")
    return {"status": "VM resource deleted and pushed to GitHub"}

@app.post("/create-bucket")
def create_bucket():
    modify_tf_file(add_code=BUCKET_RESOURCE)
    push_to_github("Added Bucket resource via API")
    return {"status": "Bucket resource added and pushed to GitHub"}

@app.post("/delete-bucket")
def delete_bucket():
    modify_tf_file(remove_key="resource \"google_storage_bucket\" \"bucket_from_api\"")
    push_to_github("Deleted Bucket resource via API")
    return {"status": "Bucket resource deleted and pushed to GitHub"}
