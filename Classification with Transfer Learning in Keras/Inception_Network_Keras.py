# -*- coding: utf-8 -*-

# @author : Dheeraj Kumar Pant
# @credits : Coursera, Kaggle(Data-Set), Google Collab

import os
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import Model
from os import getcwd

!wget --no-check-certificate \
    https://storage.googleapis.com/mledu-datasets/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5 \
    -O /inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5

path_inception ="/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5"

# Importing the inception model  
from tensorflow.keras.applications.inception_v3 import InceptionV3

# Creating an instance of the inception model from the local pre-trained weights
local_weights_file = path_inception

pre_trained_model =InceptionV3(input_shape=(220,220,3),include_top=False,weights=None) 
pre_trained_model.load_weights(local_weights_file)

# Making all the layers in the pre-trained model non-trainable
for layer in pre_trained_model.layers:
    layer.trainable=False

  
pre_trained_model.summary()

last_layer = pre_trained_model.get_layer('mixed7')
print('last layer output shape: ', last_layer.output_shape)
last_output = last_layer.output

# Callback class that stops training once accuracy reaches 97.0%
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.97):
      print("\nReached 97.0% accuracy so cancelling training!")
      self.model.stop_training = True

from tensorflow.keras.optimizers import RMSprop,Adam

# Flatten the output layer to 1 dimension
x = layers.Flatten()(last_output)
# # A fully connected layer with 1,024 hidden units and ReLU activation
# x = layers.Dense(2048,activation='relu')(x)
# x = layers.Dropout(0.4)(x)     

x = layers.Dense(1024,activation='relu')(x)
x = layers.Dropout(0.5)(x)

x = layers.Dense(512,activation='relu')(x)
x = layers.Dropout(0.5)(x)

# x = layers.Dense(256,activation='relu')(x)
# x = layers.Dropout(0.5)(x)

x = layers.Dense(2, activation='softmax')(x)          

model = Model( pre_trained_model.input,x)

model.compile(optimizer = Adam(lr=0.001), 
              loss = 'categorical_crossentropy', 
              metrics = ['accuracy'])
model.summary()

from google.colab import files
files.upload()
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# from google.colab import drive
# # drive.mount('/content/gdrive')
# !unzip emotions.zip
# !kaggle datasets download -d ahmedmoorsy/facial-expression

# !kaggle datasets download -d manishshah120/facial-expression-recog-image-ver-of-fercdataset
# !kaggle datasets download -d datamunge/sign-language-mnist
# !kaggle datasets download -d mahmoudima/mma-facial-expression
# !kaggle datasets download -d prasunroy/natural-images
# !kaggle competitions download -c dogs-vs-cats
!kaggle datasets download -d tongpython/cat-and-dog

!unzip cat-and-dog.zip

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir = "training_set/training_set"
validation_dir = "test_set/test_set"

# Rescaling
train_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)# Your Code Here )

# Training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(# Your Code Here)
    train_dir,
    target_size=(220,220),
    batch_size=20,
    shuffle = True,
    class_mode='categorical')

# Validation images in batches of 20 using test_datagen generator
validation_generator =  test_datagen.flow_from_directory( # Your Code Here)
    validation_dir,
    target_size=(220,220),
    batch_size=20,
    shuffle = True,
    class_mode='categorical')

# Iterates, and stops training at 97% accuracy

callbacks = myCallback()# Your Code Here
history = model.fit_generator(# Your Code Here (set epochs = 3))
                              train_generator,
                              epochs=20,
                              verbose=1,
                              callbacks=[callbacks],
                              validation_data=validation_generator)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()


plt.show()
