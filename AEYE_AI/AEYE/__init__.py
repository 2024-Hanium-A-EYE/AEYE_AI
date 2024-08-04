from flask import Flask, jsonify
from AEYE_AI.config import opticnet_config

def aeye_opticnet_framework(aeye: Flask):
    from AEYE_APPLICATION.AEYE_AOT import api_aot
    
    aeye.register_blueprint(api_aot)

    @aeye.before_request
    def before_my_request():
        pass

    @aeye.after_request
    def after_my_request(res):
        return res

def create_aeye_opticnet_framework():
    aeye = Flask(__name__)
    aeye.config.from_object((get_opticnet_env()))
    aeye_opticnet_framework(aeye)
    return aeye

def get_opticnet_env():
    if(opticnet_config.Config.ENV == "prod"):
        return 'config.opticnet.prodConfig'
    elif (opticnet_config.Config.ENV == "dev"):
        return 'config.opticnet.devConfig'

