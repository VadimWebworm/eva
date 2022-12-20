URL = window.URL || window.webkitURL;

let gumStream;
let rec;
let input;

let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext

let recordButton = document.getElementById("start");
let stopButton = document.querySelector('#stop');
let pauseButton = document.querySelector('#pause');

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

var question_id = document.getElementById("question_id").value

function startRecording() {
    console.log("recordButton clicked");

    let constraints = { audio: true, video: false }

    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false

    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input, { numChannels: 1 })
        rec.record()
        console.log("Recording started");

    }).catch(function (err) {
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function pauseRecording() {
    console.log("pauseButton clicked rec.recording=", rec.recording);
    if (rec.recording) {
        //pause
        rec.stop();
        pauseButton.innerHTML = "GO!";
    } else {
        //resume
        rec.record()
        pauseButton.innerHTML = "Пауза";

    }
}

function stopRecording() {
    console.log("stopButton clicked");

    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    pauseButton.innerHTML = "Пауза";
    rec.stop();

    gumStream.getAudioTracks()[0].stop();
    rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
    let xhr = new XMLHttpRequest();
    xhr.onload = function (e) {
        if (this.readyState === 4) {
            console.log("Server returned: ", e.target.responseText);
        }
    };
    let fd = new FormData();
    fd.append('voice', blob);

    fetch("http://127.0.0.1:8000/api/1/wav/" + question_id, {
    credentials: 'include',
    mode: 'same-origin',
    headers: {
      'X-CSRFToken': document.recorder_form.csrfmiddlewaretoken.value
    },
    method: "POST",
    body: fd
    });

}
