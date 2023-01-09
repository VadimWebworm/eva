import json
import wave
import sys

import requests
from vosk import Model, KaldiRecognizer
URL = 'http://127.0.0.1:5000'


def test_vosk():
    wf = wave.open('2_date.wav', "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    model = Model(lang="ru")

    # You can also specify the possible word or phrase list as JSON list,
    # the order doesn't have to be strict
    rec = KaldiRecognizer(
        model,
        wf.getframerate()
    )

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())

    print(rec.FinalResult())


def test_app():
    files = {'wav_file': open('wavs/2_date.wav', 'rb')}

    r = requests.post(URL, files=files)
    print(r.encoding)
    j_str = json.loads(r.text)
    print(json.loads(j_str)['text'])


test_app()
