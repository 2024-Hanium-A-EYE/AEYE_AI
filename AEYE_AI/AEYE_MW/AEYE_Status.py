from flask import jsonify, request, Blueprint
from datetime import datetime
from colorama import Fore, Back, Style
import requests

mw_status = Blueprint('AEYE_MW_Status', __name__)
i_am_mw_status = 'OpticNet MW - Status'

import logging
logging.basicConfig(level=logging.INFO)

def print_log(status, whoami, mw, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "active" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + str(message) +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + str(message) +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        
@mw_status.route('/mw/status', methods = ['POST'])
def aeye_mw_status() :

    i_am_client    = request.form.get('whoami')
    status_client  = request.form.get('status')
    message_client = request.form.get('message')

    print_log('active', i_am_client, i_am_mw_status, message_client)

    if i_am_client :
        if status_client:
            if message_client :
                url = 'http://127.0.0.1:2000/hal/status/'
                print_log('active', i_am_client, i_am_mw_status, "requst data to : {}".format(url))
                data={
                    'whoami' : i_am_mw_status,
                    'message': message_client,
                    'status' : status_client
                }
                response = requests.post(url, data=data)
                
                if response.status_code == 200:
                    message="Succed to send data to : {}".format(url)
                    print_log('active', i_am_mw_status, i_am_mw_status, message)
                    data={
                        'whoami' : i_am_mw_status,
                        'message': message
                    }
                    return jsonify(data), 200
                else:
                    message="Failed to send data to : {}".format(url)
                    print_log('error', i_am_mw_status, i_am_mw_status, message)
                    data={
                        'whoami' : i_am_mw_status,
                        'message': message
                    }
                    return jsonify(data), 400
            else :
                print_log('error', i_am_mw_status, i_am_mw_status, "Failed to Receive message")
                return 400
        else:
            print_log('error', i_am_mw_status, i_am_mw_status, "Failed to Receive status")
            return 400
    else:
        print_log('error', i_am_client, i_am_mw_status, "Failed to Receive from : {}".format(i_am_client))
        return 400




