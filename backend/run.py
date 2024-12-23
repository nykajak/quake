from api import app,db
from api.models import *

with app.app_context():
    db.create_all()
app.run()