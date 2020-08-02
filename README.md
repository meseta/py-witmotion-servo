# py-witmotion-servo
This is a Python for the Witmotion Servo Controller board's native USB port.

Even though the board has a USB port, the manufacturer does not supply an SDK for it, and their manual suggests that you use a USB-serial adapter to plug into the board's UART port instead for PC control. The manufacturer does provide a simple Windows utility but not the source. Therefore I have [reverse-engineered the protocol](https://medium.com/@meseta/witmotion-servo-control-reverse-engineering-d5acf7ce528f) and provideda a Python package.

# Installation
You can install from this git repo:
```sh
pip install git+https://github.com/meseta/py-witmotion-servo.git
```

py-witmotion-servo depends on [cython-hidapi](https://github.com/trezor/cython-hidapi)

# Usage
## Basic usage example

```py
import time
from witmotionservo import WitmotionServo

# connect to the first witmotion device found
wit = WitmotionServo()
wit.open()

# set channel 0 servo to 1000us position
wit.set_position(0, 1000)
time.sleep(1)

# ... and then to 1500us
wit.set_position(0, 1500)

# close the connection
wit.close()
```

## Multiple boards connected
```py
import sys
from witmotionservo import WitmotionServo

# fetch a list of connected devices
devices = WitmotionServo.list_devices()

if not devices:
  print("No devices connected")
  sys.exit()

# select the last device
selected_device = devices[-1]

# connect to the last one
wit = WitmotionServo().open(selected_device)

# do nothing but send heartbeats
while True:
  wit.heartbeat()
  time.sleep(1)
```
