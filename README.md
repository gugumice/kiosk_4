# kiosk_4
Test report kiosk 4
sudo apt-get update && sudo apt-get upgrade -y reboot computer - it looks like installing git without reboot messes up apt

Set BC reader interface to USB_COM: sudo apt-get install git

Create directory for kiosk on RaspberryPI: sudo mkdir /opt/kiosk
Create group kiosk, set ownership to pi:kiosk (sudo chown pi:kiosk

Downnload as zip or /opt/kiosk git clone /opt/kiosk/

Make scripts executable:
cd /opt/kiosk chmod a+x *.py *.sh *.ini
kiosk.ini should have execute permission!!!

Launch configuration script. This will install required libraries and configure system.
Check with sudo raspi_config: sudo ./preppi.sh
