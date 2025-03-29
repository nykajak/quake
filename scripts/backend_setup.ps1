cd backend

python -m venv .env
. ".env\Scripts\activate"

try
{
    pip install -r requirements.txt
}
finally
{
    deactivate
    cd ..
}