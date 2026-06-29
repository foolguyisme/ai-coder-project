const API_BASE = "http://127.0.0.1:8000";

const promptEl = document.getElementById("prompt");
const outputEl = document.getElementById("output");
const statusEl = document.getElementById("status");
const generateBtn = document.getElementById("generate-btn");

async function generateCode() {
  const prompt = promptEl.value.trim();
  if (!prompt) {
    statusEl.textContent = "Please enter a prompt.";
    return;
  }

  generateBtn.disabled = true;
  statusEl.textContent = "Generating...";
  outputEl.textContent = "";

  try {
    const response = await fetch(`${API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    const data = await response.json();
    outputEl.textContent = data.output;
    statusEl.textContent = "Done.";
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  } finally {
    generateBtn.disabled = false;
  }
}

generateBtn.addEventListener("click", generateCode);

promptEl.addEventListener("keydown", (event) => {
  if (event.ctrlKey && event.key === "Enter") {
    generateCode();
  }
});
