from flask import jsonify, request, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
from colorama import Fore, Back, Style
import tempfile
import os
from AEYE_HAL.AEYE_Driver import inference as inference
import requests
hal_ai_inference = Blueprint('AEYE_HAL_AI_Inference', __name__)



import logging
logging.basicConfig(level=logging.INFO)

def print_log(status, whoami, hal, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "active" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
        
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


UPLOAD_FOLDER = 'tmp_chunk'

inference_hal = 'OpticNet HAL - Inference'
@hal_ai_inference.route('/hal/ai-inference/', methods = ['POST'])
def aeye_ai_inference() :
    whoami      = request.form.get('whoami')
    image_name  = request.form.get('image_name')

    # Read Data From local
    
    # Read Weight file
    weight_file_name='Srinivasan2014.h5'
    weight_file_path=os.path.join(UPLOAD_FOLDER, weight_file_name)  
    
    img_file_name=image_name
    img_file_path=os.path.join(UPLOAD_FOLDER, img_file_name)

    print_log('active', whoami, inference_hal, 'Initiate AI Inference')

    if img_file_path:

        if weight_file_path:
            response = aeye_ai_inference_reqeuest(img_file_path, weight_file_path)

            print_log('active', whoami, inference_hal, 'Succeed AI Inference, response : {}'
                                                                                        .format(response))  
            data={
                'whoami' : inference_hal,
                'message': response,
                'ai_result' : response
                }
            return jsonify(data), 200
        else:
            message='No Image file path'
            print_log('error', inference_hal, inference_hal, message)
            data={
                'whoami' : inference_hal,
                'message': message,
            }
            return jsonify(data), 400
    else:
        message='No Weight file path.'
        print_log('error', inference_hal, inference_hal, message)
        data={
            'whoami' : inference_hal,
            'message': message,
        }
        return jsonify(data), 400


def aeye_ai_inference_reqeuest(image_file_path, weight_file_path):

    start_time = datetime.now()
    response = inference.inference(image_file_path, weight_file_path, 'Srinivasan2014')
    end_time = datetime.now()
    time_difference = end_time - start_time
    
    print_log('active', inference_hal, inference_hal, "AI Inference Time : {}".format(time_difference))
    print_log_to_maintainer('active', inference_hal, "Inference finished : {}".format(response))
    
    return response

    



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
