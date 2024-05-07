# kiosk_4
Test report kiosk 4
sudo apt-get update && sudo apt-get upgrade -y reboot computer - it looks like installing git without reboot messes up apt

Set BC reader interface to USB_COM

Create directory for kiosk on RaspberryPI: sudo mkdir /opt/kiosk
Copy files there
Create group kiosk, set ownership to pi:kiosk (sudo chown pi:kiosk
Make scripts executable:
cd /opt/kiosk chmod a+x *.py *.sh *.ini
kiosk.ini should have execute permission!!!

Launch configuration script. This will install required libraries and configure system.
Check with sudo raspi_config: sudo ./preppi.sh
