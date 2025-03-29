cd backend
. ".env\Scripts\activate"

try
{
    pip install -r requirements.txt
}
finally
{
    cd ..
    deactivate
}