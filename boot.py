import network
import utime
import ntptime
import urequests

import config
import webcam


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    start = utime.time()
    timed_out = False

    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(config.wifi_config["ssid"],
                       config.wifi_config["password"])
        while not sta_if.isconnected() and not timed_out:
            if utime.time() - start >= 20:
                timed_out = True
            else:
                pass

    if sta_if.isconnected():
        ntptime.settime()
        print("network config:", sta_if.ifconfig())
        r = urequests.get("http://icanhazip.com")
        print(r.text)
    else:
        print("internet not available")


do_connect()

webcam.run()
