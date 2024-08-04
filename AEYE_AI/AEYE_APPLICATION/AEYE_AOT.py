from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io

api_aot = Blueprint('application_layer_AOT', __name__)

def print_log(status, whoami, operation, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
                             print("\n-----------------------------------------\n"   + 
                                   current_time + whoami + "[ " + operation + " ]\n" +  
                                   Fore.GREEN + "[OpticNet - active] [ "+ message +" ]" + Fore.RESET +
                                   "\n-----------------------------------------")
    elif status == "error" :
                             print("\n-----------------------------------------\n"   + 
                                   current_time + whoami + "[ " + operation + " ]\n" +  
                                   Fore.RED + "[OpticNet - error] [ "+ message +" ]" + Fore.RESET +
                                   "\n-----------------------------------------")

    '''
    if status == "active" :
        return api_aot.logger.info("\n-----------------------------------------\n"   + 
                                   current_time + whoami + "[ " + operation + " ]\n" +  
                                   Fore.GREEN + "[OpticNet - active] [ "+ message +" ]" + Fore.RESET +
                                   "\n-----------------------------------------")
    elif status == "error" :
        return api_aot.logger.info("\n-----------------------------------------\n"   + 
                                   current_time + whoami + "[ " + operation + " ]\n" +  
                                   Fore.RED + "[OpticNet - error] [ "+ message +" ]" + Fore.RESET +
                                   "\n-----------------------------------------")

    '''
    

@api_aot.route('/api/ai-toolkit/', methods = ['POST'])
def aeye_ai_operation_toolkit() :

    whoami      = request.form.get('whoami')
    operation   = request.form.get('operation')
    message     = request.form.get('message')
    image_file  = request.files.get('image')      # option
    weight_file = request.files.get('weight')     # option

    # print log
    print_log('active', whoami, operation, "Client Requested AEYE AOT")

    if operation == 'Inference' :
        response = aeye_ai_inference_reqeuest(whoami, image_file, weight_file)
        return response
    
    elif operation == 'Test':
        pass
        response = aeye_ai_test_request(whoami, message)
        return response
    
    elif operation == 'Train':
        pass
        response = aeye_ai_train_request(whoami, message)
        return response
    else:
        return jsonify({"error": "Invalid operation"}), 400
        
    return jsonify({"error": "no operation is defined"}), 400
    


def aeye_ai_inference_reqeuest(whoami, image_file, weight_file):
    url = 'http://localhost:5000/hal/ai-inference/'

    if weight_file:
        weight_h5 = secure_filename(weight_file.filename)
        file_h5 = weight_file.read()
        print_log('active', whoami, 'Inference', 'Received Weight File{}'.format(weight_h5))

        if image_file:
            image_png = secure_filename(image_file.filename)
            file_png = image_file.read()
            print_log('active', whoami, 'Inference', 'Received Weight File{}'.format(image_png))
            
            files = get_json_file_for_inference(whoami, image_png, file_png, weight_h5, file_h5)
            
            response = requests.post(url, files=files)

            if response.status_code == 200 :
                print_log('active', whoami, 'Inference', 'Succeed to receive Data from AI')
                return response

            elif response.status_code == 400 :
                print_log('error', whoami, 'Inference', 'Failed to receive Data from AI')
                return jsonify({"error": "Failed Operating AI Inference"}), 400
            else:
                print_log('error', whoami, 'Inference', 'Failed to receive Data from AI')
                return jsonify({"error": "Failed Operating AI Inference"}), 400
            
            
            
        else:
            print_log('error', whoami, 'Inference', 'No Image file uploaded')
            return jsonify({"error": "Invalid operation"}), 400

    else:
        print_log('error', whoami, 'Inference', 'No Weight file uploaded.')
        return jsonify({"error": "Invalid operation"}), 400


def get_json_file_for_inference(whoami, image_name, image_file, weight_name, weight_file) :
    files = {
        'whoami' : whoami,
        'image' : (image_name, io.BytesIO(image_file), 'image/jpeg'),
        'weight' : (weight_name, io.BytesIO(weight_file), 'application/octet-stream')
    }

    return files

def aeye_ai_test_request(whoami, message):
    pass

def aeye_ai_train_request(whoami, message):
    pass

