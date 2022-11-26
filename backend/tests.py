from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.test import TestCase, Client

from ui.models import Quiz, Question


class BackendTestCase(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='Теория вероятностей', desc='Тест по основам теории вероятностей')
        Question.objects.create(content='Дайте определение теории вероятностей', quiz=quiz)

    def test_wav_processing(self):
        c = Client()
        c.login(username='test', password='secret')
        with open('wavs/test_1.wav', 'rb') as fn:
            in_memory_file = InMemoryUploadedFile(fn, 'voice', 'voice', 'audio/wav', None, None)
            response = c.post('/api/1/wav/1', {'voice': in_memory_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"Status": "processing"}')
