from celery import Celery

app = Celery('celery_app',
            broker="pyamqp://clrusr:p@ssword@localhost:5672/clrhst",
            backend="rpc://")

