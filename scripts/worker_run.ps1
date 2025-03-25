cd backend
. ".env\Scripts\activate"

try
{
    celery -A api.celery worker --pool=solo
}
finally
{
    cd ..
    deactivate
}
