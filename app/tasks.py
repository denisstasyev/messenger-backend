from app import celery


@celery.task()
def add_together(a, b):
    return a + b


# в task не передавать модели ORM
