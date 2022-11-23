from django.http import JsonResponse
from django.views import View
from ui.models import Quiz

import logging

logging.basicConfig(filename='logs/logs.log', level=logging.INFO)


def save_wav_to_disk(request):
    filename = 'Username_questname_date.wav'
    logging.info(f'{filename} saved to disk')
    return b'wav_blob'


def get_text_from_wav(wav_object):
    """ Send wav data to VOSK server, get the text response"""
    logging.info('Send wav data to VOSK server, get the text response')
    return 'Some text'


def get_score_from_text(user_answer):
    """ Send text data to NLP server, get the answer score """
    logging.info('Send text data to NLP server, get the answer score')
    return 0.5


class ApiView(View):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = {
            'questions': list(quiz.get_questions().values(), ),
        }
        return JsonResponse(questions, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        wav_object = save_wav_to_disk(request)
        user_answer = get_text_from_wav(wav_object)
        score = get_score_from_text(user_answer)
        return f'{int(round(10 * score))}'
