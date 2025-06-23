# Project
This project sets up a **headless Raspberry Pi webserver**, mainly to host an `<index.html>` file that interacts with another project.  
It uses Apache2 as a basic web server and provides step-by-step setup instructions from flashing the SD card to network monitoring with `tcpdump`.
New users will be added with `access control` and the webapp will be deployed with a `docker` container. In the end you can access the `todo-List` via `api` in the `browser`. 

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
- Adding user in raspberry pi with diffrent access permissions
- `Optional`: Setting static ip-adress for raspberry pi
- Installation for docker
- How to build a docker-container
- start your application with the docker container 
  
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
- Rightclick at the topframe
- Click properties
- Activate `USE Ctrl+Shift+C/V as Copy/Paste`
- Click 'OK'
Now, you should be able to copy & paste text via rightclicked mouse.
```

```bash
# --> Commands in powershell <--
# Check if raspberry is found in network, IPv4 as response
# For easier access make the IPv4 for the raspberry static
ping raspberrypi -4

# Enable SSH connection with raspberry pi
ssh <Pi_Hostname>@<raspberry Pi IPv4>
```

### 🔴 If you see `"Warning: Remote Host Identification has changed!"`

```bash
# --> Commands in powershell <--
# Reset SSH key
ssh-keygen -R <raspberry Pi IPv4>

# Retry to connect via SSH
ssh <Pi_Hostname>@<raspberry Pi IPv4>
```
### 🟢 Else

4. Authenticate:
- `yes` for authentitytest
- Enter `Pi_password`

`Optional`: Run configuration tool (`not needed!`)
```bash
# --> Commands in powershell <--
# Access to config of raspberry pi 
sudo raspi-config
```
`Optional`: Setting static ip-adress for raspberry pi (`not needed!`)
```bash
# Install NetworkManager (if not already present)
sudo apt install network-manager -y

# Disable the old system (dhcpcd) so they don’t conflict
sudo systemctl disable dhcpcd
sudo systemctl stop dhcpcd

# Now enable & start NetworkManager
sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager

# Verify that the NetworkManager is running
nmcli general status

# List your connections for a better overview 
nmcli connection show

# Set static ip-adress for raspberry pi
nmcli connection modify "<your connection>" \
ipv4.addresses <future raspberry pi ip-adress>/<subnetmask> \
ipv4.gateway <gateway ip-adress> \
ipv4.dns "<gateway ip-adress> 8.8.8.8" \
ipv4.method manual

# Apply changes
nmcli connection down "<your connection>"
nmcli connection up "<your connection>"
# Or
sudo reboot
```

### Installing apache webserver
```bash
# --> Commands in powershell <--
# Check updates for your application
sudo apt update

# Install apache2
sudo apt install apache2 -y
# Check if installed correctly and available (active (running))
sudo systemctl status apache2
```

`Optional`:
```bash
# --> Commands in powershell <--
# Upgrading currently installed applications to their latest available version
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
# EOF makes sure, that there will be no output in the console
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
1. Installing & recording
```bash
# --> Commands in powershell <--
# Install tcpdump
sudo apt install tcpdump -y

# Start recording port80 (HTTP) traffic save in file named "webzugriff.pcap"
# You can change the name, but change it in the following Commands too!
sudo tcpdump -i eth0 port 80 -w webzugriff.pcap
```
2. Interact with the server (`reload browserpage`)

3. Stop recording in powershell via
>--> Commands in powershell <--
>
> CTRL + C

4. Review the data
```bash
# --> Commands in powershell <--
sudo tcpdump -r webzugriff.pcap
```

## Adding User for Raspberry
As example we add two Users, one with normal permissions and one with adm permissions.
### Add first user
1. Add User

```bash
sudo adduser <username>
```
2. Set password and more information and save it
```markdown
- Setting password
- Verify password
- Optional: add more information
- Verify your information with 'y'
```
3. Revoke sudo access permissions for user
```bash
sudo deluser <username> sudo
```
Make sure to remember `<username>` & `<password>` for the user.
### Add second user
4. Add User
```markdown
- Repeat step 1 & 2
```
Make sure to remember `<username>` & `<password>` for the user.

5. Grant Sudo permission
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
# Use it with ubuntu
sudo docker run -it ubuntu bash
# Optional:
# Getting list of dockerimages:
sudo docker images
```
4. Create dockerfile
- Baseimage for container
- Installation of requirements
- Copy of python script in container

```markdown
# Dockerfile

# Downloading basisimage for python application
FROM python:3.12-alpine

# Changing workdirectory to Containerdirectory
WORKDIR /app

# Installing requirements
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
# Change directory
cd <path of repository>
# Build container with specific name
Sudo docker build -t <specific name>
```
6. Start container
```bash
sudo docker run -p 5000:5000 -d <specific name>
```
7. Verify running container
```bash
sudo docker ps
```
In the list should be your <specific name>.

8. Test in browser
```markdown
# <raspbarry pi ip adress>:<port>/<api endpoint>

# :5000 is the port where it is running
# /<endpoint of api>
```
```html
192.168.24.102:5000/todo-lists
```
The response should look like this:
```html
[
  {
    "id": "1318d3d1-d979-47e1-a225-dab1751dbe75",
    "name": "Einkaufsliste"
  },
  {
    "id": "3062dc25-6b80-4315-bb1d-a7c86b014c65",
    "name": "Arbeit"
  },
  {
    "id": "44b02e00-03bc-451d-8d01-0c67ea866fee",
    "name": "Privat"
  },
  {
    "id": "123dbe00-02df-4643-adcb-0c1234378900",
    "name": "Programmieren"
  }
]
```

## Have fun with it 😊
	    
# LICENCE
This project is licensed under the MIT License. See the [LICENCE](https://github.com/AlbelNox/ToDoList/blob/main/LICENSE) for more information.
