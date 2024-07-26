from machine import Pin, I2C, PWM, UART
from bmp180 import BMP180
from mpu6050 import MPU6050
from controller import PID, PI
import time
import math
import machine
import _thread

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

def rad2deg(rad):
  return rad * 180 / math.pi

def deg2rad(deg):
  return deg * math.pi / 180

def ms2ns(ms):
  return ms * 1000000

def pos2u16(pos):
  # get value between 0 and 100 representing servo position
  # return value between 0 and 65535 representing duty cycle between 0 and 100%
  # MUST KEEP RETURN BETWEEN 5-10% DUTY CYCLE

  # 0 input -> 65535*0.05
  # 100 input -> 65535*0.1

  posPercent = pos / 100

  # convert posPercent to duty cycle within bounds
  duty = 0.05 + posPercent * 0.05

  return int(duty * 65535)

#Function to handle reading from the uart serial to a buffer
def SerialRead(mode):
  SerialRecv = ""
  if mode == "0" :
    SerialRecv=str(uart.readline())
  else:
    SerialRecv=str(uart.read(mode))
  #replace generates less errors than .decode("utf-8")
  SerialRecv=SerialRecv.replace("b'", "")
  SerialRecv=SerialRecv.replace("\\r", "")
  SerialRecv=SerialRecv.replace("\\n", "\n")
  SerialRecv=SerialRecv.replace("'", "")
  return SerialRecv


print("Starting...")

# Define Pins
mpuSDA = Pin(14) # i2c 1
mpuSCL = Pin(15)

bmpSDA = Pin(16) # i2c 0
bmpSCL = Pin(17)

wifiRx = Pin(0)
wifiTx = Pin(1)

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

# Start Webserver
print("Starting Webserver")
#Set variables
recv=""
recv_buf="" 
# wifi credentials (if needed)
wifi_ssid = ("sofia")
wifi_password = ("19631964")

print ("Setting up Webserver...")
uart = UART(0,115200, tx=Pin(0), rx=Pin(1)) # uart on uart1 with baud of 115200
time.sleep(2)
# Connect to wifi, this only needs to run once, ESP will retain the CWMODE and wifi details and reconnect after power cycle, leave commented out unless this has been run once.
print ("  - Setting AP Mode...")
uart.write('AT+CWMODE=1'+'\r\n')
time.sleep(2)
print ("  - Connecting to WiFi...")
uart.write('AT+CWJAP="'+wifi_ssid+'","'+wifi_password+'"'+'\r\n')
time.sleep(5)
print ("  - Setting Connection Mode...")
uart.write('AT+CIPMUX=1'+'\r\n')
time.sleep(2)
print ("  - Starting Webserver..")
uart.write('AT+CIPSERVER=1,80'+'\r\n') #Start webserver on port 80
time.sleep(2)
# Get local IP and print result
uart.write('AT+CIFSR'+'\r\n')
time.sleep(0.5)
ipRes = uart.read()
print(ipRes)

print ("Webserver Ready!")
print("")

# Main Loop
while True:
  # Read IMU Data
  imuData = readIMU()

  # Read BMP Data
  bmpData = readBMP()

  # Calculate Angles
  angles = calcAngles(imuData)
  angles = [rad2deg(angles[0]), rad2deg(angles[1])]

  # Craft Data String
  data = "Angles: " + str(angles) + "\n" + "Pressure: " + str(bmpData[0]) + "\n" + "Altitude: " + str(bmpData[1]) + "\n" + "Temperature: " + str(bmpData[2]) + "\n"

  print(data)

  # Get Data Length
  dataLength = len(data)

  uart.write('AT+CIPSEND=0,'+str(dataLength)+'\r\n')
  time.sleep(0.1)
  uart.write(data)

  while True:
    #read a byte from serial into the buffer
    recv=SerialRead(1)
    recv_buf=recv_buf+recv

    print(recv)
    time.sleep(0.1)
