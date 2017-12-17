# harryplotter
Raspbian system configuration and web-servicer for harry plotter


## Setup
### Root filesystem
1. Download the latest [Raspbian Image](https://downloads.raspberrypi.org/raspbian_lite_latest).
2. Copy the image onto an SD-card:
    ```
    unzip <whatever you just downloaded>
    dd bs=4M conv=fsync status=progress if=<unzipped>.img of=/dev/sd<X>
    ```
3. Insert the SD-card into your Raspberry Pi and boot the system.

### Basic configuration and remote access
1. Configure keyboard and timezone:
    ```
    sudo dpkg-reconfigure keyboard-configuration
    sudo dpkg-reconfigure tzdata
    ```
2. Start SSH daemon
    ```
    passwd
    sudo systemctl enable ssh.service
    sudo reboot
    ```
3. Connect the device to your local network.

### Network configuration and web-service
1. SSH into the Raspberry Pi.
2. Clone the repository and execute setup script:
    ```
    sudo aptitude update
    sudo aptitude -y install git
    git clone https://github.com/h42i/harryplotter.git
    cd harryplotter
    sudo ./setup.py
    sudo reboot
    ```
3. Disconnect the Raspbery Pi from your network as it will start DNS- and DHCP-servers, which otherwise *will* mess things up.


## Usage
The Pi will serve IP-adresses (ranging from 192.168.1.201 to 192.168.1.249) on its Ethernet interface.
Additionally, a minimal DNS-Server will register the domain `harry.plotter`.
In effect, all you have to do is
1. Connect a computer with a running DHCP client via Ethernet.
2. Open URL `harry.plotter`.
3. Follow the instructions. :-)
