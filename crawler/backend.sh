nohup celery -A spider worker -l info > $HOME/celery.log &
nohup sudo ~/crawler/crawler/env/bin/flask run -h '0.0.0.0' -p 80 > $HOME/gunicorn.log &
