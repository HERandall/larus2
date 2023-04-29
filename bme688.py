import time
import bme680
import csv
from subprocess import PIPE, Popen

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

#Oversampling Settings

def bme_setup():
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    return

def get_temperature():
    temperature = sensor.data.temperature
    return temperature

def get_pressure():
    pressure = sensor.data.pressure
    return pressure

def get_humidity():
    humidity = sensor.data.humidity
    return humidity