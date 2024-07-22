from machine import Pin
import time
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests

print("Starting...")

# Fill in your network name (ssid) and password here:
ssid = ''
password = ''

def connect():
  #Connect to WLAN
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)
  while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep(1)
  print(wlan.ifconfig())

try:
  print("Connecting to network...")
  connect()
  print("Connected to network")
except Exception as e:
  print("Error connecting to network: ", e)
  break

# Example 1. Make a GET request for google.com and print HTML
# Print the html content from google.com
print("1. Querying google.com:")
r = urequests.get("http://www.google.com")
print(r.content)


led = Pin(25, Pin.OUT)

count = 0
while True:
  led.toggle()
  print("Hello, World! ", count)
  count += 1
  time.sleep(0.5)