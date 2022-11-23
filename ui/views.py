from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template import loader
import logging

from ui.models import Quiz, Question

logging.basicConfig(filename='logs/logs.log', level=logging.DEBUG)


def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            return redirect('/register')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "signup.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html")
    return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect('/')


def get_data_from_db():
    return 'Some quest'


def index(request):
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request, "ui/index.html", context)


@login_required(login_url='/login')
def quiz(request, my_id):
    context = {}
    context['quiz'] = Quiz.objects.get(id=my_id)
    context['question'] = Question.objects.all()[0]
    return render(request, "ui/quiz.html", context)


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
