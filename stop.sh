ps aux | grep 'serve -s build' | awk -e '{print($2)}' | xargs kill -9
ps aux | grep 'gunicorn' | awk -e '{print($2)}' | xargs kill -9
ps aux | grep 'celery' | awk -e '{print($2)}' | xargs kill -9
