import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
 
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE0)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
 
# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)
 
while True:
    print('Raw ADC Value: ', round(chan.value, 2))
    print('ADC Voltage: ' + str(round(chan.voltage, 2)) + 'V')
    print('Moisture level: ' + str(round(100-((chan.voltage*100)/3.3),1)) + '%') 
    time.sleep(2)
