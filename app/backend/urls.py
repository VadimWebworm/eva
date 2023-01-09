from django.urls import path

from . import views

urlpatterns = [
    path("<int:quiz_id>/wav/<int:quest_id>", views.process_wav, name="wav_data"),
]
