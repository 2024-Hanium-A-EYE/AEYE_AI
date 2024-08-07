from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os

api_aot = Blueprint('application_layer_AOT', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[OpticNet - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[OpticNet - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    

@api_aot.route('/api/ai-toolkit/', methods = ['POST'])
def aeye_ai_operation_toolkit() :

    whoami      = request.form.get('whoami')
    operation   = request.form.get('operation')
    message     = request.form.get('message')
    weight_file = request.files.get('weight')     # option
    image_file  = request.files.get('image')
    
    print_log('active', whoami, "AOT - Inference", "Client Requested AEYE AOT")
    whoami      = 'AEYE OpticNet AOT Inference'

    if operation == 'Inference' :

        #create_weight_and_image_buffer(reqeust)
        response = aeye_ai_inference_reqeuest(whoami, image_file, weight_file)
        delete_weight_and_image_buffer()
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
    url = 'http://127.0.0.1:2000/hal/ai-inference/'
    api = "AOT - Inference"    
    
    if weight_file:
        weight_h5 = secure_filename(weight_file.filename)
        file_h5 = weight_file.read()
        print_log('active', whoami, api, 'Received Weight File: {}'.format(weight_h5))

        if image_file:
            image_png = secure_filename(image_file.filename)
            file_png = image_file.read()
            print_log('active', whoami, api, 'Received Image File: {}'.format(image_png))
            
            files, data = get_json_file_for_inference(whoami, image_png, file_png, weight_h5, file_h5)
            
            response = requests.post(url, data=data, files=files)

            if response.status_code == 200 :


                print_log('active', whoami, api, 'Succeed to Send Data To Client')
                return jsonify({"whoami": 'OpticNet AOT', 'message' : "Succeed to receive Data from AI"}), 200

            elif response.status_code == 400 :
                print_log('error', whoami, api, 'Failed to receive Data from AI')
                return jsonify({"error": "Failed Operating AI Inference"}), 400
            else:
                print_log('error', whoami, api, 'Failed to receive Data from AI')
                return jsonify({"error": "Failed Operating AI Inference"}), 400
            
            
            
        else:
            print_log('error', whoami, api, 'No Image file uploaded')
            return jsonify({"error": "Invalid operation"}), 400

    else:
        print_log('error', whoami, api, 'No Weight file uploaded.')
        return jsonify({"error": "Invalid operation"}), 400


def get_json_file_for_inference(whoami, image_name, image_file, weight_name, weight_file) :
    files = {
        'image' : (image_name, io.BytesIO(image_file), 'image/jpeg'),
        'weight' : (weight_name, io.BytesIO(weight_file), 'application/octet-stream')
    }

    data = {
        'whoami' : whoami,
    }

    return files, data

def create_weight_and_image_buffer(request):
    image_file  = request.files['image']
    weight_file = request.files['weight']

    if image_file:
        if weight_file:

            image_name      = image_file.filename
            image_file_path = os.path.join(UPLOAD_FOLDER, image_name)
    
            uploaded_size = 0

            if os.path.exists(image_file_path):
                uploaded_size = os.path.getsize(image_file_path)

            with open(image_file_path, 'ab') as tmp_image_file:
                tmp_image_file.seek(uploaded_size)
                tmp_image_file.write(image_file.read())

            weight_name      = weight_file.filename
            weight_file_path = os.path.join(UPLOAD_FOLDER, weight_name)

            uploaded_size = 0

            if os.path.exists(weight_file_path):
                uploaded_size = os.path.getsize(weight_file_path)

            with open(weight_file_path, 'ab') as tmp_weight_file:
                tmp_weight_file.seek(uploaded_size)

        else:
            pass
    else:
        pass
    

def delete_weight_and_image_buffer():
    pass

def aeye_ai_test_request(whoami, message):
    pass

def aeye_ai_train_request(whoami, message):
    pass

