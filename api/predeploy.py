import getpass
import os
import re
import subprocess
import json

file = open("settings.json")
data = json.loads(file.read())
file.close()

ip = data["ip"]
port = data["port"]

NgnixConfData = """server {
    listen 2247;
    server_name 127.0.0.1;

    client_max_body_size 50M;
    keepalive_timeout 65;
    keepalive_requests 100;

    location / {
        proxy_pass http://127.0.0.1:8123;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}"""


NgnixConfData = re.sub(r'listen(.*?);', f"listen {port};", NgnixConfData)
NgnixConfData = re.sub(r'server_name(.*?);', f"server_name {ip};", NgnixConfData)


ServData = """[Unit]
Description=Start the API
After=network.target

[Service]
User=
Group=www-data
WorkingDirectory=
ExecStart=

[Install]
WantedBy=multi-user.target"""

GunicornPath = subprocess.check_output(['which', 'gunicorn']).decode("utf-8")
command = f"{GunicornPath[:-1]} --workers 2 --bind 127.0.0.1:8123 run:app"
ServData = re.sub(r'User=(.*?)', f"User={getpass.getuser()}", ServData)
ServData = re.sub(r'WorkingDirectory=(.*?)', f"WorkingDirectory={os.getcwd()}", ServData)
ServData = re.sub(r'ExecStart=(.*?)', f"ExecStart={command}", ServData)

NgnixConfFile = open("api.conf", "w")
NgnixConfFile.write(NgnixConfData)
NgnixConfFile.close

ServFile = open("apiserv.service", "w")
ServFile.write(ServData)
ServFile.close