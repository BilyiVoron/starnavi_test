# starnavi_test
 Social network for Starnavi's test task includes such features as:
 - user signup
 - user login
 - post creation, update, delete
 - possibility to comment post and add like or dislike
 Also wrote unit test using Django Tests for every API endpoint
 
 # INSTRUCTIONS
 1. First item you have to do is creating PostgreSQL database*:
- CREATE DATABASE your_db_name;
- CREATE USER your_user WITH ENCRYPTED PASSWORD 'your_pass';
- GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
 2. Then you have to sync database using command:
 - python manage.py migrate
 3. The next step is creating superuser to have possibility use Django admin panel:
 - python manage.py createsuperuser
 4. At least you have to start your app on a local server
 - python manage.py runserver
 
 
 * you may use my own config from .env file in the root directory 
 or replace them with yours