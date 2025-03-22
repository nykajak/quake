. "backend\.env\Scripts\activate"
celery -A backend.api.celery worker --pool=solo
cd ..