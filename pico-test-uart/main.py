from machine import Pin, UART
import time

led = Pin("LED", Pin.OUT)

rx_pin = Pin(1)
tx_pin = Pin(0)

uart = UART(0, baudrate=115200, rx=rx_pin, tx=tx_pin)

while True:

  if uart.any():
    data = uart.readline()
    print(data)
    try:
      data = data.decode('utf-8').strip()
    except:
      pass
    if data:
      if data == "high":
        led.on()
      elif data == "low":
        led.off()