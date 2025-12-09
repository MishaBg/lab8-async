from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import time
import random
import requests
from concurrent import futures

# Настройки — при необходимости измените
CALLBACK_URL = 'http://127.0.0.1:8080'
# Путь будет сформирован как: {CALLBACK_URL}/api/road/{service_id}/set-cost
SECRET_TOKEN = 'SECRET_KEY_LAB8'

executor = futures.ThreadPoolExecutor(max_workers=2)


def compute_cost(service_id):
    # эмулируем трудоёмкую работу
    time.sleep(15 + random.random()*5)
    # Возвращаем рассчитанный cost (пример): случайное float 100..1000
    cost = round(100 + random.random()*900, 2)
    return {"service_id": service_id, "cost": cost}


def callback_put(task):
    try:
        result = task.result()
    except Exception:
        return

    url = f"{CALLBACK_URL}/api/road/{result['service_id']}/set-cost"
    headers = {"Content-Type": "application/json", "X-Auth-Token": SECRET_TOKEN}
    payload = {"cost": result['cost']}
    try:
        requests.put(url, json=payload, headers=headers, timeout=5)
    except Exception:
        # логирование можно добавить здесь
        pass


@api_view(['POST'])
def calculate(request):
    # Ожидаем JSON с { "service_id": <int> }
    if not request.data or 'service_id' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        service_id = int(request.data['service_id'])
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    task = executor.submit(compute_cost, service_id)
    task.add_done_callback(callback_put)

    return Response({"status": "processing"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok", "service": "lab8-async"})
