from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_ano_models
from .serializers import aeye_ano_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.LIGHTBLUE_EX + "[ " + api + " ]" +  Fore.RESET + "\n" +
              Fore.GREEN + "[active] " +  message + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + api + " ]" +  Fore.RESET + "\n" +
              Fore.RED + "[error] " + Fore.RED + message + Fore.RESET +
              "\n-----------------------------------------")

api = 'NetOper API - ANO'

url = 'http://127.0.0.1:3000/mw/ai-inference/'

class aeye_ano_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_ano_models.objects.all().order_by('id')
    serializer_class=aeye_ano_serializers

    def create(self, request) :
        serializer = aeye_ano_serializers(data = request.data)

        if serializer.is_valid() :
            whoami    = serializer.validated_data.get('whoami')
            operation = serializer.validated_data.get('operation')
            message   = serializer.validated_data.get('message')

            print_log('active', whoami, api, 'received message  : {}\n         received operation: {}'.format(message, operation))
            
            if operation=='Inference' :
                image = request.FILES.get('image')

                response = aeye_ai_inference_request(image, url)
                
                if response.status_code==200:
                    whoami, message = aeye_get_data_from_response(response)
                    data = aeye_create_json_file(message)

                    return Response(data, status=status.HTTP_200_OK)
                else:
                    message = 'Failed to Receive Data From Server'
                    data = aeye_create_json_file(message)

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
                
            elif operation=='Train':
                pass
            elif operation=='Test':
                pass
            
            return response
            
        else :
            return Response('["ERROR"] AI Server is Not Working!', status = status.HTTP_400_BAD_REQUEST)
    

def aeye_ai_inference_request(image, url):
    whoami  = 'NetOper API ANO'
    message = "Failed to Receive Data [NetOper - ANO]"
    files   = {'image': (image.name, image.read(), image.content_type)}
    data    = {
        'whoami' : 'NetOper API ANO',
        'message' : 'Request AI Inference'
    }

    print_log('active', whoami, api, "send data to : {}".format(url))

    response = requests.post(url, data=data, files=files)

    if response.status_code==200:
        print_log('active', whoami, api, "received data from : {}".format(url))

        whoami, message = aeye_get_data_from_response(response)
        return response
    else:
        print_log('error', whoami, api, "failed to send data to : {}\n        received message from the server: {}".format(url, message) )
        return response


def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', 'AEYE NetOper Ano', api, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', 'AEYE NetOper Ano', api, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_file(message):
    data = {'whoami' : "AEYE NetOper ANO", 'message' : message}

    return data