#!/bin/sh

# This file sets up the RPi settings to allow I2C and Camera functions

# INSTRUCTIONS TO RUN FILE
# cd into Desktop
# sudo bash Raspi_Setup.sh

sudo raspi-config nonint do_i2c 0     # Enable i2c
sudo raspi-config nonint do_camera 0  # Enable Camera
reboot
