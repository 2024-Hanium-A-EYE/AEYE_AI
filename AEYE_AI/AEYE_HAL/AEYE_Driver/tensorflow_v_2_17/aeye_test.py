import tensorflow as tf
import keras
import argparse
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import keras.backend as K
from .src.aeye_metrics import print_metric
import time

def aye_test(datadir,dataset,weights):

    test_datagen = ImageDataGenerator(rescale=1.0/255)
    image_size = 224

    if dataset=='Srinivasan2014':
        classes=['AMD', 'DME','NORMAL']
        batch = 315
        test_batches = test_datagen.flow_from_directory(datadir, target_size=(image_size,image_size),color_mode='rgb', classes=classes, batch_size=batch, class_mode='categorical')
    else:
        classes = ['CNV', 'DME','DRUSEN','NORMAL']
        batch=1000
        test_batches = test_datagen.flow_from_directory(datadir, target_size=(image_size,image_size),color_mode='rgb', classes=classes, batch_size=batch, class_mode='categorical')

    imgs, y_true = next(test_batches)

    K.clear_session()


    model = load_model(weights)

    start= time.time()
    y_pred = model.predict(imgs)
    end = time.time()

    print ((end-start)/1000)
    if dataset=='Srinivasan2014':
        print_metric(y_true,y_pred,weighted_error=False)
    else:
        print_metric(y_true,y_pred,weighted_error=True)
