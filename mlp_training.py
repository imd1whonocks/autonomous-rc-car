import cv2
import numpy as np
import glob
import sys
from sklearn.model_selection import train_test_split

print('Loading training data...')

# load training data
image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 4), 'float')
training_data = glob.glob('training_data/*.npz')

# if no data, exit
if not training_data:
    print ("No training data in directory, exit")
    sys.exit()

for single_npz in training_data:
    with np.load(single_npz) as data:
        train_temp = data['train_images']
        train_labels_temp = data['train_labels']
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))

#print ('Image array shape: ', image_array.shape)
#print( 'Label array shape: ', label_array.shape)
X = image_array[1:, :]
y = label_array[1:, :]
print ('Image array shape: ', X.shape)
print( 'Label array shape: ', y.shape)


# train test split, 7:3
split_size = int(X.shape[0]*0.7)
train_image, test_image = X[:split_size], X[split_size:]
train_label, test_label = y[:split_size], y[split_size:]

#converting to float32
train_image_32 = train_image.astype(np.float32)
train_label_32 = train_label.astype(np.float32)
test_image_32 = test_image.astype(np.float32)
test_label_32 = test_label.astype(np.float32)


# create MLP
layer_sizes = np.int32([38400, 32, 4])
model = cv2.ml.ANN_MLP_create()
model.setLayerSizes(layer_sizes)
criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
model.setTermCriteria(criteria)
model.setTrainMethod (0,0.001,0)
model.setActivationFunction(1)
print('Training MLP ...')
e1 = cv2.getTickCount()
model.train(train_image_32,cv2.ml.ROW_SAMPLE,train_label_32)
e2 = cv2.getTickCount()
time = (e2 - e1)/cv2.getTickFrequency()
print('Training duration:', time)

# train data
ret_0, resp_0 = model.predict(train_image_32)
prediction_train = resp_0.argmax(-1)
true_labels_train = train_label_32.argmax(-1)
train_rate = np.mean(prediction_train == true_labels_train)
print('Train accuracy: ', "{0:.2f}%".format(train_rate * 100))

# test data
ret_1, resp_1 = model.predict(test_image_32)
prediction_test = resp_1.argmax(-1)
true_labels_test = test_label_32.argmax(-1)
test_rate = np.mean(prediction_test == true_labels_test)
print('Test accuracy: ', "{0:.2f}%".format(test_rate * 100))

# save model
model.save('mlp_xml/mlp.xml')