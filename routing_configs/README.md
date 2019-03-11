Firstly config /nginx, then check connection with gunicorn, then use command being in venv state:
```bash
gunicorn -c routing_configs/gunicorn/gunicorn.conf.py run:app
```
to run.
