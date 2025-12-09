# lab8-async

Асинхронный сервис (Django) для лабораторной 8.

- Один POST-эндпоинт `/calculate/` — принимает JSON `{ "service_id": <int> }`.
- Запускает фоновую задачу (5-10s), вычисляет `cost` (случайно или по формуле) и выполняет PUT к основному сервису:
  - URL: `http://<MAIN_HOST>:<MAIN_PORT>/api/road/{service_id}/set-cost`
  - Заголовок: `X-Auth-Token: SECRET_KEY_LAB8`
  - Тело: JSON `{ "cost": <float> }`

Quickstart:

1. Создайте виртуenv: `python -m venv env` и активируйте: `. env/bin/activate`
2. Установите зависимости: `pip install -r requirements.txt`
3. Запустите: `python manage.py runserver 8001`
4. Тест: `curl -X POST http://127.0.0.1:8001/calculate/ -H "Content-Type: application/json" -d '{"service_id":1}'`

Настройте `CALLBACK_URL` и `SECRET_TOKEN` в `app/views.py` при необходимости.
