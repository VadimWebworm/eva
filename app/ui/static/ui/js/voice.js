URL = window.URL || window.webkitURL;

let gumStream;
let rec;
let input;

let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext

const recordButton = document.getElementById("start");
const stopButton = document.querySelector('#stop');
const soundClips = document.querySelector('.sound-clips');

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
        if (document.querySelector('.clip')) {
            document.querySelector('.clip').remove();
        }
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

    if (!document.querySelector('.clip')) {
        // clipName = document.getElementById('question_id').value;
        const clipContainer = document.createElement('article');
        const audio = document.createElement('audio');

        clipContainer.classList.add('clip');
        audio.setAttribute('controls', '');

        clipContainer.appendChild(audio);
        soundClips.appendChild(clipContainer);
        const audioURL = window.URL.createObjectURL(blob);
        audio.src = audioURL;
    }
    var endpoint = "/api/1/wav/" + question_id.value
    console.log("Send POST to endpoint: " + endpoint)
    fetch(endpoint, {
        credentials: 'include',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': document.quizInnerForm.csrfmiddlewaretoken.value
        },
        method: "POST",
        body: fd
    });

}
