const statusBox = document.getElementById("status");
const API_BASE = "http://127.0.0.1:8000";

async function callAPI(endpoint, method) {
  try {
    statusBox.textContent = "Processing...";
    const response = await fetch(`${API_BASE}${endpoint}`, { method });
    const data = await response.json();
    statusBox.textContent = data.message || "Done!";
  } catch (error) {
    statusBox.textContent = "Error: " + error.message;
  }
}

// Prevent page flash/reload by avoiding form submissions
document.getElementById("createBucket").addEventListener("click", () => callAPI("/create-bucket", "POST"));
document.getElementById("deleteBucket").addEventListener("click", () => callAPI("/delete-bucket", "DELETE"));
document.getElementById("createVM").addEventListener("click", () => callAPI("/create-vm", "POST"));
document.getElementById("deleteVM").addEventListener("click", () => callAPI("/delete-vm", "DELETE"));
