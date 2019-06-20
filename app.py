#!/usr/bin/env python3
# coding: UTF-8

import json
import requests
from time import sleep
import os
from os.path import join, dirname
from CO2Meter import *
from datetime import datetime
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ["TOKEN"]
send_url = os.environ["SEND_URL"]
user_agent = os.environ["USER_AGENT"]

def main():
    sensor = CO2Meter('/dev/hidraw0')

    headers = {
        'User-Agent': user_agent
    }

    print('started.')

    count = 0

    while True:
        data = sensor.get_data()

        print(data)

        if 'temperature' not in data or 'co2' not in data:
            print('no data')
            if count > 10:
                print('time out')
                break
            sleep(3)
            count += 1
            continue

        timestamp = datetime.now().strftime('%s')

        post_data = {
            'token': token,
            'co2': str(data['co2']),
            'temperature': str(data['temperature']),
            'timestamp': str(timestamp)
        }

        print(post_data)
        response = requests.post(send_url, headers=headers, data=post_data)

        break

if __name__=='__main__':
    main()
