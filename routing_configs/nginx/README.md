Steps to config nginx:
1. copy messenger.conf to /etc/nginx/sites-available
2. create symbolic link with command:
```bash
sudo ln -s /etc/nginx/sites-available/messenger-backend.conf /etc/nginx/sites-enabled
```
3. in /etc/nginx/sites-enabled delete file default:
```bash
sudo rm default
```
4. restart nginx:
```bash
service nginx restart
```

Also file /etc/hosts can be changed to load std-messenger.com instead 127.0.0.1 (or localhost) in browser by inserting:
```bash
127.0.0.1 std-messenger.com www.std-messenger.com
```

Then open in browser: std-messenger.com/api/

(after in venv: gunicorn helloworld:app)
