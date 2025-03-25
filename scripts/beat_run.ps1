cd backend
. ".env\Scripts\activate"

try
{
    celery -A api.celery beat -l info
}
finally
{
    cd ..
    deactivate
}