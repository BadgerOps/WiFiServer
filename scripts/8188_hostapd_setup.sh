#!/bin/bash

error() {
  printf '\E[31m'; echo "$@"; printf '\E[0m'
}

info() {
  printf '\E[32m'; echo "$@"; printf '\E[0m'
}

BASE=$(mktemp -d /tmp/setup_XXX)

if [ $UID != 0 ] ;
    then
        error "Please run this script as root"
        info "Usage: 'sudo bash 8188_hostapd_setup.sh'";
    exit 1;
fi

info "Installing some necessary software"
    sudo apt-get update
    sudo apt-get install -y git python-pip dnsmasq htop iw

info "Stopping unecessary services"
    sudo service dnsmasq stop

info "Done, moving on"

info "Changing to $BASE"
    cd $BASE

info "Building Hostapd from source"
    wget https://github.com/jenssegers/RTL8188-hostapd/archive/v1.1.tar.gz
    tar -zxvf v1.1.tar.gz
    cd RTL8188-hostapd-1.1/hostapd
    sudo make
    sudo make install

info "Ensuring Hostapd is not running"
    sudo service hostapd stop

info "Getting WiFiServer & dependencies"
    sudo mkdir /opt/wifiserver
    cd /opt/wifiserver
    git clone https://github.com/Badger32d/WiFiServer.git
    cd WiFiServer
    sudo pip install -r requirements.txt
    sudo cp conf/hostapd.conf /etc/hostapd/hostapd.conf
    sudo cp conf/dnsmasq.conf /etc/dnsmasq.conf

error "Setup Complete"
