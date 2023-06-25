import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from match_maker_bot import celery_app

from sport_events.utils import is_valid_payment_status


# Create your views here.

@api_view(['POST'])
def payment_notification(request):
    data = json.loads(request.body)
    status = data.get("status")


    if not is_valid_payment_status(status):
        return Response("Invalid data", status=400)

    data = json.loads(data.get("callback_data"))
    if status == 'paid':
        task = celery_app.signature('sport_events.tasks.notify_user_about_payment_success')
        task.delay(data)
    else:
        task = celery_app.signature('sport_events.tasks.notify_about_payment_cancel')
        task.delay(data)
    return Response("OK", status=200)
