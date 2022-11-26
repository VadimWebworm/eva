import json

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ui.models import Quiz

import os
import logging

logging.basicConfig(filename='logs/logs.log', level=logging.INFO)


def get_user_dir(user_name):
    user_dir = f'wavs/{user_name}'
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    return user_dir


def save_wav_to_disk(request, quest_id):
    user_name = str(request.user)
    user_dir = get_user_dir(user_name)
    filename = f'{user_dir}/{quest_id}_date.wav'
    file_in_memory = request.FILES['voice']
    blob = file_in_memory.read()
    with open(filename, 'wb') as fn:
        fn.write(blob)
    return blob


def get_text_from_wav(wav_object):
    """ Send wav data to VOSK server, get the text response"""
    logging.info('Send wav data to VOSK server, get the text response')
    return 'Some text'


def get_score_from_text(user_answer):
    """ Send text data to NLP server, get the answer score """
    logging.info('Send text data to NLP server, get the answer score')
    return 0.5


def get_quiz_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = {
        'questions': list(quiz.get_questions().values(), ),
    }
    return JsonResponse(questions, safe=False, json_dumps_params={'ensure_ascii': False})


@require_POST
def process_wav(request, quiz_id, quest_id):
    wav_blob = save_wav_to_disk(request, quest_id)
    # user_answer = get_text_from_wav(wav_blob)
    # score = get_score_from_text(user_answer)
    return JsonResponse({'Status': 'processing'})
