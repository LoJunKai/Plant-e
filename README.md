# Plant-e

## Installation

It is recommended to use VSCode as an IDE, along with [micropy-cli](https://github.com/BradenM/micropy-cli) as it provides:

* Linting
* Dependency management
* Version Control System (VCS) compatibility

To set up the project on a local machine for development:

```bash
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

```bash
# Install esptool
python3 -m pip install esptool

# Only needed if flashing for the first time
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# Flash the firmware
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 micropython_3a9d948_esp32_idf4.x_ble_camera.bin
```

## Usage

Create `config.py` in the root directory with the following content:

```python
wifi_config = {
    "ssid":"<wifi ssid>",
    "password":"<wifi password>"
}
```

1. Run upycraft
2. Plug in FTDI and press connect - flash if necessary
3. Take out the connection between GND and IO0 and press the reset button - unplug and plug in the FTDI if necessary
4. Press connect on upycraft
5. DownloadAndRun all the files to load it into ESP32
6. To over-write files, press Stop > DownloadAndRun > reset button on esp32


## Reference Materials

- [ESP32 MicroPython Firmware Download](https://micropython.org/download/esp32/)
- [Flashing with esptool](https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/)
- [Using uPyCraft](https://randomnerdtutorials.com/getting-started-micropython-esp32-esp8266/)

How to connect FTDI to ESP32:
![Image taken from https://randomnerdtutorials.com/esp32-cam-video-streaming-face-recognition-arduino-ide/](https://github.com/LoJunKai/Plant-e/blob/master/FTDI%20to%20ESP32%20Connection.png)
