#!/bin/sh -xe
# Install dependencies
aptitude -y upgrade
aptitude -y install dnsmasq python-flask python-pil python-serial

# Configure network services
sed -i 's/raspberrypi/harry/' /etc/hostname /etc/hosts
sed -i 's/127.0.1.1/192.168.1.1/' /etc/hosts
patch /etc/network/interfaces etc/network/interfaces.patch
patch /etc/dnsmasq.conf etc/dnsmasq.conf.patch
systemctl disable dhcpcd.service

# Install web-server and its systemd service
install --mode=644 --owner=root --group=root etc/systemd/system/harry.service /etc/systemd/system
systemctl daemon-reload
systemctl enable harry.service
