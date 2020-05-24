from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.datasets import mnist
from keras.utils import np_utils
from keras.optimizers import Adam
import sys
from keras import backend as K



x=[]
f=open(sys.argv[1], 'r') 
file=f.readlines()
for line in file:
    x.append(int(line.strip()))

kernel=x[0]
layer=x[1]
pool=x[2]
filter_size=32
(x_train, y_train), (x_test, y_test)  = mnist.load_data()
#saved the data
img_rows = x_train[0].shape[0]
img_cols = x_train[1].shape[0]

# Getting our date in the right 'shape' needed for Keras
# We need to add a 4th dimenion to our date thereby changing our
# Our original image shape of (60000,28,28) to (60000,28,28,1)
x_train = x_train.reshape(x_train.shape[0], img_cols , img_rows, 1)
x_test = x_test.reshape(x_test.shape[0], img_cols, img_rows, 1)

# store the shape of a single image 
input_shape = (img_cols, img_rows, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# Normalize our data by changing the range  (0 to 255) to (0 to 1)
x_train /= 255
x_test /= 255

# Now we one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

num_classes = y_test.shape[1]
num_pixels = x_train.shape[1] * x_train.shape[2]



# create model
model = Sequential()

# 2 sets of CRP (Convolution, RELU, Pooling)
model.add(Convolution2D(filters=filter_size,kernel_size=(kernel,kernel),padding = "same",activation='relu',input_shape=input_shape))

model.add(MaxPooling2D(pool_size=(pool,pool)))

for i in range(1,layer):    
    model.add(Convolution2D(filters=filter_size+(i*filter_size),kernel_size=(kernel,kernel),padding = "same",activation='relu',))
    model.add(MaxPooling2D(pool_size=(pool,pool)))



# Fully connected layers (w/ RELU)
model.add(Flatten())
model.add(Dense(units=500, activation='relu'))
model.add(Dense(units=num_classes, activation='softmax'))
# Softmax (for classification)

model.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])
    
print(model.summary())


# Training Parameters
batch_size = 128
epochs = 10

history = model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test),
          shuffle=True)

model.save("mnist_LeNet.h5")

# Evaluate the performance of our trained model
scores = model.evaluate(x_test, y_test, verbose=1)
f=open("accuracy","w")
f.write("{}".format(model.history.history['val_accuracy'][-1]))
f.close()

r=open("history","a")
r.write('Test loss: {}'.format(str(scores[0])))
r.write('\nTest accuracy: {}'.format(str(scores[1])))
r.close()

