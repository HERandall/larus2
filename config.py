# Set up Instructions for Fresh Pi OS, install all into the init.d folder. Default I2C is 0x76
# 
# sudo apt install  python3
#                   -y python3-picamera2
#                   git
#                   flex
#                   bison
#                   make
#                   -y ffmpeg
#                   time
#                   python3-smbus
#                   vim
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
# cd /etc/init.d
# ssh-keygen
# cat ~/.ssh/id_rsa.pub     # # Link to Github repo
#
# sudo apt install -y curl git
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
import os
from picamera2 import Picamera2, Preview
from subprocess import PIPE, Popen

now = datetime.datetime.now()
date_integer = int(now.strftime('%d'))

folder = f"{date_integer}"
path = os.path.join(os.path.expanduser("-"), "Documents", folder)
os.makedirs(path, exist_ok=True)
savedata = os.path.join(path, (f"data_{date_integer}.csv"))

uart = busio.UART(boart.TX, board.RX, buadrate= 9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0") #Turn on basic GGA and RMC info
gps.send_command(b"PMTK220,1000") #Set update rate to 1Hz

try:
    bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IndexError):
    bme = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

bme.set_humidity_oversample(bme680.OS_2X)
bme.set_pressure_oversample(bme680.OS_4X)
bme.set_temperature_oversample(bme680.OS_8X)
bme.set_filter(bme680.FILTER_SIZE_3)

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

with open(savedata, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(
        [
            'Time (s)', 
            'Count', 
            'Latitude (Degrees)', 
            'Latitude (Minutes)', 
            'Longitude (Degrees)', 
            'Longitude (Minutes)', 
            'Altitude (m)', 
            'Ground Speed (Knots)', 
            'No. of Satellites', 
            'Pressure (Pa)', 
            'Temperature (C)', 
            'Humidity', 
            'Acceleration x (m/s^2)',
            'Acceleration y (m/s^2)',
            'Acceleration z (m/s^2)', 
            'Gyroscope x (rad/s)',
            'Gyroscope y (rad/s)',
            'Gyroscope z (rad/s)', 
            'mpu-6050 Temperature (C)',
            'Image Name'
        ]
    )

    count = 0
    while True:
        image = picam2.capture_file(f"image_{count}.jpg")
        if gps.has_fix:
            lat_deg = gps.latitude_degrees, 
            lat_min = gps.latitude_minutes, 
            long_deg = gps.longitude_degrees, 
            long_min = gps.longitude_minutes, 
            alt = gps.altitude_m, 
            speed = gps.speed_knots, 
            satno = gps.satellites
        else:
            lat_deg = 0,
            lat_min = 0,
            long_deg = 0,
            long_min = 0,
            alt = 0,
            speed = 0, 
            satno = 0,
            continue

        writer.writerow(
            [
                time.monotonic(), 
                count, 
                lat_deg,
                lat_min,
                long_deg,
                long_min,
                alt,
                speed,
                satno,
                bme.data.pressure, 
                bme.data.temperature, 
                bme.data.humidity, 
                mpu.acceleration[0], 
                mpu.acceleration[1], 
                mpu.acceleration[2], 
                mpu.gyro[0], 
                mpu.gyro[1], 
                mpu.gyro[2], 
                mpu.temperature,
                image
            ]
        )
        
        count += 1
        time.sleep(1)