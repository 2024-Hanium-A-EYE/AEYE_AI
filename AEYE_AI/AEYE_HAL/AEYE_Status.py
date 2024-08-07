from flask import jsonify, request, Blueprint
from datetime import datetime
from colorama import Fore, Back, Style

hal_ai_status = Blueprint('AEYE_HAL_AI_Status', __name__)
hal = 'HAL - Status'
def print_log(status, whoami, message, hal) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + " Request to : " + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[OpticNet - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + "Request to : " + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.RED + "[OpticNet - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        
@hal_ai_status.route('/hal/ai-status', methods = ['POST'])
def hal_ai_status() :

    whoami  = request.form.get('whoami')
    status  = request.form.get('status')
    message = request.form.get('message')

    validate = check_valid_data(whoami, status, message)

    if validate == 200:
        print_log('active', whoami, message, hal)
        return 200
    else:
        return 400




def check_valid_data(whoami, status, message) :

    if whoami :
        if status:
            if message :
                return 200
            else :
                print_log('error', whoami, "Failed to Receive message", hal)
                return 400
        else:
            print_log('error', whoami, "Failed to Receive status", hal)
            return 400
    else:
        print_log('error', 'Client', "Failed to Receive whoami", hal)
        return 400
