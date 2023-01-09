import wave

from flask import Flask, jsonify, request, g
from vosk import Model, KaldiRecognizer

FRAME_RATE = 44100


def get_app():
    vosk_app = Flask(__name__)
    vosk_app.config['MODEL_PATH'] = 'models/vosk-model-small-ru-0.22'
    vosk_app.config['JSON_AS_ASCII'] = False

    def get_recognizer():
        if 'recognizer' not in g:
            g.model = Model(vosk_app.config['MODEL_PATH'])
            g.recognizer = KaldiRecognizer(
                g.model,
                FRAME_RATE)
        return g.recognizer

    @vosk_app.route("/", methods=['POST'])
    def do_prediction():
        wav_file = request.files['wav_file'].stream
        if wav_file:
            recognizer = get_recognizer()
            wf = wave.open(wav_file, "rb")

            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                return jsonify({'result': 'Audio file must be WAV format mono PCM'})

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    print(recognizer.Result())
                else:
                    print(recognizer.PartialResult())

            result = recognizer.FinalResult()
            return jsonify(result)

    return vosk_app


if __name__ == "__main__":
    app = get_app()
    app.run(host='0.0.0.0', port='5005')
