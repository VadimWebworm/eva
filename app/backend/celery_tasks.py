import json
import requests

from celery import shared_task
from django.core.files.storage import default_storage
from django.utils import timezone
from eva import settings
from ui.models import Question, Answer
from django.contrib.auth.models import User

import logging
if settings.DEBUG:
    logging.basicConfig(filename='logs/debug_logs.log', level=logging.DEBUG)
else:
    logging.basicConfig(filename='logs/prod_logs.log', level=logging.INFO)

ASR_URL = 'http://asr:5005'
TS_URL = 'http://ts:5000'


def text_to_score(user_answer, right_answer):
    """ Send text data to NLP server, get the answer score """
    r = requests.post(TS_URL, json={'s1': user_answer, 's2': right_answer})
    j_res = json.loads(r.text)
    score = float(j_res['Similarity'])
    logging.info(f'User answer: {user_answer}, right answer: {right_answer} , Score: {score}')
    return score


@shared_task()
def create_task(wav_filename: str,
                quest_id: int,
                user_id: int) -> bool:
    logging.info(f'user id {user_id}, type is {type(user_id)}')
    user = User.objects.get(pk=user_id)
    question = Question.objects.get(id=quest_id)
    if settings.USE_SERVICES:
        try:
            wav_file = default_storage.open(wav_filename)
        except FileNotFoundError:
            logging.error(f'Missing file: {wav_filename}')
            return False
        file_wrapper = {'wav_file': wav_file}
        r = requests.post(ASR_URL, files=file_wrapper)
        j_str = json.loads(r.text)

        user_answer = json.loads(j_str)['text']
        right_answer = question.true_answer
        score = text_to_score(user_answer, right_answer)
    else:
        user_answer = 'Services disabled'
        score = 0.0
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
