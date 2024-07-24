from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import socket
import imu
import json
import time

setScreenColor(0x111111)

# Replace 'SSID' and 'Password' with your WiFi network's SSID and password
wifiCfg.doConnect('LLUI-Guest', 'WPA2-Guest')
imu0 = imu.IMU()

ip_address_computer = '10.129.20.192'
port = 1234

# Frequency in Hz
frequency = 50
interval = 1.0 / frequency

udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

connecting_message = 'Connecting to WiFi...'
attempts = 0

while not wifiCfg.wlan_sta.isconnected():
    lcd.clear()
    lcd.print(connecting_message, 0, 20, 0xFFFFFF)
    asterisks = '*' * ((attempts % 4) + 1)  # Cycle through 1 to 4 asterisks
    lcd.print(asterisks, 150, 20, 0xFFFFFF)  # Update asterisks on the screen
    time.sleep(1)
    attempts += 1

lcd.clear()
lcd.print('Connected to WiFi', 10, 10, 0xFFFFFF)

while True:
    accel_x = imu0.acceleration[0]
    accel_y = imu0.acceleration[1]
    accel_z = imu0.acceleration[2]
    ypr_yaw = imu0.ypr[0]
    ypr_pitch = imu0.ypr[1]
    ypr_roll = imu0.ypr[2]
    gyro_x = imu0.gyro[0]
    gyro_y = imu0.gyro[1]
    gyro_z = imu0.gyro[2]

    # Create a JSON object with accelerometer, YPR, and gyroscope data
    imu_data = {
        'linear_acceleration': {
            'x': accel_x,
            'y': accel_y,
            'z': accel_z
        },
        'orientation': {
            'yaw': ypr_yaw
            'pitch': ypr_pitch,
            'roll': ypr_roll
        },
        'angular_velocity': {
            'x': gyro_x,
            'y': gyro_y,
            'z': gyro_z
        }
    }
    
    # Convert the JSON object to a string
    imu_data_str = json.dumps(imu_data)

    # Send the data
    udpsocket.sendto(imu_data_str.encode(), (ip_address_computer, port))
    
    # Display the data on the screen
    lcd.clear()
    lcd.print('accel_x: {:.2f}'.format(accel_x), 10, 10, 0xFFFFFF)
    lcd.print('accel_y: {:.2f}'.format(accel_y), 10, 30, 0xFFFFFF)
    lcd.print('accel_z: {:.2f}'.format(accel_z), 10, 50, 0xFFFFFF)
    lcd.print('pitch: {:.2f}'.format(ypr_pitch), 10, 70, 0xFFFFFF)
    lcd.print('roll: {:.2f}'.format(ypr_roll), 10, 90, 0xFFFFFF)
    lcd.print('gyro_x: {:.2f}'.format(gyro_x), 10, 110, 0xFFFFFF)
    lcd.print('gyro_y: {:.2f}'.format(gyro_y), 10, 130, 0xFFFFFF)
    lcd.print('gyro_z: {:.2f}'.format(gyro_z), 10, 150, 0xFFFFFF)

    # Wait for the next interval
    time.sleep(interval)
