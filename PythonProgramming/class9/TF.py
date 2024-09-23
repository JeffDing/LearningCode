import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
res = sess.run(result)
print('result:',res)