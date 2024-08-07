import tensorflow as tf
import keras
import argparse
import keras.backend as K
from keras.models import load_model
import cv2
import numpy as np
import requests

url_log='http://127.0.0.1:2000/mw/status'

# status == active or error
def print_log(status, message) :
    data = {
        'whoami' : 'AI Inference',
        'status' : status, 
        'message' : message
        }
    requests.post(url_log, data=data)

def print_pred(preds,classes):

    preds = preds.ravel()
    y = len(classes)
    
    message='preds: {}, classes: {}'.format(preds, classes)
    print_log('good', message)

    for i in range(y):
        preds_rounded = np.around(preds,decimals=4)
        x = x+classes[i]+": "+str(preds_rounded[i])+"%"
        if i!=(y-1):
            x = x+", "
        
        else:
            None
    return x

def image_preprocessing(img):
    img = cv2.imread(img)
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])
    img = 1.0*img/255

    return img

def inference(img,weights,dataset):

    if dataset=='Srinivasan2014':
        classes=['AMD', 'DME','NORMAL']
    else:
        classes = ['CNV', 'DME','DRUSEN','NORMAL']

    processsed_img = image_preprocessing(img)

    K.clear_session()
    
    message='processsed_img: {}'.format(processsed_img)
    print_log('good', message)

    model = load_model(weights)
    
    message='loaded Model: {}'.format(model)
    print_log('good', message)
    
    preds = model.predict(processsed_img,batch_size=None,steps=1)
    
    message='preds: {}'.format(preds)
    print_log('good', message)
    
    return preds, classes
    
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, required=True, help='path/to/image')
    parser.add_argument('--weights', type=str, required=True, help='Weights for prediction')
    parser.add_argument('--dataset', type=str, required=True, help='Choosing between 2 OCT datasets', choices=['Srinivasan2014','Kermany2018'])
    args = parser.parse_args()
    inference(args.imgpath, args.weights, args.dataset)
