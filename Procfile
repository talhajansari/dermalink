web: gunicorn runp-heroku:app
init: rm app.db && python db_create.py 
upgrade: python db_upgrade.py
