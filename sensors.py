import serial

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

def read_light(bus, addr):
  """Reads light value for each plant"""

  #Read data from I2C interface
  data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def read_moisture(plant):
    """ returns moisture level for each plant """
    moisture = None
    ser = serial.Serial("/dev/ttyACM0", 9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600

    for _ in range(20):
        ser.write(b'%d'%plant)
        ser.flush()
        if ser.in_waiting > 0:
            val = ser.readline()
            val = val.replace(b'\r', b'')
            val = val.replace(b'\n', b'')
            if val == b'':
                continue
            moisture = ord(val)
            break
        time.sleep(1)

    return moisture
