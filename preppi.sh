#!/bin/bash

systemctl disable bluetooth.service
systemctl disable hciuart.service
apt-get update && apt-get -y upgrade

ln /opt/kiosk/kiosk.service /lib/systemd/system/kiosk.service
ln /opt/kiosk/firstboot.service /lib/systemd/system/firstboot.service
ln /opt/kiosk/kiosk.ini /home/pi/kiosk.ini
systemctl enable firstboot.service

timedatectl set-timezone Europe/Riga
sed -i '/^# Additional overlays.*/a dtoverlay=pi3-disable-wifi\ndtoverlay=pi3-disable-bt' /boot/config.txt
sed -i '/^\[all\].*/a gpu_mem=16' /boot/config.txt
apt-get --yes install libcups2-dev cups cups-bsd
cupsctl --remote-admin --remote-any
usermod -a -G lpadmin pi
usermod -a -G lp pi
addgroup kiosk
usermod -a -G kiosk pi
mkdir /var/log/kiosk
ln -s /var/log/kiosk/kiosk.log /home/pi/kiosk.log
chown -R pi:kiosk /var/log/kiosk
addgroup watchdog
usermod -a -G watchdog pi
service cups restart
apt-get --yes install python3-pip
sed -i '/^\[global\]$/a break-system-packages = true' /etc/pip.conf

#apt-get --yes --allow-downgrades --allow-remove-essential --allow-change-held-packages install python3-pip
echo 'KERNEL=="watchdog", MODE="0660", GROUP="watchdog"' > /etc/udev/rules.d/60-watchdog.rules
sed -i '/^#NTP=.*/a FallbackNTP=laiks.egl.local' /etc/systemd/timesyncd.conf
echo '10.100.20.104   laiks.egl.local' >> /etc/hosts
pip3 --no-input install requests pyserial configparser
pip3 --no-input install pycups
#/usr/sbin/shutdown -r now
