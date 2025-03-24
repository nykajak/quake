from api import app,db
from api.models import * # Required to make sure all models created!

# Note: Requires a proper setup script to setup database to a pre-defined state!
# Create all tables in db if they don't exist!
with app.app_context():
    db.create_all()

# Run the application
app.run()