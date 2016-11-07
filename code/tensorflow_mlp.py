#!/bin/python
#-----------------------------------------------------------------------------
# Author: Emre Neftci
#
# Creation Date : 21-10-2016
# Last Modified : Fri 21 Oct 2016 03:31:40 PM PDT
#
# Copyright : (c) 
# Licence : GPLv2
#----------------------------------------------------------------------------- 
import tensorflow as tf
import numpy as np

sess = tf.InteractiveSession()


from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


x = tf.placeholder(tf.float32, shape=[None,784])
t = tf.placeholder(tf.float32, shape=[None,10])

W1 = tf.Variable(np.random.uniform(size=[784,100]).astype('float32')-.5)
b1 = tf.Variable(np.zeros([100], 'float32'))

W2 = tf.Variable(np.random.uniform(size=[100,10]).astype('float32')-.5)
b2 = tf.Variable(np.zeros([10], 'float32'))

h1 = tf.matmul(x,W1)+b1
a = tf.matmul(h1,W2)+b2
y = tf.nn.sigmoid(a)

cost = tf.reduce_mean(tf.reduce_sum((y-t)**2,1))

train_step = tf.train.GradientDescentOptimizer(.05).minimize(cost)

sess.run(tf.initialize_all_variables())

N_epochs=10000
for i in range(N_epochs):
    data,labels = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x:data,t:labels})
    if i%100==0:
        print cost.eval(feed_dict={x:mnist.train.images,t:mnist.train.labels})
        pred = np.argmax(y.eval(feed_dict={x:mnist.validation.images,t:mnist.validation.labels}),axis=1)
        true_label = np.argmax(mnist.validation.labels,axis=1)
        print np.mean(pred == true_label)*100
