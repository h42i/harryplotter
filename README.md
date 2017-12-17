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
    dpkg-reconfigure keyboard-configuration
    service keyboard-setup restart
    dpkg-reconfigure tzdata
    ```
2. Start SSH daemon
    ```
    passwd 
    systemctl enable ssh.service
    systemctl start ssh.service
    ```


### Network configuration and web-service
1. SSH into the Raspberry Pi.
2. Clone the repository and execute setup script:
    ```
    git clone https://github.com/h42i/harryplotter.git
    cd harryplotter
    sudo ./setup.py
    sudo reboot
    ```
