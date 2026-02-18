const video = document.getElementById("video");
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

let stream = null;
let detectionInterval = null;
let lastDetected = null;
let displayTimeout = null;
let sentence = "";

// ======================
// START CAMERA
// ======================
function startCamera() {

    if (stream) return;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(mediaStream => {

            stream = mediaStream;
            video.srcObject = stream;

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

        // Only update if new detection
        if (data.text !== lastDetected) {

            lastDetected = data.text;

            const resultElement = document.getElementById("result");
            resultElement.classList.add("fade");

            resultElement.innerText = data.text;

            // Show confidence if backend sends it
            if (data.confidence) {
                document.getElementById("confidence").innerText =
                    "Confidence: " + (data.confidence * 100).toFixed(2) + "%";
            }

            // Add to sentence
            sentence += data.text + " ";
            document.getElementById("sentence").innerText = sentence;

            // Speak detected word
            speakText(data.text);

            // Pause detection for 3 seconds
            clearInterval(detectionInterval);

            displayTimeout = setTimeout(() => {
                detectionInterval = setInterval(capture, 1000);
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
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 0.9;
    window.speechSynthesis.speak(speech);
}

// Speak full sentence
function speakSentence() {
    if (!sentence) return;
    speakText(sentence);
}

// Clear sentence
function clearSentence() {
    sentence = "";
    document.getElementById("sentence").innerText = "";
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

    video.srcObject = null;
}
