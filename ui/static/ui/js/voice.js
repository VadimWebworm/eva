URL = window.URL || window.webkitURL;

let gumStream;
let rec;
let input;

let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext

let recordButton = document.getElementById("start");
let stopButton = document.querySelector('#stop');

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);


function startRecording() {
    console.log("recordButton clicked");
    let constraints = { audio: true, video: false }
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input, { numChannels: 1 })
        rec.record()
        console.log("Recording started");

    })
}

function stopRecording() {
    console.log("stopButton clicked");
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
