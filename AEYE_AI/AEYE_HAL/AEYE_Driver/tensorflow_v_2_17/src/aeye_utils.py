from tensorflow.keras import callbacks

def callback_for_training(tf_log_dir_name='./log/', patience_lr=10, snapshot_name=None):
    cb = []
    
    # TensorBoard log callback
    tb = callbacks.TensorBoard(log_dir=tf_log_dir_name, histogram_freq=0)
    cb.append(tb)
    
    # Uncomment for usage of Early Stopping callback
    # early_stop = callbacks.EarlyStopping(monitor='val_accuracy', min_delta=0, patience=5, verbose=1, mode='auto', save_best_only=True)
    # cb.append(early_stop)
    
    # Model Checkpoint
    if snapshot_name is not None:
        checkpointer = callbacks.ModelCheckpoint(filepath=f"{snapshot_name}.{{epoch:02d}}-{{val_accuracy:.2f}}.hdf5",
                                                 verbose=0,
                                                 monitor='val_accuracy',
                                                 save_best_only=True)
    else:
        checkpointer = callbacks.ModelCheckpoint(filepath="optic-net.{epoch:02d}-{val_accuracy:.2f}.hdf5",
                                                 verbose=0,
                                                 monitor='val_accuracy',
                                                 save_best_only=True)
    cb.append(checkpointer)
    
    # Reduce Learning Rate on Plateau
    reduce_lr_loss = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=6, verbose=1, min_lr=1e-8, mode='auto')
    cb.append(reduce_lr_loss)
    
    return cb
