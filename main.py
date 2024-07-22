from machine import Pin, I2C
from bmp180 import BMP180
from mpu6050 import MPU6050
import time
import math

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

def readBMP():
  # Get BMP Data
  pressure = bmp.pressure
  altitude = bmp.altitude
  temperature = bmp.temperature

  return [pressure, altitude, temperature]

def calcAngles(imuData): # Not entirely sure this will work when in flight

  # Get Accelerometer Data
  accelData = imuData[0]

  phi = math.atan2(accelData[1], accelData[2])
  theta = math.atan2(accelData[0], accelData[2])

  return [phi, theta]

print("Starting...")

# Define Pins
mpuSDA = Pin(14) # i2c 1
mpuSCL = Pin(15)

bmpSDA = Pin(16) # i2c 0
bmpSCL = Pin(17)

# Define I2C Busses
i2c_mpu = I2C(1, sda=mpuSDA, scl=mpuSCL)
i2c_bmp = I2C(0, sda=bmpSDA, scl=bmpSCL)

# Define Sensors
bmp = BMP180(i2c_bmp)
mpu = MPU6050(i2c_mpu)

# Calibrate Everything
print("Calibrating Sensors")
normalValues = calibrateSensors()

# Wake up MPU
print("Waking up MPU")
mpu.wake()

count = 0
while True:
  # Read IMU Data
  imuData = readIMU()

  # Read BMP Data
  bmpData = readBMP()

  # Calculate Angles
  angles = calcAngles(imuData)

  # Print Data
  print("IMU Data: ", imuData)
  print("BMP Data: ", bmpData)
  print("Angles: ", angles)

  time.sleep(.5)