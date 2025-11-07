// const API_URL = "http://127.0.0.1:8000";

// async function createBucket() {
//   updateStatus("Creating bucket...");
//   try {
//     const res = await fetch(`${API_URL}/create-bucket`, { method: "POST" });
//     const data = await res.json();
//     updateStatus("✅ " + data.message);
//   } catch (err) {
//     updateStatus("❌ Error: " + err.message);
//   }
// }

// async function deleteBucket() {
//   updateStatus("Deleting latest bucket...");
//   try {
//     const res = await fetch(`${API_URL}/delete-bucket`, { method: "DELETE" });
//     const data = await res.json();
//     updateStatus("✅ " + data.message);
//   } catch (err) {
//     updateStatus("❌ Error: " + err.message);
//   }
// }

// async function createVM() {
//   updateStatus("Creating VM...");
//   try {
//     const res = await fetch(`${API_URL}/create-vm`, { method: "POST" });
//     const data = await res.json();
//     updateStatus("✅ " + data.message);
//   } catch (err) {
//     updateStatus("❌ Error: " + err.message);
//   }
// }

// async function deleteVM() {
//   updateStatus("Deleting latest VM...");
//   try {
//     const res = await fetch(`${API_URL}/delete-vm`, { method: "DELETE" });
//     const data = await res.json();
//     updateStatus("✅ " + data.message);
//   } catch (err) {
//     updateStatus("❌ Error: " + err.message);
//   }
// }

// function updateStatus(message) {
//   document.getElementById("status").textContent = message;
// }

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
