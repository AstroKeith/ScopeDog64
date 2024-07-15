#!/bin/sh

echo "ScopeDog install"
echo "This will take some time! ( > 30 minutes)"
echo " "
echo "*****************************************************************************"
#sudo rpi-update -y

sudo apt update
sudo apt upgrade -y
echo "Pi update done"
HOME=/home/scopedog

echo "***********************************"
echo " "
echo 'dtoverlay=uart2' | sudo tee -a /boot/firmware/config.txt > /dev/null
echo " "
echo "**********************************"


sudo apt-get install -y libcairo2-dev libnetpbm11-dev netpbm libpng-dev libjpeg-dev zlib1g-dev libbz2-dev swig libcfitsio-dev
# sudo -u efinder python3 -m pip install --upgrade pip

sudo apt install -y python3-fitsio
sudo apt install -y imagemagick
sudo apt install -y python3-skyfield
sudo apt install -y python3-pil.imagetk


#Lets install the Phidgets dependencies
curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash - &&\ sudo apt-get install -y libphidget22
sudo apt-get install -y libphidget22-dev
sudo apt-get install -y libphidget22extra
sudo apt-get install -y phidget22admin
sudo apt-get install -y phidget22networkserver

python -m venv /home/scopedog/venv-scopedog --system-site-packages

echo "ScopeDog virtual environment setup"
venv-scopedog/bin/python venv-scopedog/bin/pip install git+https://github.com/esa/tetra3.gitvenv-scopedog/bin/python venv-scopedog/bin/pip install astropy pyfits
venv-scopedog/bin/python venv-scopedog/bin/pip install adafruit-circuitpython-ina260

# Lets install the astrometry.net package
cd $HOME
sudo -u scopedog git clone https://github.com/dstndstn/astrometry.net.git
echo ""

cd $HOME/astrometry.net
make
make py
make extra
sudo make install

sudo sh -c "echo export PATH=$PATH:/usr/local/astrometry/bin >> /etc/profile"

cd /usr/local/astrometry/data
sudo wget http://data.astrometry.net/4100/index-4107.fits
sudo wget http://data.astrometry.net/4100/index-4108.fits
sudo wget http://data.astrometry.net/4100/index-4109.fits
sudo wget http://data.astrometry.net/4100/index-4110.fits
sudo wget http://data.astrometry.net/4100/index-4111.fits

sudo mkdir /usr/local/astrometry/annotate_data
cd /usr/local/astrometry/annotate_data
sudo wget http://data.astrometry.net/hd.fits
sudo wget http://data.astrometry.net/hip.fits
sudo wget https://github.com/dstndstn/astrometry.net/tree/main/catalogs/abell-all.fits

echo "Astrometry.net installed"

cd $HOME

sudo -u scopedog git clone https://github.com/AstroKeith/ScopeDog64.git
sudo cp ScopeDog64/ScopeDog_m3ef_Bookworm/99-libphidget22.rules /etc/udev
venv-scopedog/bin/python venv-scopedog/bin/pip install phidget22

echo "Phidgets installed"

# Lets install the ASI Camera dependencies
cd ScopeDog64
tar xf ASI_linux_mac_SDK_V1.31.tar.bz2
cd ASI_linux_mac_SDK_V1.31/lib
sudo mkdir /lib/zwoasi
sudo mkdir /lib/zwoasi/armv8
sudo cp armv8/*.* /lib/zwoasi/armv8
sudo install asi.rules /lib/udev/rules.d
cd $HOME
venv-scopedog/bin/python venv-scopedog/bin/pip install zwoasi

echo "Camera support installed"

# Install the ScopeDog code
cd $HOME
echo "tmpfs /var/tmp tmpfs nodev,nosuid,size=100M 0 0" | sudo tee -a /etc/fstab > /dev/null

mkdir /home/scopedog/Solver
mkdir /home/scopedog/Solver/Stills

echo ""
cp /home/scopedog/ScopeDog64/ScopeDog_m3ef_Bookworm/*.* /home/scopedog
mv *.jp* Solver

sudo apt install -y samba samba-common-bin
sudo tee -a /etc/samba/smb.conf > /dev/null <<EOT
[efindershare]
path = /home/scopedog
writeable=Yes
create mask=0777
directory mask=0777
public=no
EOT
username="scopedog"
pass="scopedog"
(echo $pass; sleep 1; echo $pass) | sudo smbpasswd -a -s $username
sudo systemctl restart smbd

echo "ScopeDog files installed"

# Lets set up the webpage server
sudo apt-get install -y apache2
sudo apt-get install -y php8.2
sudo chmod a+rwx /home/scopedog
sudo cp ScopeDog64/ScopeDog_m3ef_Bookworm/www/*.* /var/www/html
sudo mv /var/www/html/index.html /var/www/html/apacheindex.html

# Set it up to autostart on boot
mkdir /home/scopedog/.config/autostart
cp /home/scopedog/scopedog.desktop /home/scopedog/.config/autostart

# Set up the Pi configuration
sudo raspi-config nonint do_vnc 0
sudo raspi-config nonint do_hostname scopedogmk3
sudo raspi-config nonint do_blanking 1
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_serial_hw 0
sudo raspi-config nonint do_serial_cons 1
sudo raspi-config nonint do_vnc_resolution 1920x1080

echo "Done, after the reboot vnc and ssh should be available at 'scopedogmk3.local'"
