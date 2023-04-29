# Set up Instructions for Fresh Pi OS, install all into the init.d folder. Default I2C is 0x76
# 
# apt install sudo
# sudo apt install  python3
#                   -y python3-picamera2
#                   git
#                   flex
#                   bison
#                   make
#                   -y ffmpeg
#                   time
#                   python3-smbus
#
# pip3 install  gps
#               mpu6050-raspberrypi
#                   
# sudo apt-get install gpsd gpsd-clients
#
# curl https://get.pimoroni.com/bme680 | bash
#
# sudo raspi-config         # # Enable Glamour in Pi Settings
#
# git pull origin main      # # Updates code
#

import csv
import time
import datetime
import board
import busio
import adafruit_gps
import adafruit_mpu6050
import bme680
from subprocess import PIPE, Popen

uart = busio.UART(boart.TX, board.RX, buadrate= 9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0") #Turn on basic GGA and RMC info
gps.send_command(b"PMTK220,1000") #Set update rate to 1Hz

try:
    bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IndexError):
    bme = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

now = datetime.datetime.now()
date_integer = int(now.strftime('%d'))
savedata = f"data_{date_integer}.csv"

with open(savedata, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['Time (s)', 'Count', 'Latitude (Degrees)', 'Latitude (Minutes)', 'Longitude (Degrees)', 'Longitude (Minutes)', 'Altitude (m)', 'Ground Speed (Knots)', 'No. of Satellites', 'Pressure (Pa)', 'Temperature (C)', 'Humidity', 'Acceleration x (m/s^2)','Acceleration y (m/s^2)','Acceleration z (m/s^2)', 'Gyroscope x (rad/s)','Gyroscope y (rad/s)','Gyroscope z (rad/s)', 'mpu-6050 Temperature (C)'])

    count = 0
    while True:
        if gps.has_fix:
            writer.writerow([time.monotonic(), count, gps.latitude_degrees, gps.latitude_minutes, gps.longitude_degrees, gps.longitude_minutes, gps.altitude_m, gps.speed_knots, gps.satellites, bme.data.pressure, bme.data.temperature, bme.data.humidity, mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2], mpu.gyro[0], mpu.gyro[1], mpu.gyro[2], mpu.temperature])
        else:
            continue

        count += 1
        time.sleep(1)