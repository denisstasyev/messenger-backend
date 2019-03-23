from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["result_backend"],
        broker=app.config["broker_url"],
    )
    celery.conf.update(app.config)

    celery.conf.timezone = "UTC"
    celery.conf.beat_schedule = {
        "birthday-task": {
            "task": "tasks.send_email_birthday",
            "schedule": crontab(hour=7, minute=0),
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
