# messenger-backend
This repository is only for Backend part of TechnoTrack FullStack development course by Mail.Ru.

## Setup
To setup this project:
1) setup nginx in folder /configs;
2) setup database:
```bash
flask db init
flask db upgrade
```;

Run this project with commands:
```bash
source venv/bin/activate
gunicorn -c routing_configs/gunicorn/gunicorn.conf.py run:app
```

## Database migrations
```bash
flask db init
flask db migrate -m "000_some_text"
flask db upgrade
```

In case of any migration problems:
```bash
DROP TABLE alembic_version;
```

## Open database from Terminal
```bash
psql messenger-backend-development
SELECT * FROM users;
```

## Flask-Migrate
You can use any migration commant via db postfix, for example:
```bash
python3 run.py db upgrade
```

## Celery
Celery creates queue of asynchronous tasks. To enable asynchronous tasks run command below at the same time with Gunicorn command above:
```bash
celery -A app.celery worker --loglevel=INFO
```
For scheduled tasks run also Celery Beat:
```bash
celery -A app.celery beat --loglevel=INFO
```

To manage celery use Flower:
```bash
flower -A app.celery --port=5555
```

## Memcached
```bash
sudo apt install memcached
sudo systemctl start memcached
```