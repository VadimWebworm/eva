from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from ui.models import Quiz, Answer


def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
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


def index(request):
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request, "ui/index.html", context)


@login_required(login_url='/login')
def quiz(request, quiz_id, page):
    current_quiz = Quiz.objects.get(id=quiz_id)
    questions = current_quiz.get_questions()
    paginator = Paginator(questions, 1)
    page_object = paginator.get_page(page)
    question = page_object.object_list[0]
    context = {
        'quiz': current_quiz,
        'question': question,
        'question_id': question.id,
        'page_obj': page_object
    }
    return render(request, "ui/quiz.html", context)


@login_required(login_url='/login')
def results(request, quiz_id):
    answers = Answer.objects.filter(user=request.user).order_by().distinct('question')
    context = {
        'answers': answers
    }
    return render(request, 'ui/results.html', context)

