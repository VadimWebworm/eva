import json
import requests

from celery import shared_task
from django.utils import timezone
from ui.models import Answer, Question
from django.contrib.auth.models import User

import logging
logging.basicConfig(filename='logs/logs.log', level=logging.INFO)

ASR_URL = 'http://asr:5005'
TS_URL = 'http://ts:5000'


def text_to_score(user_answer, true_answer):
    """ Send text data to NLP server, get the answer score """
    r = requests.post(TS_URL, json={'s1': user_answer, 's2': true_answer})
    j_res = json.loads(r.text)
    score = float(j_res['Similarity'])

    logging.info(f'User answer: {user_answer} , Score: {score}')
    return score


@shared_task
def create_task(wav_filename, quest_id, user_id):

    file_wrapper = {'wav_file': open(wav_filename, 'rb')}
    r = requests.post(ASR_URL, files=file_wrapper)
    j_str = json.loads(r.text)

    user_answer = json.loads(j_str)['text']
    question = Question.objects.get(id=quest_id)
    true_answer = question.true_answer
    score = text_to_score(user_answer, true_answer)

    user = User.objects.get(id=user_id)
    answer = Answer(
        content=user_answer,
        question=question,
        user=user,
        wav=wav_filename,
        date_time=timezone.now(),
        score=score
    )
    answer.save()

    return True
