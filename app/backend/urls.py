from django.urls import path

from . import views

urlpatterns = [
    path("<int:quiz_id>/questions", views.get_quiz_questions, name="questions"),
    path("<int:quiz_id>/wav/<int:quest_id>", views.process_wav, name="wav_data"),
]
