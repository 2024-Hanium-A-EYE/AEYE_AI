import argparse
import keras
from .src.aeye_dataloaderdataloader import Kermany2018,Srinivasan2014
from .src.aeye_model import aeye_OpticNet
import time
import keras.backend as K
import gc
from .src.aeye_utils import callback_for_training
from .src.aeye_visualize import plot_loss_acc
from tensorflow.keras.models import load_model

def aeye_train(data_dir, logdir, input_size, dataset, batch_size, weights, epoch, pre_trained_model,snapshot_name):
    
    if dataset=='Srinivasan2014':
        train_batches, test_batches = Srinivasan2014(batch_size, input_size, data_dir)
        num_of_classes = 3
        train_size = 2916
        test_size = 315
    elif dataset == 'Kermany2018' :
        train_batches, test_batches = Kermany2018(batch_size, input_size, data_dir)
        num_of_classes = 4
        train_size = 83484
        test_size = 1000
    # Clear any outstanding net or memory    
    K.clear_session()
    gc.collect()

    # Calculate the starting time
    
    start_time = time.time()

    # Callbacks for model saving, adaptive learning rate
    cb = callback_for_training(tf_log_dir_name=logdir,snapshot_name=snapshot_name)


    # Loading the model
    if weights == None:
        model = aeye_OpticNet(input_size,num_of_classes)
    else :
        model = load_model(weights)

    # Training the model
    history = model.fit_generator(train_batches, shuffle=True, steps_per_epoch=train_size //batch_size, validation_data=test_batches, validation_steps= test_size//batch_size, epochs=epoch, verbose=1, callbacks=cb)


    end_time = time.time()

    print("--- Time taken to train : %s hours ---" % ((end_time - start_time)//3600))

    # Saving the final model
    if snapshot_name == None :
        model.save('OpticNet.h5')
       
    else :    
        model.save(snapshot_name+'.h5')
    
    plot_loss_acc(history,snapshot_name)