import time
import unittest
from multiprocessing import Process

import requests
import subprocess


from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

import ts_app

URL = 'http://localhost:5000'
MODEL_PATH = 'models/ts_model'
SENTENCE = ["теория вероятностей наука о случайных числах",
            "теория вероятностей наука о случайных величинах"]


class TestLocally(unittest.TestCase):

    def setUp(self):
        app = ets_app.get_app()
        self.server = Process(target=app.run, kwargs={'host': '0.0.0.0', })
        self.server.start()

    def test_server_response(self):
        r = requests.post(URL, json={'s1': SENTENCE[0], 's2': SENTENCE[1]})
        self.assertIn(b'Similarity', r.content)

    def tearDown(self):
        self.server.terminate()
        self.server.join()


class TestDocker(unittest.TestCase):
    def setUp(self) -> None:
        command = 'docker run -d -p 5000:5000 ts_model'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.container_id = output.decode("utf-8").strip()
        print('container id: ', self.container_id)
        time.sleep(1.0)

    def test_server_response(self):
        r = requests.post(URL, json={'s1': SENTENCE[0], 's2': SENTENCE[1]})
        self.assertIn(b'Similarity', r.content)

    def tearDown(self) -> None:
        command = f'docker kill {self.container_id}'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        print(output, ' killed')


class TestModel(unittest.TestCase):

    def test_model_loading(self):
        model = SentenceTransformer(MODEL_PATH)

        # Sentences are encoded by calling model.encode()
        embs = model.encode(SENTENCE)

        cs = embs[0] @ embs[1].T / (norm(embs[0]) * norm(embs[1]))
        self.assertGreater(cs, 0.9)


if __name__ == '__main__':
    unittest.main()
