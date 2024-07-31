import socket
from machine import Pin, UART

def do_connect():
  import network
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('<ssid>', '<key>')
    while not sta_if.isconnected():
        pass
  print('network config:', sta_if.ifconfig())
  return sta_if.ifconfig()[0]

# Define Pins

rx_pin = Pin(3)
tx_pin = Pin(1)

# Define UART

uart = UART(0, baudrate=115200, rx=rx_pin, tx=tx_pin)

# Establish UDP socket


ip = do_connect()

UDP_IP = ip
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  uart.write(data)