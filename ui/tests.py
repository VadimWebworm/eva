from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory

from ui import views
from ui.models import Quiz, Question


class UiTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='testb@ya.ru', password='secret')

        quiz = Quiz.objects.create(name='Теория вероятностей', desc='Тест по основам теории вероятностей')
        Question.objects.create(content='Дайте определение теории вероятностей', quiz=quiz)

    def test_database(self):
        quiz = Quiz.objects.get(name='Теория вероятностей')
        question = Question.objects.get(content='Дайте определение теории вероятностей')
        self.assertEqual(quiz.desc, 'Тест по основам теории вероятностей')
        self.assertEqual(question.content, 'Дайте определение теории вероятностей')

    def test_unauthorized(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Для работы с Евой нужно авторизоваться')

    def test_index(self):
        client = Client()
        client.post('/login/', {'username': 'test', 'password': 'secret'})
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Теория вероятностей'.encode("ascii", "ignore"))
        self.assertContains(response, 'Дайте определение теории вероятностей'.encode("ascii", "ignore"))

    def test_quiz(self):
        request = self.factory.get('')
        request.user = self.user
        response = views.quiz(request, 1, 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Запись'.encode("ascii", "ignore"))
