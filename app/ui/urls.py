from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:quiz_id>/<int:page>", views.quiz, name="quiz"),
    path("<int:quiz_id>/results", views.results, name='results'),
    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

]
