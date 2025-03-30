# Quake
Quizzing application built as part of IITM BS Degree - Diploma level - MAD 2 project

# Setup instructions
- git clone this repo
- Navigate to the root folder of Quake
- Run `./scripts/backend_setup.ps1 $1` where $1 is the path to app_secrets.py file to set up the backend.
- Run `./scripts/frontend_setup.ps1` to set up the frontend.

# Run instructions
- Ensure setup steps properly completed.
- Navigate to root folder and create 5 terminals
- In the first terminal run `./scripts/backend_run.ps1` to boot up the backend.
- In the second terminal run `./scripts/frontend_run.ps1` to boot up the backend.
- In the third terminal launch redis, using default port.
- In the fourth terminal run`./scripts/beat_run.ps1` to boot up celery beat.
- In the fifth terminal run`./scripts/worker_run.ps1` to start the celery worker.
- Go to http://localhost:5173 to view the application

# Other info
- The manage_db.py requires a backend/api/database.json file to setup and backup the current database state.
- The app_secrets.py includes four variables - FLASK_SECRET_KEY, JWT_SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD 
- The first two variables can be set manually, the other two should be mailtrap credentials.
- The generated reports will be in backend/api/static folder. There is no automated deletion.
- A test database is already in instance folder (quiz.db)

# Links
Project report: [Link](https://drive.google.com/file/d/1VazLerBQTPa53a_Up15i71PA5sjMviy-/view?usp=sharing)
Project video: [Link](https://drive.google.com/file/d/1386fOVpum6oaTS42R0mLWVfVxBQ5tW3O/view?usp=drive_link)