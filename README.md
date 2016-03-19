#R2 Chat

Realtime chat application built using Django


```
sudo apt-get install python-psycopg2  django-debug-toolbar django-redis redis
sudo apt-get install redis-server

#start the django server
python manage.py migration
python manage.py makemigrations 
python manage.py runserver

cd nodejs
npm install 
node chat.js #this opens socket.io server on localhost:4000

```