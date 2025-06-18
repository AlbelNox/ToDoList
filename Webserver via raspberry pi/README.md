# Project
This project sets up a **headless Raspberry Pi webserver**, mainly to host an `<index.html>` file that interacts with another project.  
It uses Apache2 as a basic web server and provides step-by-step setup instructions from flashing the SD card to network monitoring with `tcpdump`.

# Librarys
- apache2
- tcpdump
- openssh-server (usually preinstalled on Pi OS)

# Web-Framework-Librarys
- Apache2

# Functions
- Apache2 setup for HTML serving
- Headless Pi configuration
- SSH access and configuration
- Index page customization via Bash
- Basic TCP traffic monitoring (port 80)
  
# Setup
## Setup Guide: Webserver on Raspberry Pi (`Headless, from Windows`)
### Flash image & enable SSH
1. Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash the SD card (16–128 GB).

2. Enable SSH (under 'Advanced options').

3. Set: 
 - `Pi_Hostname`
 - `Pi_password`
 - Save them for later
 
### First boot & network connection
1. Insert SD card, connect Pi to **power** and **router/switch** via RJ45 (LAN).

2. Check LED at RJ45 port: orange (power), green (network activity).

3. Open Windows PowerShell (`Admin`) on your windows pc:
```markdown
If copy & paste is not enabled in your powershell:
- rightclick at the topframe
- click properties
- activate `USE Ctrl+Shift+C/V as Copy/Paste`
- click 'OK'
Now, you should be able to copy & paste text via rightclicked mouse.
```

```bash
# --> Commands in powershell <--
# check if raspberry is found in network, IPv4 as response
# for easier access make the IPv4 for the raspberry static
ping raspberrypi -4

# Enable SSH connection with raspberry pi
ssh <Pi_Hostname>@<raspberry Pi IPv4>
```

### 🔴 If you see `"Warning: Remote Host Identification has changed!"`

```bash
# --> Commands in powershell <--
# reset SSH key
ssh-keygen -R <raspberry Pi IPv4>

# retry to connect via SSH
ssh <Pi_Hostname>@<raspberry Pi IPv4>
```
### 🟢 Else

4. Authenticate:
- `yes` for authentitytest
- enter `Pi_password`

Optional: Run configuration tool (`not needed!`)
```bash
# --> Commands in powershell <--
# Access to config of raspberry pi 
sudo raspi-config
```

### Installing apache webserver
```bash
# --> Commands in powershell <--
# check updates for your application
sudo apt update

# install apache2
sudo apt install apache2 -y
# check if installed correctly and available (active (running))
sudo systemctl status apache2
```

Optional:
```bash
# --> Commands in powershell <--
# upgrading currently installed applications to their latest available version
sudo apt upgrade
```

### Test apache server
1. Open in your pc browser:
   
```HTML
# Browser url
<raspberry Pi IPv4>
```
you should see `Apache2 Debian Default Page`

2. Run your own html (another test)
```bash
# --> Commands in powershell <--
# HTML with little Design
sudo tee /var/www/html/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Raspberry Pi Website</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 100px;
            background-color: #f0f0f0;
            color: #333;
        }
        h1 {
            color: #2c3e50;
        }
        p {
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <h1>Hello World!</h1>
    <p>This website is published by my Raspberry Pi. Now a great journey begins!</p>
</body>
</html>
EOF
```

3. Reload browser - it should show your message.

### Monitor web traffic
1. installing & recording
```bash
# --> Commands in powershell <--
# install tcpdump
sudo apt install tcpdump -y

# start recording port80 (HTTP) traffic save in file named "webzugriff.pcap"
# you can change the name, but change it in the following Commands too!
sudo tcpdump -i eth0 port 80 -w webzugriff.pcap
```
2. interact with the server (`reload browserpage`)

3. stop recording in powershell via
>--> Commands in powershell <--
>
> CTRL + C

4. review the data
```bash
# --> Commands in powershell <--
sudo tcpdump -r webzugriff.pcap
```

## Adding User for Raspberry
As example we add two Users, one with normal rights and one with adm rights.
### Add first user
1. Add User

```bash
sudo adduser <username>
```
2. Set password and more information and save it
```markdown
- setting password
- verify password
- optional: add more information
- verify your information with 'y'
```
3. revoke sudo rights for user
```bash
sudo deluser <username> sudo
```
### Add second user
4. Add User
```markdown
- Repeat step 1 & 2
```
5. Grant Sudorights
```bash
sudo usermod -aG sudo <username>
```
## Setting up Application with Docker
1. Install Docker
```bash
sudo apt install docker.io
# If there is a question for more dataspace verify with 'yes'
```
2. Start Docker
```bash
sudo systemctl start docker.service
```
3. Verify installation with test
```bash
sudo docker run hello-world
# use it with ubuntu
sudo docker run -it ubuntu bash
# optional:
# getting list of dockerimages:
sudo docker images
```
4. Create dockerfile
- Baseimage for container
- installation of requirements
- copy of python script in container

```markdown
# Dockerfile

# Downloading basisimage for python application
FROM python:3.12-alpine

# Changing workdirectory to Containerdirectory
WORKDIR /app

# installing requirements
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy local file into dockerimage
COPY server.py /app

# Configure the command to be executed in the container
# (Application Python + Scriptname as Parameter)
ENTRYPOINT [ "python" ]
CMD ["server.py"]
```
5. Build docker container
```bash
git clone <link to repository>
# change directory
cd <path of repository>
# build container with specific name
Sudo docker build -t <specific name>
```
6. Start container
```bash
sudo docker run -p 5000:5000 -d <specific name>
```
7. verify running container
```bash
sudo docker ps
```
Here should be your <specific name> in the list
8. Test in browser
```markdown
<raspbarry pi ip adress>:<port>/<apiendpoint>

:5000 is the port where it is running
/<endpoint of api>
```
```html
192.168.24.102:5000/todo-lists
```

## Have fun with it 😊
	    
# LICENCE
This project is licensed under the MIT License. See the [LICENCE](https://github.com/AlbelNox/ToDoList/blob/main/LICENSE) for more information.
