# RIAnalytics


1. Fist do this commmand then paste the content this file to your vm
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
content
```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=dhairya
Group=www-data
WorkingDirectory=/home/dhairya/RIAnalytics    # Change the username from dhairya to your username in every place
ExecStart=/home/dhairya/RIAnalytics/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/dhairya/RIAnalytics/RIAnalytics.sock RIAnalytics.wsgi:application

[Install]
WantedBy=multi-user.target
```

2. Start this service
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
```
Check status
```bash
sudo systemctl status gunicorn
```

3. Now do this commands and paste content.
```bash
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/conf.d/RIAnalytics.conf
```
Content
```bash
server {
    listen 80;
    server_name 134.209.151.28;    # Change this with your vm ip

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/dhairya/RIAnalytics/static/;   # Change username from dhairya to your username in every place
    }
    location /.well-known {
    alias /home/dhairya/RIAnalytics/;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/dhairya/RIAnalytics/RIAnalytics.sock;
    }
}
```

4. Restart NGINX
```bash
sudo systemctl restart nginx
```

And done visit the ip
