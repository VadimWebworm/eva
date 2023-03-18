import subprocess
import time

import requests
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, Client

from backend.celery_tasks import wav_to_text
from ui.models import Quiz, Question
import wave

TEST_FILE_PATH = 'mediafiles/test_1.wav'
TEST_FILE_FRAME_RATE = 44100
ASR_URL = 'http://localhost:5005'


class BackendTestCase(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='Теория вероятностей', desc='Тест по основам теории вероятностей')
        Question.objects.create(content='Дайте определение теории вероятностей', quiz=quiz)
        user = User.objects.create(username='test_user')
        user.set_password('secret')
        user.save()
        self.client = Client()
        self.client.login(username='test_user', password='secret')

    def test_wav_post(self):
        with open(TEST_FILE_PATH, 'rb') as fn:
            in_memory_file = InMemoryUploadedFile(fn, 'voice', 'voice', 'audio/wav', None, None)
            response = self.client.post('/api/1/wav/1', {'voice': in_memory_file})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'result', response.content)


class KaldiTestCase(TestCase):
    def test_wav_frame_rate(self):
        wf = wave.open(TEST_FILE_PATH, 'rb')
        frame_rate = wf.getframerate()
        self.assertEqual(frame_rate, TEST_FILE_FRAME_RATE)


class AsrDockerTestCase(TestCase):
    def setUp(self) -> None:
        command = 'docker run -d -p 5005:5005 eva-asr'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.container_id = output.decode("utf-8").strip()
        print('container id: ', self.container_id)
        time.sleep(1.0)

    def test_server_response(self):
        text = wav_to_text('../mediafiles/test_1.wav', asr_url=ASR_URL)
        print(text)
        self.assertIn('теория вероятности это раздел математики', text)

    def tearDown(self) -> None:
        command = f'docker kill {self.container_id}'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output, ' killed')
