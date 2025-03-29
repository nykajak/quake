cd backend

python -m venv .env
. ".env\Scripts\activate"
cp -Path $args[0] -Destination ".\api\app_secrets.py"

try
{
    pip install -r requirements.txt
}
finally
{
    deactivate
    cd ..
}