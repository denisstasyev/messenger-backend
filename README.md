# messenger-backend
This repository is only for Backend part of TechnoTrack FullStack development course by Mail.Ru.

## Setup
To setup this project:
1) setup nginx in folder /configs;

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

## Testing by hand views.py
POST methods:
```bash
curl -d "first_name=Denis&last_name=Stasyev" http://std-messenger.com/api/create_user/unique_username
```