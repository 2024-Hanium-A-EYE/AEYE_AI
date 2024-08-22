from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os

api_LP = Blueprint('application_layer_LP', __name__)

UPLOAD_FOLDER = 'tmp_chunk'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


import logging
logging.basicConfig(level=logging.INFO)

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "active" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[OpticNet - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[OpticNet - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
   

i_am_pl = 'OpticNet - API LP'

aeye_net_oper       = 'http://network_operator_container:3000'
print_to_maintainer = '/mw/print-to-maintainer/'

@api_LP.route('/api/log-printer/', methods = ['POST'])
def aeye_log_printer() :

    i_am_client      = request.form.get('whoami')
    message_client   = request.form.get('message')
    operation_client = request.form.get('operation')
    status_client = request.form.get('status')


    if i_am_client:
        if message_client:
            if operation_client:
                print_log('active', i_am_client, i_am_pl, "{} sent {}".format(i_am_client, operation_client))
                
                if operation_client == 'Maintainer Server':                    
                    url = '{}{}'.format(aeye_net_oper, print_to_maintainer)
                    print_log('active', i_am_client, i_am_pl, "requst data to : {}".format(url))

                    data={
                        'whoami' : i_am_pl,
                        'message': message_client,
                        'status' : status_client
                    }
                    response = requests.post(url, data=data)
                    
                    if response.status_code == 200:
                        message="Succed to send data to : {}".format(url)
                        print_log('active', i_am_pl, i_am_pl, message)
                        data={
                            'whoami' : i_am_pl,
                            'message': message
                        }
                        return jsonify(data), 200
                    else:
                        message="Failed to send data to : {}".format(url)
                        print_log('error', i_am_pl, i_am_pl, message)
                        data={
                            'whoami' : i_am_pl,
                            'message': message
                        }
                        return jsonify(data), 400
                    
                elif operation_client == 'OpticNet':
                    url = 'http://127.0.0.1:2000/mw/status/'
                    print_log('active', i_am_client, i_am_pl, "requst data to : {}".format(url))

                    data={
                        'whoami' : i_am_pl,
                        'message': message_client,
                        'status' : status_client
                    }
                    response = requests.post(url, data=data)
                    
                    if response.status_code == 200:
                        message="Succed to send data to : {}".format(url)
                        print_log('active', i_am_pl, i_am_pl, message)
                        data={
                            'whoami' : i_am_pl,
                            'message': message
                        }
                        return jsonify(data), 200
                    else:
                        message="Failed to send data to : {}".format(url)
                        print_log('error', i_am_pl, i_am_pl, message)
                        data={
                            'whoami' : i_am_pl,
                            'message': message
                        }
                        return jsonify(data), 400
                else:
                    pass
            else:
                print_log('error', i_am_client, i_am_pl, "{} missed to send file_hash. ".format(i_am_client))
                message='AEYE OpticNet is alive, but failed to send file_hash' 
                data={
                    'whoami' : i_am_pl,
                    'message': message
                }
                return jsonify(data), 400
        else:
            print_log('error', i_am_client, i_am_pl, "{} missed to send file_size.".format(i_am_client))
            message='AEYE OpticNet is alive, but failed to send file_size' 
            data={
                'whoami' : i_am_pl,
                'message': message
            }
            return jsonify(data), 400
    else:
        print_log('error', i_am_client, i_am_pl, "{} missed to send file_name.".format(i_am_client))
        message='AEYE OpticNet is alive, but failed to send file_name' 
        data={
                'whoami' : i_am_pl,
                'message': message
            }
        return jsonify(data), 400
    
    
