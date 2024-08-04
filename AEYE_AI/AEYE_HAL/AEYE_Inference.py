from flask import jsonify, request, Blueprint

hal_ai_inference = Blueprint('AEYE_HAL_AI_Inference', __name__)

@hal_ai_inference.route('/hal/ai-inference', methods = ['POST'])
def hal_ai_inference() :
    pass
