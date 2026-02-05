const video = document.getElementById("video");
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

let detectionInterval = null;

// START CAMERA
function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;

            video.onloadedmetadata = () => {
                video.play();

                // Set canvas size once
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                console.log("Camera started");

                // Start continuous capture
                if (!detectionInterval) {
                    detectionInterval = setInterval(capture, 1000); // 1 sec
                }
            };
        })
        .catch(err => {
            console.error("Camera error:", err);
            alert("Camera permission denied or not available");
        });
}

// CAPTURE FRAME AND SEND TO BACKEND
function capture() {
    if (!video.srcObject || video.videoWidth === 0) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL("image/jpeg");

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(res => res.json())
    .then(data => {
        // Show result instantly
        document.getElementById("result").innerText = data.text;
    })
    .catch(err => {
        console.error("Fetch error:", err);
    });
}

// OPTIONAL: STOP CAMERA BUTTON
function stopCamera() {
    const stream = video.srcObject;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    video.srcObject = null;
    clearInterval(detectionInterval);
    detectionInterval = null;
}
