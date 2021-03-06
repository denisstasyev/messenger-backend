server {
        listen 80;

        server_name stasyev.chickenkiller.com www.stasyev.chickenkiller.com;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        proxy_cache_valid 10m;

        root /home/ubuntu/www;
        index index.html;

        location /api {
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_redirect off;
                proxy_buffering off;

                if (!-f $request_filename) {
                        proxy_pass http://127.0.0.1:8000;
                }
        }

        location /public {
                alias /home/ubuntu/messenger-backend/public;
                autoindex on;
        }

        # For HTTPS
        location ~ /.well-known/acme-challenge {
                allow all;
        }

}
