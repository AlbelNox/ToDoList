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

3. Open Windows PowerShell (`Admin`):

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
   
```html
# Browser url
<raspberry Pi IPv4>
```
you should see `Apache2 Debian Default Page`

2. Run your own html (another test)
```bash
# --> Commandss in powershell <--
echo '<h1>Hello World!</h1>' | sudo tee /var/www/html/index.html
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
> CTRL + C

4. review the data
```bash
# --> Commands in powershell <--
sudo tcpdump -r webzugriff.pcap
```
## Have fun with it 😊
	    
# LICENCE
This project is licensed under the MIT License. See the [LICENCE](https://github.com/AlbelNox/ToDoList/blob/main/LICENSE) for more information.
