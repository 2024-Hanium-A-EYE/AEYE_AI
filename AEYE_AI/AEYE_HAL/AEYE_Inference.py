from flask import jsonify, request, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
from colorama import Fore, Back, Style
import tempfile
import os
from AEYE_HAL.AEYE_Driver import inference

hal_ai_inference = Blueprint('AEYE_HAL_AI_Inference', __name__)


def print_log(status, whoami, hal, message) :
    colorama.init(strip=False, convert=True)

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[OpticNet - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.RED + "[OpticNet - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        

inference_hal = 'HAL - Inference'
@hal_ai_inference.route('/hal/ai-inference/', methods = ['POST'])
def aeye_ai_inference() :
    whoami      = request.form.get('whoami')
    image_file  = request.files.get('image')
    weight_file = request.files.get('weight')

    validate = check_valid_data(whoami, image_file, weight_file)
    
    if validate == 200:
        print_log('active', whoami, inference_hal, 'Received valid_data : {}, {}'
                                            .format(image_file.filename, weight_file.filename))        
        tmp_image_file_path, tmp_weight_file_path = aeye_create_buffer(whoami, image_file, weight_file)

        print_log('active', whoami, inference_hal, 'Initiate AI Inference')  
        response = aeye_ai_inference_reqeuest(whoami, tmp_image_file_path, tmp_weight_file_path)
        print_log('active', whoami, inference_hal, 'Succeed AI Inference, response : {}'
                                                                                .format(response))  

        aeye_delete_buffer(whoami, image_file.filename, tmp_image_file_path)
        aeye_delete_buffer(whoami, image_file.filename, tmp_weight_file_path)

        return response, 200

    else:
        print_log('error', whoami, inference_hal, 'Received Invalid valid_data {}, {}'
                                            .format(image_file.filename, weight_file.filename))


def check_valid_data(whoami, image_file, weight_file):
    
    if whoami: 
        if weight_file:
            if image_file:
                return 200
            else:
                print_log('error', whoami, inference_hal, ' Not Received Image File: {}'
                                                                                    .format(image_file))
                return 400
        else: 
            print_log('error', whoami, inference_hal, ' Not Received Weight File: {}'.format(weight_file))
            return 400
    else:
        print_log('error', whoami, inference_hal, ' Not Received whoami: {}'.format(whoami))
        return 400


def aeye_ai_inference_reqeuest(whoami, image_file_path, weight_file_path):
    
    if image_file_path:

        if weight_file_path:
            
            #response = inference.inference(image_file, weight_file, 'Srinivasan2014')
            #return response

            return "GOOD"
        else:
            print_log('error', whoami, inference_hal, 'No Image file path')
            return jsonify({"error": "Invalid operation"}), 400

    else:
        print_log('error', whoami, inference_hal, 'No Weight file path.')
        return jsonify({"error": "Invalid operation"}), 400


def aeye_create_buffer(whoami, image_file, weight_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_image_file:
        temp_image_file.write(image_file.read())
        temp_image_file_path = temp_image_file.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_weight_file :
        temp_weight_file.write(weight_file.read())
        temp_weight_file_path = temp_weight_file.name
        
    
    if temp_image_file_path and temp_weight_file_path:
        print_log('active', whoami, inference_hal, "Created Temporary Path : {}, {}"
                                            .format(temp_image_file_path, temp_weight_file_path))
    else:
        print_log('error', whoami, inference_hal, "Failed to Create Temporary Path : {}, {}"
                                            .format(temp_image_file_path, temp_weight_file_path))
    

    return temp_image_file_path, temp_weight_file_path

def aeye_delete_buffer(whoami, file_name, tmp_file_path):
    try:
        os.remove(tmp_file_path)
        print_log('active', whoami, inference_hal, "Deleted Temporary File : {}"
                                                                    .format(file_name))
    except OSError as e:
        print("Error: {}".format(e.strerror))
        print_log('active', whoami, inference_hal, "Deleted Temporary File : {}"
                                                                    .format(file_name))

