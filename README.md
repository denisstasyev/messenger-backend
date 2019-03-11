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