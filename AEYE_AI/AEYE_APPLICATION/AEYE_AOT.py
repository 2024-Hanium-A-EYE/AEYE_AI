from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os
import asyncio
import aiohttp


api_aot = Blueprint('application_layer_AOT', __name__)

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
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        logging.info("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_api_aot      = 'AEYE OpticNet AOT Inference'

@api_aot.route('/api/ai-toolkit/', methods = ['POST'])
def aeye_ai_operation_toolkit() :

    whoami      = request.form.get('whoami')
    operation   = request.form.get('operation')
    message     = request.form.get('message')
    image_name  = request.form.get('image_name')

    print_log('active', whoami, i_am_api_aot, "Client Requested AEYE AOT")

    if operation == 'Inference' :
        url = 'http://127.0.0.1:2000/hal/ai-inference/'

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server_data = loop.run_until_complete(aeye_ai_inference_reqeuest(url, image_name))
        
        i_am_server    = server_data.get('whoami')
        message_server = server_data.get('message')
        ai_result   = server_data.get('ai_inference')

        message="Succed to Receive data from : {}".format(url)
        data={
            'whomai'    : i_am_api_aot,
            'message'   : message,
            'ai_result' : ai_result,
            }
        return jsonify(data), 200
    
    elif operation == 'Test':
        pass
        response = aeye_ai_test_request(i_am_api_aot, message)
        return response
    
    elif operation == 'Train':
        pass
        response = aeye_ai_train_request(i_am_api_aot, message)
        return response
    else:
        return jsonify({"error": "Invalid operation"}), 400
        
    return jsonify({"error": "no operation is defined"}), 400
    


async def aeye_ai_inference_reqeuest(url, image_name):            
    data={
        'whoami' : i_am_api_aot,
        'message': "request AI Inference",
        'image_name': image_name,
    }

    async with aiohttp.ClientSession() as session:
         async with session.post(url, data=data) as response:
             if response.status == 200:
                 result = await response.json()
                 
                 return result 
        

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

