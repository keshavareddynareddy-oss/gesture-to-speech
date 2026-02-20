const video = document.getElementById("video");
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

let stream = null;
let detectionInterval = null;
let lastDetected = null;
let displayTimeout = null;

// ======================
// START CAMERA
// ======================
function startCamera() {

    if (stream) return;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(mediaStream => {

            stream = mediaStream;
            video.srcObject = stream;

            document.getElementById("status").innerText = "Camera Active";
            document.getElementById("status").style.background = "green";

            video.onloadedmetadata = () => {
                video.play();

                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                if (!detectionInterval) {
                    detectionInterval = setInterval(capture, 1000);
                }
            };
        })
        .catch(err => {
            console.error("Camera error:", err);
            alert("Camera permission denied or not available");
        });
}

// ======================
// CAPTURE FRAME
// ======================
function capture() {

    if (!stream || video.videoWidth === 0) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL("image/jpeg");

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
    })
    .then(res => res.json())
    .then(data => {

        if (!data.text) return;

        const resultElement = document.getElementById("result");

        if (data.text !== lastDetected) {

            lastDetected = data.text;

            // Stop previous timeout
            clearTimeout(displayTimeout);

            // Show gesture
            resultElement.innerText = data.text;
            resultElement.classList.add("show");

            // Show confidence if provided
            if (data.confidence) {
                document.getElementById("confidence").innerText =
                    "Confidence: " + (data.confidence * 100).toFixed(2) + "%";
            }

            // Speak detected word
            speakText(data.text);

            // Hide after 3 seconds if no new gesture
            displayTimeout = setTimeout(() => {
                resultElement.classList.remove("show");
                resultElement.innerText = "";
                document.getElementById("confidence").innerText = "";
                lastDetected = null;
            }, 3000);
        }

    })
    .catch(err => {
        console.error("Fetch error:", err);
    });
}

// ======================
// TEXT TO SPEECH
// ======================
function speakText(text) {

    const wave = document.getElementById("wave");
    wave.style.visibility = "visible";

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 0.9;

    speech.onend = () => {
        wave.style.visibility = "hidden";
    };

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);
}

// ======================
// STOP CAMERA
// ======================
function stopCamera() {

    if (detectionInterval) {
        clearInterval(detectionInterval);
        detectionInterval = null;
    }

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    clearTimeout(displayTimeout);

    document.getElementById("status").innerText = "Camera Off";
    document.getElementById("status").style.background = "red";

    video.srcObject = null;

    // Clear display
    document.getElementById("result").innerText = "";
    document.getElementById("confidence").innerText = "";
    lastDetected = null;
}