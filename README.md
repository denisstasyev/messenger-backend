# messenger-backend
This repository is only for Backend part of TechnoTrack FullStack development course by Mail.Ru.

## Deployment
```bash
sudo apt update
sudo apt nginx python3 memcached
sudo apt install git -y
sudo apt install redis-server -y
sudo apt install python3-pip -y
sudo pip3 install virtualenv
sudo systemctl start memcached

git clone https://github.com/denisstasyev/messenger-backend.git
cd messenger-backend/
virtualenv venv
pip3 install -r requirements.txt
source venv/bin/activate
```
Change user from "denis" to your local user in ./routing_configs/nginx/messenger-backend.conf, change server_name to your (my: stasyev.chikenkiller.com)
```bash
cp ./routing_configs/nginx/stasyev.chickenkiller.com /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/stasyev.chickenkiller.com /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

mkdir instance
touch ./instance/production.cfg

flask db upgrade
```
In production.cfg add SQLALCHEMY_DATABASE_URI (better to use Postgresql), MAIL_PASSWORD and SECRET_KEY.
Finally change in app/\__init__.py line to:
```python
app.config.from_pyfile("production.cfg", silent=True)
```
HTTPS via Certbot
```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx 

sudo certbot --nginx
sudo certbot renew --dry-run
```

## Run
Run this project with commands:
```bash
cd messenger-backend/
source venv/bin/activate
gunicorn -c routing_configs/gunicorn/gunicorn.conf.py run:app
```

## Some basics
### Setup
To setup this project:
1) setup nginx in folder /configs;
2) create database:
```bash
sudo apt install postgresql
sudo -u postgres psql
    CREATE USER denis WITH ENCRYPTED PASSWORD 'your_password';
    CREATE DATABASE "messenger" OWNER denis;
    GRANT ALL PRIVILEGES ON DATABASE "messenger" TO denis;
```
3) setup database via migrations.

### Database migrations
```bash
flask db init
flask db migrate -m "000_some_text"
flask db upgrade
```

In case of any migration problems:
```bash
DROP TABLE alembic_version;
```

### Open database from Terminal
```bash
psql messenger-backend-development
SELECT * FROM users;
```

### Flask-Manager + Flask-Migrate
You can use any migration commant via db postfix, for example:
```bash
python3 run.py db upgrade
```

### Celery
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

### Memcached
```bash
sudo apt install memcached
sudo systemctl start memcached
```