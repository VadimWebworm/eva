import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from backend.kaldi_utils import wav_to_text
from ui.models import Quiz, Answer, Question

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
    return filename


def get_score_from_text(user_answer):
    """ Send text data to NLP server, get the answer score """
    logging.info(f'User answer: {user_answer} , calculating score')
    return 0.5


def get_quiz_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = {
        'questions': list(quiz.get_questions().values(), ),
    }
    return JsonResponse(questions, safe=False, json_dumps_params={'ensure_ascii': False})


@require_POST
@login_required
def process_wav(request, quiz_id, quest_id):
    wav_filename = save_wav_to_disk(request, quest_id)
    user_answer = wav_to_text(wav_filename)
    print(user_answer)
    score = get_score_from_text(user_answer)
    answer = Answer(
        content=user_answer,
        question=Question.objects.get(id=quest_id),
        user=request.user,
        wav=wav_filename,
        date_time=timezone.now(),
        score=score
    )
    answer.save()
    return JsonResponse({'Status': 'processing'})
