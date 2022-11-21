from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
import logging
logging.basicConfig(filename='logs/logs.log', level=logging.DEBUG)


def get_data_from_db():
    return 'Some quest'


def index(request):
    template = loader.get_template('ui/index.html')
    quest = get_data_from_db()
    context = {'quest': f'{quest}'}
    return HttpResponse(template.render(context, request))


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


def api_message(request):
    wav_object = save_wav_to_disk(request)
    user_answer = get_text_from_wav(wav_object)
    score = get_score_from_text(user_answer)
    response = f'{int(round(10*score))}'
    return response
