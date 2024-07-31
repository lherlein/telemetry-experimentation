from machine import Pin, UART
import time

rx_pin = Pin(13)
tx_pin = Pin(15)

uart = UART(0, baudrate=115200, rx=rx_pin, tx=tx_pin)

while True:
  uart.write("high")
  time.sleep(1)
  uart.write("low")
  time.sleep(1)