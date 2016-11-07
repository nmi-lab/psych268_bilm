#!/bin/python
#-----------------------------------------------------------------------------
# Author: Emre Neftci
#
# Creation Date : 20-10-2016
# Last Modified : Thu 20 Oct 2016 10:34:01 PM PDT
#
# Copyright : (c) 
# Licence : GPLv2
#----------------------------------------------------------------------------- 
import tensorflow as tf
sess = tf.InteractiveSession()

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


x = tf.placeholder(tf.float32, shape=[None, 784])
y = tf.placeholder(tf.float32, shape=[None, 10])

x_image = tf.reshape(x, [-1, 28, 28, 1])
W1 = weight_variable([5,5,1,32]) #x, y, channels (input depth), depth
b1 = bias_variable([32]) 
hc1 = tf.nn.relu(tf.nn.conv2d(x_image, W1, strides=[1, 1, 1, 1], padding='SAME')+b1)
hp1 = tf.nn.max_pool(hc1, ksize=[1,2,2,1], strides=[1, 2, 2, 1], padding='SAME')

W2 = weight_variable([5,5,32,64]) #x, y, channels (input depth), depth
b2 = bias_variable([64]) 
hc2 = tf.nn.relu(tf.nn.conv2d(hp1, W2, strides=[1, 1, 1, 1], padding='SAME')+b2)
hp2 = tf.nn.max_pool(hc2, ksize=[1,2,2,1], strides=[1, 2, 2, 1], padding='SAME')


W3 = tf.Variable(tf.random_uniform([7*7*64,1024])-.5)
b3 = tf.Variable(tf.zeros([1024])-1)

hf = tf.reshape(hp2, [-1, 7*7*64])
hid1= tf.nn.relu(tf.matmul(hf,W3)+b3)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

out = tf.nn.softmax(tf.matmul(hid1, W_fc2) + b_fc2)

cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(out),1))
#train_step = tf.train.AdamOptimizer(1e-4).minimize(cost)
train_step = tf.train.GradientDescentOptimizer(1e-4).minimize(cost)
accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out,1),tf.argmax(y,1)),tf.float32))

sess.run(tf.initialize_all_variables())
for i in range(100000):
    batch = mnist.train.next_batch(50)
    train_step.run(feed_dict={x: batch[0], y: batch[1]})
    if i%500 == 0:
        print accuracy.eval(feed_dict={x: mnist.test.images, y: mnist.test.labels})
