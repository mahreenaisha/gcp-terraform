from fastapi import FastAPI
import re
from git import Repo
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow your frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔧 Adjust this to your Terraform repo path
TERRAFORM_PATH = r"C:\Users\Mahreen Aisha\Desktop\Coding\gcp-terraform"
MAIN_TF_PATH = os.path.join(TERRAFORM_PATH, "main.tf")

# ✅ GitHub settings
GITHUB_REMOTE = "origin"
BRANCH_NAME = "main"

repo = Repo(TERRAFORM_PATH)

# ----------------------- 🌐 BUCKET FUNCTIONS ----------------------- #

def get_next_bucket_index():
    with open(MAIN_TF_PATH, "r") as f:
        content = f.read()
    matches = re.findall(r"my-bucket-79-(\d+)", content)
    return max(map(int, matches)) + 1 if matches else 1


def get_latest_bucket_index():
    with open(MAIN_TF_PATH, "r") as f:
        content = f.read()
    matches = re.findall(r"my-bucket-79-(\d+)", content)
    return max(map(int, matches)) if matches else None


@app.post("/create-bucket")
def create_bucket():
    index = get_next_bucket_index()
    resource_name = f"my-bucket-79-{index}"
    bucket_name = f"storage-bucket-79-{index}"

    new_block = f"""
resource "google_storage_bucket" "{resource_name}" {{
  name                     = "{bucket_name}"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}}
"""
    with open(MAIN_TF_PATH, "a") as f:
        f.write("\n" + new_block)

    repo.git.add(MAIN_TF_PATH)
    repo.index.commit(f"Add {resource_name}")
    repo.remote(GITHUB_REMOTE).push(BRANCH_NAME)

    return {"message": f"{bucket_name} created and pushed to GitHub"}


@app.delete("/delete-bucket")
def delete_bucket():
    index = get_latest_bucket_index()
    if not index:
        return {"message": "No buckets to delete."}

    resource_name = f"my-bucket-79-{index}"

    with open(MAIN_TF_PATH, "r") as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    brace_count = 0

    for line in lines:
        if f'resource "google_storage_bucket" "{resource_name}"' in line:
            skip = True
            brace_count = 0

        if skip:
            brace_count += line.count("{") - line.count("}")
            if brace_count <= 0 and line.strip().endswith("}"):
                skip = False
            continue

        if not skip:
            new_lines.append(line)

    with open(MAIN_TF_PATH, "w") as f:
        f.writelines(new_lines)

    repo.git.add(MAIN_TF_PATH)
    repo.index.commit(f"Delete {resource_name}")
    repo.remote(GITHUB_REMOTE).push(BRANCH_NAME)

    return {"message": f"{resource_name} deleted and changes pushed to GitHub"}


# ----------------------- 💻 VM FUNCTIONS ----------------------- #

def get_next_vm_index():
    with open(MAIN_TF_PATH, "r") as f:
        content = f.read()
    matches = re.findall(r"my-vm-79-(\d+)", content)
    return max(map(int, matches)) + 1 if matches else 1


def get_latest_vm_index():
    with open(MAIN_TF_PATH, "r") as f:
        content = f.read()
    matches = re.findall(r"my-vm-79-(\d+)", content)
    return max(map(int, matches)) if matches else None


@app.post("/create-vm")
def create_vm():
    index = get_next_vm_index()
    resource_name = f"my-vm-79-{index}"
    vm_name = f"vm-79-{index}"

    new_block = f"""
resource "google_compute_instance" "{resource_name}" {{
  name         = "{vm_name}"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {{
    initialize_params {{
      image = "debian-cloud/debian-11"
      labels = {{
        my_label = "value"
      }}
    }}
  }}

  network_interface {{
    network = "default"
  }}

  metadata_startup_script = "echo hi > /test.txt"
}}
"""

    with open(MAIN_TF_PATH, "a") as f:
        f.write("\n" + new_block)

    repo.git.add(MAIN_TF_PATH)
    repo.index.commit(f"Add {resource_name}")
    repo.remote(GITHUB_REMOTE).push(BRANCH_NAME)

    return {"message": f"{vm_name} created and pushed to GitHub"}


@app.delete("/delete-vm")
def delete_vm():
    index = get_latest_vm_index()
    if not index:
        return {"message": "No VMs to delete."}

    resource_name = f"my-vm-79-{index}"

    with open(MAIN_TF_PATH, "r") as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    brace_count = 0

    for line in lines:
        if f'resource "google_compute_instance" "{resource_name}"' in line:
            skip = True
            brace_count = 0

        if skip:
            brace_count += line.count("{") - line.count("}")
            if brace_count <= 0 and line.strip().endswith("}"):
                skip = False
            continue

        if not skip:
            new_lines.append(line)

    with open(MAIN_TF_PATH, "w") as f:
        f.writelines(new_lines)

    repo.git.add(MAIN_TF_PATH)
    repo.index.commit(f"Delete {resource_name}")
    repo.remote(GITHUB_REMOTE).push(BRANCH_NAME)

    return {"message": f"{resource_name} deleted and changes pushed to GitHub"}
