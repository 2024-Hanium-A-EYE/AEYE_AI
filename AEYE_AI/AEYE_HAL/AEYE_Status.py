from flask import jsonify, request, Blueprint

hal_ai_status = Blueprint('AEYE_HAL_AI_Status', __name__)

@hal_ai_status.route('/hal/ai-status', methods = ['POST'])
def hal_ai_status() :
    pass
