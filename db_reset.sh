#!/bin/bash
echo "Database is being reset...:"
echo "1. Deleting existing app.db..."
rm app.db
echo "2. Creating new app.db..."
flask/bin/python db_create.py
echo "3. Migrating to new app.db..."
flask/bin/python db_migrate.py
echo "4. Emptying uploaded pics directory"
rm uploads/*
echo "Database reset complete."
echo "*************************" 
