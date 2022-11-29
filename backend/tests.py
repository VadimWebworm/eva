import asyncio
import json

from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.test import TestCase, Client

from backend.kaldi_utils import wav_to_text
from ui.models import Quiz, Question
import wave

TEST_FILE_PATH = 'wavs/test_1.wav'
TEST_FILE_FRAME_RATE = 44100


class BackendTestCase(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='Теория вероятностей', desc='Тест по основам теории вероятностей')
        Question.objects.create(content='Дайте определение теории вероятностей', quiz=quiz)
        self.client = Client()
        self.client.login(username='test', password='secret')

    def test_wav_post(self):
        with open(TEST_FILE_PATH, 'rb') as fn:
            in_memory_file = InMemoryUploadedFile(fn, 'voice', 'voice', 'audio/wav', None, None)
            response = self.client.post('/api/1/wav/1', {'voice': in_memory_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"Status": "processing"}')


class KaldiTestCase(TestCase):
    def test_wav_frame_rate(self):
        wf = wave.open(TEST_FILE_PATH, 'rb')
        frame_rate = wf.getframerate()
        self.assertEqual(frame_rate, TEST_FILE_FRAME_RATE)

    def test_kaldi(self):
        """ Kaldi server must be active:
         $ docker run -d -p 2700:2700 alphacep/kaldi-ru:latest
         """
        result = wav_to_text(TEST_FILE_PATH)
        self.assertTrue('теория вероятности это раздел' in result)
