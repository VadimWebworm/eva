import json
import os
import logging

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from ui.models import Answer, Question

logging.basicConfig(filename='logs/logs.log', level=logging.INFO)
ASR_URL = 'http://asr:5005'
TS_URL = 'http://ts:5000'


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
    return filename


def wav_to_text(wav_filename):
    pass


def text_to_score(user_answer, true_answer):
    """ Send text data to NLP server, get the answer score """
    r = requests.post(TS_URL, json={'s1': user_answer, 's2': true_answer})
    j_res = json.loads(r.text)
    score = float(j_res['Similarity'])

    logging.info(f'User answer: {user_answer} , Score: {score}')
    return score


@require_POST
@login_required
def process_wav(request, quiz_id, quest_id):
    wav_filename = save_wav_to_disk(request, quest_id)
    question = Question.objects.get(id=quest_id)
    if os.getenv('STUB_EVA_SERVICES'):
        user_answer = 'Сервис распознавания голоса отключен'
        score = 0.01
    else:
        file_wrapper = {'wav_file': open(wav_filename, 'rb')}
        r = requests.post(ASR_URL, files=file_wrapper)
        j_str = json.loads(r.text)
        user_answer = json.loads(j_str)['text']
        true_answer = question.true_answer
        score = text_to_score(user_answer, true_answer)

    answer = Answer(
        content=user_answer,
        question=question,
        user=request.user,
        wav=wav_filename,
        date_time=timezone.now(),
        score=score
    )
    answer.save()
    return JsonResponse({'answer': user_answer,
                         'score': score})
