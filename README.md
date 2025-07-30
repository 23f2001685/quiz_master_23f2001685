# quiz_master_23f2001685
It is a multi-user app (one requires an administrator and other users) that acts as an exam preparation site for multiple courses.

---
# Commands

Steps to run the app
For Caching and celery to work you need to open
First open folder in vs code
## Install required dependencies
For Backend & Celery
```sh
pip install -r requirements.txt
```

Secondly, you need to migrate your database
```sh
flask db upgrade
flask db migrate -m "Initial database setup"
```

For Frontend
```sh
cd frontend
npm i
```

Then run the app using following command
## Run Backend
```sh
cd backend
py app.py
```
## Run Frontend
```sh
cd frontend
npm run dev
```

## Run celery (for workers)
```sh
cd backend
celery -A celery_config.celery_app worker --loglevel=info --pool=solo
```

## Run celery (for beats)
```sh
cd backend
celery -A celery_config.celery_app beat --loglevel=info
```
