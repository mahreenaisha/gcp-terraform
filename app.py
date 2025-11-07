from fastapi import FastAPI
import re
from git import Repo
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow your frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://127.0.0.1:5500"] if using VSCode Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔧 Adjust this to the path of your local repo
TERRAFORM_PATH = r"C:\Users\Mahreen Aisha\Desktop\Coding\gcp-terraform"
MAIN_TF_PATH = os.path.join(TERRAFORM_PATH, "main.tf")

# ✅ Your GitHub repo
GITHUB_REMOTE = "origin"
BRANCH_NAME = "main"

repo = Repo(TERRAFORM_PATH)


# 🧮 Helper — find the next bucket index
def get_next_bucket_index():
    with open(MAIN_TF_PATH, "r") as f:
        content = f.read()

    matches = re.findall(r"my-bucket-79-(\d+)", content)
    if not matches:
        return 1
    return max(map(int, matches)) + 1


# 🧩 Helper — get latest bucket index
def get_latest_bucket_index():
    with open(MAIN_TF_PATH, "r") as f:
        content = f.read()

    matches = re.findall(r"my-bucket-79-(\d+)", content)
    if not matches:
        return None
    return max(map(int, matches))


# 🧠 Create a new bucket block in Terraform
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

    # Append the new resource block
    with open(MAIN_TF_PATH, "a") as f:
        f.write("\n" + new_block)

    # Git add, commit, push
    repo.git.add(MAIN_TF_PATH)
    repo.index.commit(f"Add {resource_name}")
    repo.remote(GITHUB_REMOTE).push(BRANCH_NAME)

    return {"message": f"{bucket_name} created and pushed to GitHub"}


# 🧹 Delete the latest bucket block
@app.delete("/delete-bucket")
def delete_bucket():
    index = get_latest_bucket_index()
    if not index:
        return {"message": "No buckets to delete."}

    resource_name = f"my-bucket-79-{index}"

    with open(MAIN_TF_PATH, "r") as f:
        lines = f.readlines()

    # Remove lines that belong to the latest bucket block
    new_lines = []
    skip = False
    for line in lines:
        if f'resource "google_storage_bucket" "{resource_name}"' in line:
            skip = True
        if not skip:
            new_lines.append(line)
        if skip and line.strip() == "}":
            skip = False

    # Write updated file
    with open(MAIN_TF_PATH, "w") as f:
        f.writelines(new_lines)

    # Git add, commit, push
    repo.git.add(MAIN_TF_PATH)
    repo.index.commit(f"Delete {resource_name}")
    repo.remote(GITHUB_REMOTE).push(BRANCH_NAME)

    return {"message": f"{resource_name} deleted and changes pushed to GitHub"}
