// The browser only collects the expression; the server calculates it
// (POST /api/calc), so the logic lives in one place and is covered by tests.
const display = document.getElementById("display");
let expression = "";

function show(text) {
  display.textContent = text === "" ? "0" : text;
}

async function calculate() {
  if (expression === "") return;
  const response = await fetch("api/calc", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression }),
  });
  const data = await response.json();
  if (response.ok) {
    expression = String(data.result);
    show(expression);
  } else {
    expression = "";
    show(data.error);
  }
}

document.querySelectorAll("button[data-key]").forEach((button) => {
  button.addEventListener("click", () => {
    const key = button.dataset.key;
    if (key === "C") {
      expression = "";
      show(expression);
    } else if (key === "=") {
      calculate();
    } else {
      expression += key;
      show(expression);
    }
  });
});
