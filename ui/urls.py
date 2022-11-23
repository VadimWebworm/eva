from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:quiz_id>/", views.quiz, name="quiz"),
    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

]
