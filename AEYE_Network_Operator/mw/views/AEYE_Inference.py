from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_inference_models
from .serializers import aeye_inference_serializers
from .forms import aeye_image_form
from colorama import Fore, Back, Style
import datetime
import requests
import os

def print_log(status, whoami, mw, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[AI NetOper - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.RED + "[AI NetOper - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

mw = 'MW - Inference'

url = 'opticnet_container:5000/api/ai-toolkit/'
class aeye_inference_Viewswets(viewsets.ModelViewSet):
    queryset=aeye_inference_models.objects.all().order_by('id')
    serializer_class=aeye_inference_serializers

    def create(self, request) :
        serializer = aeye_inference_serializers(data = request.data)
        form = aeye_image_form(request.POST, request.FILES)

        if serializer.is_valid() :
            whoami    = serializer.validated_data.get('whoami')
            message   = serializer.validated_data.get('message')
            form.save()
            print_log('active', whoami, mw, "Succeed to Received Data : {}".format(message))

            image = request.FILES.get('image')
            response = aeye_ai_inference_request(image, url)

            if response.status_code==200:
                return response
            else:
                return response
        else:
            message = "Client Sent Invalid Data"
            data = aeye_create_json_data(message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



def aeye_ai_inference_request(image, url):

    files = aeye_create_json_files(whoami, image)
    data = {
        'whoami' : 'AEYE NetOper MW Inference',
        'operation' : 'Inference',
        'message' : 'Request AI Inference',
    }

    if files!=400:
        response = requests.post(url, data=data, files=files)

        if response.status_code==200:
            response_data = response.json()
            whoami, message = aeye_get_data_from_response(response_data)
            
            print_log('active', whoami, mw, "Succedd to Receive Data : {}".format(message) )
            return response
        else:
            print_log('error', whoami, mw, "Failed to Receive Data : {}".format(message) )
            message = "Failed to Get Response For the Server"
            data = aeye_create_json_data(message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = "Failed to Add image and files to Json files"
        data = aeye_create_json_data(message)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


def aeye_create_json_files(whoami, image):
    
    h5_file_path = os.path.join(os.path.dirname(__file__), 'weight', 'Srinivasan2014.h5')
            
    with open(h5_file_path, 'rb') as h5_file:
        if h5_file:
            files = {
                    'image': (image.name, image.read(), image.content_type),
                    'model': ('model.h5', h5_file, 'application/octet-stream'),
            }
            print_log('active', whoami, mw, "Succeed to add image and h5 files to Json files")
            return files
        else:
            print_log('error', whoami, mw, "Failed to add image and h5 files to Json files")
            return 400

def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', 'AEYE NetOper MW Inference', mw, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', 'AEYE NetOper MW Inference', mw, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_data(message):
    data = {
        'whoami' : "AEYE NetOper MW Inference",
        'message' : message
    }

    return data