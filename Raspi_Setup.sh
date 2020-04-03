#!/bin/sh

sudo raspi-config nonint do_i2c 0     # Enable i2c
sudo raspi-config nonint do_camera 0  # Enable Camera
reboot