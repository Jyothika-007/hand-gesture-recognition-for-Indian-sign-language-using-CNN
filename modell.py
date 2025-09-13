import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

tf.__version__

# -------------------------------
# Dataset Load (70% train, 15% val, 15% test already split manually)
# -------------------------------

# Train generator with augmentation
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

# Validation and Test generators (only rescale, no augmentation)
val_test_datagen = ImageDataGenerator(rescale=1./255)

# Training set (70%)
training_set = train_datagen.flow_from_directory('dataSet/datasetimg/trainingData',
                                                 target_size=(128, 128),
                                                 batch_size=10,
                                                 color_mode='grayscale',
                                                 class_mode='categorical')

# Validation set (15%)
validation_set = val_test_datagen.flow_from_directory('dataSet/datasetimg/validatingData',
                                                      target_size=(128, 128),
                                                      batch_size=10,
                                                      color_mode='grayscale',
                                                      class_mode='categorical')

# Test set (15%)
test_set = val_test_datagen.flow_from_directory('dataSet/datasetimg/testingData',
                                                target_size=(128, 128),
                                                batch_size=10,
                                                color_mode='grayscale',
                                                class_mode='categorical')

# -------------------------------
# Building CNN (same as before)
# -------------------------------
classifier = tf.keras.models.Sequential()

# step 1 - Convolution
classifier.add(tf.keras.layers.Conv2D(filters=32,
                                     kernel_size=3,
                                     padding="same",
                                     activation="relu",
                                     input_shape=[128, 128, 1]))

# step 2 - Pooling
classifier.add(tf.keras.layers.MaxPool2D(pool_size=2,
                                         strides=2,
                                         padding='valid'))

# adding second convolutional layer
classifier.add(tf.keras.layers.Conv2D(filters=32,
                                      kernel_size=3,
                                      padding="same",
                                      activation="relu"))

classifier.add(tf.keras.layers.MaxPool2D(pool_size=2,
                                         strides=2,
                                         padding='valid'))

# step 3 - Flattening
classifier.add(tf.keras.layers.Flatten())

# step 4 - Full Connection
classifier.add(tf.keras.layers.Dense(units=128,
                                     activation='relu'))
classifier.add(tf.keras.layers.Dropout(0.40))
classifier.add(tf.keras.layers.Dense(units=96, activation='relu'))
classifier.add(tf.keras.layers.Dropout(0.40))
classifier.add(tf.keras.layers.Dense(units=64, activation='relu'))
classifier.add(tf.keras.layers.Dense(units=36, activation='softmax')) # softmax for more than 2

# training cnn
classifier.compile(optimizer='adam',
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])


classifier.summary()

# -------------------------------
# Training with validation
# -------------------------------
classifier.fit(training_set,
               epochs=5,
               validation_data=validation_set)

# -------------------------------
# Saving the model
# -------------------------------
model_json = classifier.to_json()
with open("newproject/model_new_1.json", "w") as json_file:
    json_file.write(model_json)
print('Model Saved')
classifier.save_weights('newproject/model_new_1.h5')
print('Weights saved')



