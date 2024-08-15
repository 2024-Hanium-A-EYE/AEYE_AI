from inference import inference
import os
import cv2
import requests


def initiate():
    url_log='http://127.0.0.1:2000/mw/status'
    img_path='/app/AEYE_AI/tmp_chunk/CNV-1569-1.jpeg'
    weight_path='/app/AEYE_AI/tmp_chunk/Srinivasan2014.h5'
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError("이미지를 로드할 수 없습니다. 이미지 경로를 확인하세요: {}".format(img_path))
        
    if not os.path.exists(weight_path):
            raise ValueError("모델 파일을 찾을 수 없습니다. 경로를 확인하세요: {}".format(weight_path))
        
    data = {
        'whoami' : 'AI Inference',
        'status' : "GOOD", 
        'message' : "WORKED"
        }
    requests.post(url_log, data=data)
    preds, classes = inference(img_path, weight_path, "Srinvivasan2014")


if __name__ == '__main__':
    initiate() 

