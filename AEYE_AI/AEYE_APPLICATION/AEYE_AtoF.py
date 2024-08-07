from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import io
import os
import hashlib

api_UinC = Blueprint('application_layer_UtoF', __name__)

UPLOAD_FOLDER = 'tmp_chunk'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to: " + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to:" + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

api='AEYE OpticNet API AtoF'

@api_UinC.route('/api/data-assemble/', methods = ['POST'])
def aeye_ai_upload_file_in_chunk()->jsonify:

    whoami            = request.form.get('whoami')
    message           = request.form.get('message')
    file_name         = request.form.get('file_name')
    total_chunk_index = request.form.get('total_chunk_index')
    total_chunk_hash  = request.form.get('total_chunk_hash')
    
    # Assemble File
    valid_data=valid(whoami, message, file_name, total_chunk_index, total_chunk_hash)
    
    if valid_data:
        with open(os.path.join(UPLOAD_FOLDER, file_name), 'wb') as final_file:
            for i in range(total_chunk_index):
                chunk_file_path = os.path.join(UPLOAD_FOLDER, f"{file_name}.part{i}")
                with open(chunk_file_path, 'rb') as chunk_file:
                    final_file.write(chunk_file.read())
                os.remove(chunk_file_path)
        
        # Check File is not missed
        with open(os.path.join(UPLOAD_FOLDER, file_name), 'rb') as final_file:
            if calculate_hash(final_file.read()) != total_chunk_hash:
                return jsonify({'message': 'File hash mismatch'}), 400
        
    else:
        pass
    
    
    
def calculate_hash(data)->hashlib:
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def valid(whoami : str, message : str, file_name : str, totatl_chunk_index : int, total_chunk_hash)->bool:
    
    if whoami:
        if message:
            if file_name:
                if totatl_chunk_index:
                    if total_chunk_hash:
                        return True
                    else:
                        return False
                else:
                    return False
            return False
        return False
    return False