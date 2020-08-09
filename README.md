# Plant-e

## Installation

It is recommended to use VSCode as an IDE, along with [micropy-cli](https://github.com/BradenM/micropy-cli) as it provides:

* Linting
* Dependency management
* Version Control System (VCS) compatibility

To set up the project on a local machine for development:

```
# Clone project
git clone https://github.com/LoJunKai/Plant-e.git
cd Plant-e

# Create virtual environment
python3 -m venv env
source env/bin/activate

# Install packages
python3 -m pip install micropy-cli pylint

# Set up Micropy environment locally
micropy
```

## Flashing Firmware

This project uses [custom MicroPython firmware](https://github.com/melvinkokxw/micropython) with camera and BLE support. The firmware was compiled using esp-idf 4.x (hash 4c81978a3e2220674a432a588292a4c860eef27b).

The firmware is included in the `firmware` folder. To flash it to the board:

```
# Install esptool
python3 -m pip install esptool

# Flash the firmware
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 micropython_8da40ba_esp32_idf4.x_ble_camera.bin
```

## Reference Materials

- [ESP32 MicroPython Firmware Download](https://micropython.org/download/esp32/)
- [Flashing with esptool](https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/)
- [Using uPyCraft](https://randomnerdtutorials.com/getting-started-micropython-esp32-esp8266/)

How to connect FTDI to ESP32:
![Image taken from https://randomnerdtutorials.com/esp32-cam-video-streaming-face-recognition-arduino-ide/](https://github.com/LoJunKai/Plant-e/blob/master/FTDI%20to%20ESP32%20Connection.png)
