function startRecording() {
  fetch("/start_recording", { method: "POST" })
    .then((res) => res.json())
    .then(() => {
      document.getElementById("start_btn").disabled = true;
      document.getElementById("stop_btn").disabled = false;
    });
}

function stopRecording() {
  fetch("/stop_recording", { method: "POST" })
    .then((res) => res.json())
    .then(() => {
      document.getElementById("start_btn").disabled = false;
      document.getElementById("stop_btn").disabled = true;
    });
}

setInterval(() => {
  const now = new Date();
  document.getElementById("feed_time").textContent = now.toLocaleTimeString();
}, 1000);

document.getElementById("sos_btn").addEventListener("click", () => {
  fetch("/sos_alert", { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      console.log(data.status); // Optional: Log the response
    });
});

document.getElementById("toggle_mode").addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  document.body.classList.toggle("light-mode");
});
