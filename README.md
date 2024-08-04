<div align="center">
  <h1>Hidden Cave</h1>
</div>

## Table of Contents
1. [Introduction](#introduction)
2. [Deployment](#deployment)
3. [Contributing](#contributing)
4. [TODO](#todo)
5. [Disclaimer](#disclaimer)

## Introduction
**Hidden Cave** is an API-based command-and-control (C2) server designed to manage interactions with The Bear infostealer. It ensures secure communication between the API and the attacker by encrypting all requests and responses using AES-GCM 256 encryption. For routes documentation, please refer to the [APIDOC](https://github.com/yo-aiv1/hiddencave/blob/main/APIDOC.md), For the CLI commands documentation please refer to it's [README.MD](https://github.com/yo-aiv1/hiddencave/blob/main/CLI/README.md).

## Deployment
> :information_source: The C2 API can only be deployed on Linux servers, but the CLI that can be used to interact with the API can work on any OS.

Before starting the deployment, ensure you have the following prerequisites installed:
- **Nginx:** `sudo apt-get install nginx`
- **Gunicorn:** `sudo apt-get install gunicorn`
- **Python Dependencies:** Install the required packages using `pip3 install -r requirements.txt`

After installing the prerequisites, generate the `settings.json` file that the API and the preload script rely on by launching the CLI:
```bash
python main.py
```
Use the `set` command to generate random cryptographic parameters and set the API IP (public IP):
> :information_source: Ensure the port you want to serve the API on is open. This depends on your hosting provider; you may need to open the port in the provider's panel.
```bash
$HiddenCave-> set key rand
$HiddenCave-> set iv rand
$HiddenCave-> set ip 112.168.1.2
$HiddenCave-> set port 1174
```
After setting the needed parameters, save the settings to a file:
```bash
$HiddenCave-> save settings.json
```
Copy the `settings.json` file to the API folder and transfer the API folder to the server where you plan to deploy it.

On the Linux server, after installing Nginx and Gunicorn, run the `predeploy.py` script to generate two files: `api.conf` and `apiserv.service`.
- **apiserv.service:** A service file to run the API, ensuring it starts automatically even if the server reboots.
- **api.conf:** The Nginx config file to route web requests to Gunicorn.

Copy the `apiserv.service` file to the services folder (`/etc/systemd/system/`) and start the service:
```bash
sudo cp apiserv.service /etc/systemd/system/
sudo systemctl start apiserv
sudo systemctl enable apiserv
```
Check its status:
```bash
sudo systemctl status apiserv
```
If it says `Active: active (running)`, the service is running correctly.

Enable the Nginx config file by copying it to the sites-available directory and linking it to the sites-enabled directory:
```bash
sudo cp api.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/api.conf /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

Now that the API is deployed, launch the CLI again, load the `settings.json` file, and use the `check` command to ensure everything is working:
```bash
$HiddenCave-> load settings.json
$HiddenCave-> check
[+] All good.
```

## Contributing
Contributions are welcome! If you would like to contribute to this project, please open an issue first to discuss your proposed changes or additions. This helps ensure that your contribution aligns with the project's goals and prevents duplication of effort. Additionally, check the [TODO](#todo) section for current bugs to fix and areas for improvement.

Thank you for your interest in improving this project!

## TODO
- Add a route for extracting crypto wallet seeds.
- Add a route for delete a victim's data.
- Edit the API to function as a proxy so users can add a Telegram bot token or Discord webhook and automatically receive data when a new victim is available.


## Disclaimer
This repository is created for educational purposes only. The author is not responsible for any damage or misuse of the code. Users are solely responsible for their actions and any consequences that may arise from using this software. Please use this tool responsibly and ethically, and only in environments where you have explicit permission to conduct security testing.
