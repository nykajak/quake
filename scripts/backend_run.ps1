cd backend
. ".env\Scripts\activate"

try
{
    python "run.py"
}
finally
{
    cd ..
    deactivate
}