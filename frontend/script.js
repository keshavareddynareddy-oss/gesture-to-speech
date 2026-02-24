const video = document.getElementById("video");
const statusText = document.getElementById("status");
const resultText = document.getElementById("result");
const confidenceText = document.getElementById("confidence");

const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

let stream = null;
let interval = null;
let currentSentence = "";

// Change if using Android Emulator
const BACKEND_URL = "http://127.0.0.1:5000/predict";
// const BACKEND_URL = "http://10.0.2.2:5000/predict";


// ==========================
// START CAMERA
// ==========================
async function startCamera() {
  try {
    if (stream) return; // prevent multiple starts

    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    statusText.innerText = "Camera On";

    video.onloadedmetadata = () => {
      video.play();
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      if (!interval) {
        interval = setInterval(captureFrame, 800);
      }
    };

  } catch (err) {
    console.error(err);
    statusText.innerText = "Camera Error";
  }
}


// ==========================
// STOP CAMERA
// ==========================
function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
    stream = null;
  }

  if (interval) {
    clearInterval(interval);
    interval = null;
  }

  statusText.innerText = "Camera Off";
}


// ==========================
// CAPTURE FRAME
// ==========================
function captureFrame() {
  if (!video.videoWidth) return;

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL("image/jpeg");

  sendToBackend(imageData);
}


// ==========================
// SEND TO BACKEND
// ==========================
async function sendToBackend(imageData) {
  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData })
    });

    const data = await response.json();

    // Show detected gesture
    confidenceText.innerText = "Detected: " + data.gesture;

    // Always display latest sentence from backend
    currentSentence = data.sentence || "";
    resultText.innerText = currentSentence;

  } catch (error) {
    console.error("Backend Error:", error);
    statusText.innerText = "Backend Error";
  }
}


// ==========================
// CLEAR SENTENCE BUTTON
// ==========================
async function clearSentence() {
  try {
    await fetch("http://127.0.0.1:5000/reset", {
      method: "POST"
    });

    currentSentence = "";
    resultText.innerText = "";

  } catch (error) {
    console.error("Reset Error:", error);
  }
}


// ==========================
// SPEAK FULL SENTENCE
// ==========================
function speakFullSentence() {
  if (!currentSentence.trim()) return;

  const utterance = new SpeechSynthesisUtterance(currentSentence);
  speechSynthesis.speak(utterance);
}