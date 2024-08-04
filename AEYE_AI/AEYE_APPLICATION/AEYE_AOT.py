from flask import jsonify, request, Blueprint
from colorama import Fore, Back, Style


api = Blueprint('application_layer', __name__)

@api.route('/api/ai-toolkit', methods = ['POST'])
def aeye_ai_operation_toolkit() :
    pass
