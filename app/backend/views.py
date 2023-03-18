from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import datetime
from backend.celery_tasks import create_task

import logging

from eva import settings

logging.basicConfig(filename='logs/logs.log', level=logging.INFO)


def save_wav_to_disk(request, quest_id):
    user_name = str(request.user)
    date_time_str = str(datetime.now()).replace(' ', '_').split('.')[0]
    filename = f'{user_name}_{quest_id}_{date_time_str}.wav'
    file_in_memory = request.FILES['voice']
    new_fn = default_storage.save(filename, file_in_memory)
    logging.info(f'File {filename} saved, new file name: {new_fn}')
    return new_fn


@require_POST
@login_required
def process_wav(request, quiz_id, quest_id):
    wav_filename = save_wav_to_disk(request, quest_id)

    if settings.USE_SERVICES:
        user_id = request.user.id
        task = create_task.delay(wav_filename, quest_id, user_id)
        result = {'result': task.id}
    else:
        result = {'result': 'Services disabled'}

    logging.info(result)
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
