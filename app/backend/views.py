import os

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from backend.celery_tasks import create_task


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


@require_POST
@login_required
def process_wav(request, quiz_id, quest_id):
    wav_filename = save_wav_to_disk(request, quest_id)

    if os.getenv('USE_SERVICES'):
        user_id = request.user.id
        task = create_task.delay(wav_filename, quest_id, user_id)
        result = {'result': task.id}
    else:
        result = {'result': 'Сервисы распознавания голоса отключены'}

    return JsonResponse(result)


@login_required
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)
