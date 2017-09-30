
# coding: utf-8

# In[3]:

import subprocess
import os
import numpy
import scipy
import scipy.misc
from PIL import Image
import fileinput
import random, string
import sys
import operator
from subprocess import Popen, PIPE
import tensorflow as tf, sys

# In[3]:

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

OUTPUT_DIR = "data/label"
TEST_X_DIR = "test_data"
trainX = numpy.load('tinyX.npy') # this should have shape (26344, 3, 64, 64)
trainY = numpy.load('tinyY.npy') 
testX = numpy.load('tinyX_test.npy') # (6600, 3, 64, 64)


# In[ ]:

def create_graph(model_path):
    """
    create_graph loads the inception model to memory, should be called before
    calling extract_features.

    model_path: path to inception model in protobuf form.
    """
    with gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def extract_features(image_paths, verbose=False):
    """
    extract_features computed the inception bottleneck feature for a list of images

    image_paths: array of image path
    return: 2-d array in the shape of (len(image_paths), 2048)
    """
    feature_dimension = 2048
    features = np.empty((len(image_paths), feature_dimension))

    with tf.Session() as sess:
        flattened_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        for i, image_path in enumerate(image_paths):
            if verbose:
                print('Processing %s...' % (image_path))

            if not gfile.Exists(image_path):
                tf.logging.fatal('File does not exist %s', image)

            image_data = gfile.FastGFile(image_path, 'rb').read()
            feature = sess.run(flattened_tensor, {
                'DecodeJpeg/contents:0': image_data
            })
            features[i, :] = np.squeeze(feature)

    return features


# In[3]:

if not os.path.isdir("data"):
    os.makedirs("data")

labels = ["%d" % label for label in trainY]

#generate training images dir
for i in range(len(trainX)):
    label = labels[i]
    new_path = OUTPUT_DIR + label
    if not os.path.isdir(new_path):
        os.makedirs(new_path)

    im = Image.fromarray(trainX[i].transpose(2,1,0))
    im.save(OUTPUT_DIR + label + "/" + randomword(32) + ".jpeg")


# In[9]:

# generate test images dir
for i in range(len(testX)):
    if not os.path.isdir(TEST_X_DIR):
        os.makedirs(TEST_X_DIR)
    im = Image.fromarray(testX[i].transpose(2,1,0))
    im.save(TEST_X_DIR + "/" + str(i) + ".jpeg")


# PIPE

orig_sys = sys.stdout
with open('output.txt','w') as out:
    sys.stdout = out
    for i in range(6600):
        cmd = "/Users/mahmoodhegazy/tensorflow/bazel-bin/tensorflow/examples/label_image/label_image --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt --output_layer=final_result --image=/Users/mahmoodhegazy/Desktop/test_data/"
        cmd = cmd + str(i) + ".jpeg"
        p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print "Image : " + str(i)
        print "Return code: ", p.returncode
        print out.rstrip(), err.rstrip()   


# In[2]:




# In[29]:


# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("/tmp/output_labels.txt")]
# Unpersists graph from file
with tf.gfile.FastGFile("/tmp/output_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


# In[34]:

test_predictions = []


# In[ ]:

#Kaggle predictions
test_dir = '/Users/mahmoodhegazy/Desktop/test_data'
kaggle_pred = []
for img in os.listdir(test_dir):
        if img == '.DS_Store':
            continue
        print "Image: " + img
        image_path = test_dir + '/' + str(img)
        image_data = tf.gfile.FastGFile(image_path, 'rb').read() #read image data
        score_dict = {}
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor,              {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                score_dict[int(human_string)] = score
        kaggle_pred.append(max(score_dict.iteritems(), key=operator.itemgetter(1))[0]) #only append the class you are 'most confiden
        sess.close()


# In[30]:

len(os.listdir(test_dir))


# In[26]:

validation_predictions = []
y_true = []


# In[ ]:

validatate_dir = '/Users/mahmoodhegazy/Desktop/Project 3/train-validation/validation'
for label in os.listdir(validatate_dir):
    if (label_dir == '.DS_Store'):
        continue
    for img in os.listdir(validatate_dir + '/' + label):
        image_path = test_dir + str(img)
        image_data = tf.gfile.FastGFile(image_path, 'rb').read() #read image data
        score_dict = {}
        y_true.append(int(label))
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,                  {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                score_dict[int(human_string)] = score
                validation_predictions.append(max(score_dictionary.iteritems(), key=operator.itemgetter(1))[0])


# In[9]:

import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications


# In[10]:

# dimensions of images.
img_width, img_height = 64, 64


# In[12]:

# path to the model weights files.
weights_path = 'vgg16_weights.h5'
top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = 'train-validation/train'
validation_data_dir = 'train-validation/validation'
test_data_dir = '/Users/mahmoodhegazy/Desktop/test_data'
nb_train_samples = 26344
nb_validation_samples = 6586
epochs = 120
batch_size = 89


# In[13]:

datagen = ImageDataGenerator(rescale=1. / 255)

# build the VGG16 network
model = applications.VGG16(include_top=False, weights='imagenet')

generator = datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    shuffle=False)
bottleneck_features_test = model.predict_generator(
    generator, nb_train_samples)
np.save(open('bottleneck_features_test.npy', 'wb'),
        bottleneck_features_train)


# In[ ]:



