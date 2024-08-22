from flask import Flask
from AEYE import create_aeye_opticnet_framework
import click
import requests

def print_log_to_maintainer(status, whoami, message):
    url = 'http://127.0.0.1:2000/api/log-printer/'
    data={
        'whoami'    : whoami,
        'operation' : 'Maintainer Server',
        'status'    : status,
        'message'   : message
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        pass
    else:
        pass

framework = create_aeye_opticnet_framework()

if __name__ == "__main__":
    framework.run(host='0.0.0.0', port=2000, debug=True)
    print_log_to_maintainer("active", "AEYE AI", "AEYE AI Server is alive!")
