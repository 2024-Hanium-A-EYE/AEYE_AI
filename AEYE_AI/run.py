from flask import Flask, url_for, request, jsonify
import logging
from logging import FileHandler
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 업로드 폴더 설정
UPLOAD_FOLDER = 'DATA'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

INFERENCE_FORMAT = {'png', 'jpg', 'jpeg'}
TRAIN_FORMAT = {'txt'}

def check_inference_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in INFERENCE_FORMAT

def check_train_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in TRAIN_FORMAT

def check_test_format(filename):
    return ''

import locale
os.environ["LC_ALL"] = "C.UTF-8"
os.environ["LANG"] = "C.UTF-8"

locale.setlocale(locale.LC_ALL, 'C.UTF-8')

##################################################################
# Dependencies

from colorama import Fore, Back, Style

def print_log(type, string) :
    if type == "active" :
        return app.logger.info("\n-----------------------------------------\n" + 
                               Fore.GREEN + "[OpticNet Back - SUCCESS] [ " + string +" ] " + Fore.RESET +
                               "\n-----------------------------------------")
    elif type == "error" :
        return app.logger.info("\n-----------------------------------------\n" + 
                               Fore.RED + "[OpticNet Back - FAIL] [" + string +"] " + Fore.RESET +
                               "\n-----------------------------------------")

def print_lo_ai(type, string) :
    if type == "active" :
        return app.logger.info("\n-----------------------------------------\n" + 
                               Fore.GREEN + "[OpticNet AI - SUCCESS] [ " + string +" ] " + Fore.RESET +
                               "\n-----------------------------------------")
    elif type == "error" :
        return app.logger.info("\n-----------------------------------------\n" + 
                               Fore.RED + "[OpticNet AI - FAIL] [" + string +"] " + Fore.RESET +
                               "\n-----------------------------------------")
    
def send_response(status, code, message, data) :
    print_log(status, message)
    return jsonify({'status': status, 'code' : code, 'message': message, 'data': data}), code

# localhost:7070/
@app.route('/')
def index() :
    print_log("SUCCESS", "Client Accessed AI Server...")
    return send_response('active', 200, 'Client Accessed AI Server', request.files)

@app.route('/log')
def get_log() :
    status = request.form['status']
    message = request.form['message']

    print_lo_ai(status, message)

##################################################################
# AI
from AI_Module.inference import inference
# from AI_Module.inference import inference
# {"name" : "GOOD"}
@app.route('/api/ai-inference', methods=['POST'])
def ai_inference() :
    print_log("active", "Client Requested AI Inference \nReceived : {}".format(request.form))
    name = request.form['name']

    if name == '' :
        return send_response('error', 400, 'No file part', name)

    file = request.files['file']

    ######################
    # TO - Do : 외부로 받은 File 데이터를 로컬에 저장
    
    ######################

    if file.filename == '':
        print_log("error", "Server Received Empty File")
        return send_response('error', 400, 'No selected file', request.files) 

    ######## RUN INFERENCE ###################
    data_dir = '/DATA/'
    model_path = '/DATA/AI_Module_weight/Optic_net-3-classes-Srinivasan2014.hf'
    model_name = 'Srinivasan2014'
    print_log("active", "start AI")
    response = inference(data_dir, model_path, model_name)
    print_log("active", response)
    ##########################################

    return "GOOD"

#    if file and check_inference_format(file.filename):
#        print_log("SUCCESS", "Client Requested AI Inference with Correct Image Format")

#        filename = secure_filename(file.filename)
#        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#        file.save(filepath)
        

        # Start Inference #
        

        ###################


#        return send_response('active', 200, 'File successfully uploaded', filename)
#    else:
#        return send_response('error', 400, 'Invalid file type', file)
    

# from AI_Module.test import test

@app.route('/api/ai-test', methods=['POST'])
def ai_test():
    print_log("active", "Client Request AI Inference")

    if 'file' not in request.files:
        return send_response('error', 400, 'No file part', request.files)

    file = request.files['file']
    
    if file.filename == '':
        print_log("error", "Server Received Empty File")
        return send_response('error', 400, 'No selected file', request.files) 

    if file and check_test_format(file.filename):
        print_log("active", "Client Requested AI Inference with Correct Image Format")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)


        # Start Test #

        ##############


        return send_response('active', 200, 'File successfully uploaded', filename)
    else:
        return send_response('error', 400, 'Invalid file type', file)
    
# from AI_Module.train import train

@app.route('/api/ai-train', methods=['POST'])
def ai_train():
    print_log("active", "Client Request AI Inference")

    if 'file' not in request.files:
        return send_response('error', 400, 'No file part', request.files)

    file = request.files['file']
    
    if file.filename == '':
        print_log("active", "Server Received Empty File")
        return send_response('error', 400, 'No selected file', request.files) 

    if file and check_train_format(file.filename):
        print_log("active", "Client Requested AI Inference with Correct Image Format")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)


        # Start Train #

        ###############


        return send_response('active', 200, 'File successfully uploaded', filename)
    else:
        return send_response('error', 400, 'Invalid file type', file)
    

##################################################################

import argparse

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Run Flask app on a specific port.')
    parser.add_argument('--p', type=int, default=3000, help='Port to run the Flask app on')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    print_log("active", "Running AI Server...")
    app.run(host='0.0.0.0', port=args.p, debug=True)

