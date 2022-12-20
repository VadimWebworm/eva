import asyncio
import json
import wave
import websockets

KALDI_URI = 'ws://localhost:2700'


async def async_wav_to_text(wav_path):
    async with websockets.connect(KALDI_URI) as websocket:

        wf = wave.open(wav_path, "rb")
        print(wav_path, ' opened')
        await websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
        buffer_size = int(wf.getframerate() * 0.5) # 0.2 seconds of audio
        while True:
            data = wf.readframes(buffer_size)

            if len(data) == 0:
                break

            await websocket.send(data)
            result = await websocket.recv()

        await websocket.send('{"eof" : 1}')
        return result


def wav_to_text(wav_path):
    res = asyncio.run(async_wav_to_text(wav_path))
    jres = json.loads(res)
    return jres['partial']
