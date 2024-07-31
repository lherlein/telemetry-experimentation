from machine import Pin, I2C, PWM, UART
from lib.mpu6050 import MPU6050
import time
import math
import machine
import socket

def calibrateSensors():
  sealevel = 0
  phiNormal = 0
  thetaNormal = 0
  # Average N readings
  N = 100
  for i in range(N):
    sealevel += bmp.pressure
    imuData = readIMU()
    orientation = calcAngles(imuData)
    phiNormal += orientation[0]
    thetaNormal += orientation[1]
    time.sleep_ms(10)

  bmp.sealevel = sealevel/N
  return [phiNormal/N, thetaNormal/N, sealevel/N]

def readIMU():
  # Get IMU Data
  accelData = mpu.read_accel_data()
  gyroData = mpu.read_gyro_data()

  return [accelData, gyroData]

def calcAngles(imuData): # Not entirely sure this will work when in flight

  # Get Accelerometer Data
  accelData = imuData[0]

  phi = math.atan2(accelData[1], accelData[2])
  theta = math.atan2(accelData[0], accelData[2])

  return [phi, theta]

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

rx_pin = Pin(13)
tx_pin = Pin(15)

uart = UART(0, baudrate=115200, rx=rx_pin, tx=tx_pin)

# Define I2C Busses
#i2c_mpu = I2C(1, sda=mpuSDA, scl=mpuSCL)

# Define Sensors
#mpu = MPU6050(i2c_mpu)

# Calibrate Everything
#normalValues = calibrateSensors()

# Wake up MPU
#mpu.wake()

# Check if connected to wifi

# If not, connect to wifi

# Establish UDP Client

ip = do_connect()

UDP_IP = ip
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Main Loop
while True:
  # Read IMU Data
  # Calculate Angles

  # Send req to server for setpoint - include IMU data as bonus

  # Wait for server response - includes setpoint for PID

  # Pass setpoint to Flight Controller - UART connected to FC


  # For now, just print the udp message
  data, addr = sock.recvfrom(1024)
  print(data)