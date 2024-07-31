# Network Communications Experimentation

I need to learn about device-device communications over a network in order to build the communications/telemetry modules for my drones. This repo holds that effort.

## Moving to the ESP8266-12F Board for Dev

I could not easily make the ESP8266-01 board work alongside the Pico board, so I am moving to the ESP8266-12F board (ESP8266 chip with decent pinout). 

Ampy does work to communicate with the ESP8266 board, you just need to turn off the board's automatic `osDebug` feature so that debug outputs don't confuse Ampy. Follow [this](https://pythonforundergradengineers.com/upload-py-files-to-esp8266-running-micropython.html) guide for instructions on how to do that.  

## Communicating with the RPi Pico && ESP8266

Ampy turns your chosen dev environment into a micropython IDE. 

Download Ampy with pip in your virtual environment:

```
pip3 install adafruit-ampy
```

Plug in your pico, identify the USB port it was attached to. The pico will be attached to a device, so `/dev/ttyXXX`. Run `ls /dev/tty*` with the pico plugged in and then without, and find the port that changes. You could also check the `dmesg` logs, with `sudo dmesg -tail`. This will output something like:

```
[] usb 3-3.4.3: new full-speed USB device number 26 using xhci_hcd
[] usb 3-3.4.3: New USB device found, idVendor=2e8a, idProduct=0005, bcdDevice= 1.00
[] usb 3-3.4.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[] usb 3-3.4.3: Product: Board in FS mode
[] usb 3-3.4.3: Manufacturer: MicroPython
[] usb 3-3.4.3: SerialNumber: ...
[] cdc_acm 3-3.4.3:1.0: ttyACM0: USB ACM device
```

Where the device the pico was enumerated to is at the end. This device already has micropython on it. 

Once ampy is installed and the device ID is found, check that ampy has access to the port with the ls command. If there is no access, but you have verified that the pico is plugged in and enumerated, then you must give access to the device. WHILE IN THE VIRTUAL ENVIRONMENT: `sudo chmod 777 /dev/ttyXXX`. Then try again.

## Ampy Commands


List files on Pico:

```
ampy --port /dev/ttyXXX ls
```

Run a file: 

```
ampy --port /dev/ttyXXX run main.py
```

Upload a file:

```
ampy --port /dev/ttyXXXX put main.py
```

Port seems to be (for me) `/dev/ttyACM0`

### Env Setup

```
source telem/bin/activate
```

```
deactivate
```
