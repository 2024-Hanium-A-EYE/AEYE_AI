from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_ano_models
from .serializers import aeye_ano_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import asyncio
import aiohttp

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + str(whoami) + " ] send to : " + Fore.LIGHTBLUE_EX + "[ " + str(api) + " ]" +  
              Fore.RESET + "\n" + Fore.GREEN + "[active] " +  str(message) + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + api + " ]" +  
              Fore.RESET + "\n" + Fore.RED + "[error] " + Fore.RED + message + Fore.RESET +
              "\n-----------------------------------------")

i_am_api_ano = 'NetOper API - ANO'


class aeye_ano_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_ano_models.objects.all().order_by('id')
    serializer_class=aeye_ano_serializers

    def create(self, request) :
        serializer = aeye_ano_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client    = serializer.validated_data.get('whoami')
            operation_client = serializer.validated_data.get('operation')
            message_client   = serializer.validated_data.get('message')

            message='received message  : {}\n         received operation: {}'\
                                            .format(message_client, operation_client)
            print_log('active', i_am_client, i_am_api_ano, message)
            
            if operation_client=='Inference' :
                image = request.FILES.get('image')
                url = 'http://127.0.0.1:3000/mw/ai-inference/'

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response_from_server = loop.run_until_complete(aeye_ai_inference_request(image, url))
                
                i_am_server    = response_from_server.get('whoami')
                message_server = response_from_server.get('message')
                ai_result      = response_from_server.get('ai_result')
                gpt_result     = response_from_server.get('gpt_result')

                message = "succed to receive data from : {}".format(url)
                print_log('active', i_am_api_ano, i_am_api_ano, message)
                
                data={
                    'whoami'     : i_am_api_ano,
                    'message'    : message,
                    'ai_result'  : ai_result,
                    'gpt_result' : gpt_result,
                    }
                
                return Response(data, status=status.HTTP_200_OK)

            elif operation_client=='Train':
                pass
            elif operation_client=='Test':
                pass
            else:
                pass
        else :
            message='Sent Invalide Data : {}'.format(serializer.errors)
            data={
                'whoami' : i_am_api_ano,
                'message': message
            }
            print_log('error', i_am_api_ano, i_am_api_ano, message)

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
    

async def aeye_ai_inference_request(image, url):

    print_log('active', i_am_api_ano, i_am_api_ano, "send data to : {}".format(url))

    async with aiohttp.ClientSession() as session:
        message='Request AI Inference'
        form_data = aiohttp.FormData()
        form_data.add_field('whoami', i_am_api_ano)
        form_data.add_field('message', message)
        form_data.add_field('image', image.read(), filename=image.name, content_type=image.content_type)
        async with session.post(url, data=form_data) as response_from_server:
            if response_from_server.status == 200:
                result = await response_from_server.json()

                return result
