const video = document.getElementById("video");

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            console.log("Camera started");
        })
        .catch(err => {
            console.error("Camera error:", err);
            alert("Camera error: " + err.name);
        });
}

function capture() {
    if (!video.srcObject) {
        alert("Camera not started yet");
        return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL("image/jpeg");

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            "Detected Text: " + data.text;
    })
    .catch(err => {
        console.error("Fetch error:", err);
    });
}
