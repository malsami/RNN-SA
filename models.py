"""Model classes."""

import functools
import time

import numpy as np
import tensorflow as tf
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score
from tensorflow.contrib import rnn


def doublewrap(function):
    """
    A decorator decorator, allowing to use the decorator to be used without parentheses if no
    arguments are provided. All arguments must be optional.
    Source: https://gist.github.com/danijar/8663d3bbfd586bffecf6a0094cd116f2
    """

    @functools.wraps(function)
    def decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return function(args[0])
        else:
            return lambda wrapee: function(wrapee, *args, **kwargs)

    return decorator


@doublewrap
def define_scope(function, scope=None, *args, **kwargs):
    """
    A decorator for functions that define TensorFlow operations. The wrapped function will only be
    executed once. Subsequent calls to it will directly return the result so that operations are
    added to the graph only once. The operations added by the function live within a
    tf.variable_scope(). If this decorator is used with arguments, they will be forwarded to the
    variable scope. The scope name defaults to the name of the wrapped function.
    Source: https://gist.github.com/danijar/8663d3bbfd586bffecf6a0094cd116f2
    """
    attribute = '_cache_' + function.__name__
    name = scope or function.__name__

    @property
    @functools.wraps(function)
    def decorator(self):
        if not hasattr(self, attribute):
            with tf.variable_scope(name, *args, **kwargs):
                setattr(self, attribute, function(self))
        return getattr(self, attribute)

    return decorator


class BasicModel:
    """Basic model class.

    Declares the interface of all model classes.
    Source: https://danijar.com/structuring-your-tensorflow-models/
    https://gist.github.com/danijar/8663d3bbfd586bffecf6a0094cd116f2
    """

    def __init__(self, data, target):
        """Constructor.

        Args:
            data -- placeholder for input data
            target -- placeholder for labels
        """
        self.data = data
        self.target = target

        # mention properties, so the full graph is ensured to be defined by the time
        # tf.initialize_variables() is run
        self._prediction
        self._optimize
        self._error

    @define_scope(initializer=tf.contrib.slim.xavier_initializer())
    def prediction(self):
        return

    @define_scope
    def optimize(self):
        return

    @define_scope
    def error(self):
        return


class my_BaseModel:
    """Base class for all tensorflow estimator models."""

    def train_input_fn(self, features, labels, batch_size, num_epochs):
        """Input function for training.

        Args:
        Return:
        """
        pass

    def eval_input_fn(self, dataset):
        """Input function for evaluation.

        Args:
        Return:
        """
        pass

    def test_input_fn(self, dataset):
        """Input function for test.

        Arg:
        Return:
        """
        pass

    def model_fn(self, features, labels, mode, params):
        """Model function.

        Defines the model of an tensorflow estimator.

        Args:
            features -- batches of features returned from the input function
            labels -- batches of labels returned from the input function
            mode -- an instance of tf.estimator.ModeKeys (training, predicting, or evaluation)
            params -- additional configuration

        Return:
        """
        pass


class Single_LSTM_Model:
    """According to
    https://blog.goodaudience.com/first-experience-of-building-a-lstm-model-with-tensorflow-e632bde911e1
    """

    def __init__(self, epochs=8, n_classes=1, n_units=200, n_features=36, sequence_length=4,
                 batch_size=35):
        """Constructor."""
        # specify hyperparameters
        self.epochs = epochs  # number of iterations to run the data set through the model
        self.n_classes = n_classes  # number of classes (binary classification: 0 = not schedulable, 1 = schedulable)
        self.n_units = n_units  # size of hidden state of the LSTM (both c and h)
        self.n_features = n_features  # number of features in the dataset
        self.sequence_length = sequence_length  # length of the sequence
        self.batch_size = batch_size  # size of each batch of data that is feed into the model

        # define placeholders for data-batches
        self.xplaceholder = tf.placeholder('float', [None, self.n_features])
        self.yplaceholder = tf.placeholder('float')

    def recurrent_neural_network_model(self):
        """Design a LSTM model."""
        # define shapes of weights and biases manually
        # random value of shape [rnn_size, n_classes] and [n_classes]
        # automatically do this: https://www.tensorflow.org/api_docs/python/tf/contrib/layers/fully_connected
        layer = {'weights': tf.Variable(tf.random_normal([self.n_units, self.n_classes])),
                 'bias': tf.Variable(tf.random_normal([self.n_classes]))}

        # assign data to x as a sequence: split feature batch along vertical dimension (=1) into 29 slices
        # each slice is an element of the sequence given as input to the LSTM layer
        # (shape of one element of  sequence: [batch_size, num_features / sequence_length])
        x = tf.split(self.xplaceholder, self.sequence_length, 1)
        print(x)  # TODO: delete or replace with logger

        # create LSTM layer and instantiate variables for all gates
        lstm_cell = tf.nn.rnn_cell.LSTMCell(self.n_units)

        # outputs = outputs of the LSTM layer for each time step
        # states = value of last state of both the hidden states (h and c)
        outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

        # take only the last output of the LSTM layer, multiply it with the previouly defined weight matrix
        # and add the bias value
        # result = logit value of forward propagation
        output = tf.matmul(outputs[-1], layer['weights']) + layer['bias']

        # return logit value
        return output

    def train_neural_network(self, X_train, y_train, X_test, y_test):
        """Train and test LSTM model."""
        '''TRAINING'''
        # get logit value = inverse of activation
        logit = self.recurrent_neural_network_model()
        # reshape matrix into vector (shape of labels and logits should be equal for feeding into cost function)
        logit = tf.reshape(logit, [-1])

        # define the cost function
        # sigmoid_cross_entropy_with_logits: because of binary classification
        # (for multi class classification: softmax_cross_entropy_with_logits)
        cost = tf.reduce_mean(
            tf.nn.sigmoid_cross_entropy_with_logits(logits=logit, labels=self.yplaceholder))
        # pass cost to the optimizer
        # AdamOptimizer: because of fairly better performance
        optimizer = tf.train.AdamOptimizer().minimize(cost)

        # create tensorflow session
        with tf.Session() as sess:

            # initialize all global and local variables
            tf.global_variables_initializer().run()
            tf.local_variables_initializer().run()

            # loop over number of iterations (epochs)
            for epoch in range(self.epochs):
                # stop start time
                start_time = time.time()

                # reset epoch loss to 0
                epoch_loss = 0

                # define variable to keep track of start and end computation when splitting data into batches
                i = 0
                # Loop over number of batches
                for step in range(int(len(X_train) / self.batch_size)):
                    # keep track from where data was split in each iteration
                    start = i
                    end = i + self.batch_size

                    # assign a batch of features and labels
                    batch_x = np.array(X_train[start:end])
                    batch_y = np.array(y_train[start:end])

                    # tell tensorflow to run the subgraph necessary to compute the optimizer and the
                    # cost by feeding the values in batch_x and batch_y to the placeholders
                    # compute value of optimizer and cost and assign them to the variables
                    _, c = sess.run([optimizer, cost],
                                    feed_dict={self.xplaceholder: batch_x,
                                               self.yplaceholder: batch_y})
                    # add loss of current batch to epoch_loss
                    epoch_loss += c
                    # raise iterator through data batches
                    i += self.batch_size

                # stop time
                stop_time = time.time()

                # print total loss of epoch
                print('Epoch', epoch, 'completed out of', self.epochs, 'loss:',
                      epoch_loss)  # TODO: delete or replace with logger
                print('Time elapsed: ', stop_time - start_time)

            '''TESTING'''
            # feed testing data set into the model and tell tensorflow to run the subgraph necessary to
            # compute logit
            # pass logit value through a sigmoid activation to get prediction
            # round off to remove decimal places of predicted values
            pred = tf.round(tf.nn.sigmoid(logit)).eval(
                {self.xplaceholder: np.array(X_test), self.yplaceholder: np.array(y_test)})
            # calculate F1 score = weighted average of precision and recall
            f1 = f1_score(np.array(y_test), pred, average='macro')
            # calculate accurarcy score
            accuracy = accuracy_score(np.array(y_test), pred)
            # calculate recall = ratio of correctly predicted positive observations to all positive observations
            recall = recall_score(y_true=np.array(y_test), y_pred=pred)
            # calculate precision = ratio of correctly predicted positive observations to total predicted positive observations
            precision = precision_score(y_true=np.array(y_test), y_pred=pred)
            # print out all calculated scores
            # TODO: delete or replace with logger
            print("F1 Score:", f1)
            print("Accuracy Score:", accuracy)
            print("Recall:", recall)
            print("Precision:", precision)


class Single_GRU_Model:
    """Model with single GRU-cell."""

    def __init__(self, epochs=8, n_classes=1, n_units=200, n_features=36, sequence_length=4,
                 batch_size=35):
        """Constructor."""
        # specify hyperparameters
        self.epochs = epochs  # number of iterations to run the data set through the model
        self.n_classes = n_classes  # number of classes (binary classification: 0 = not schedulable, 1 = schedulable)
        self.n_units = n_units  # size of hidden state of the LSTM (both c and h)
        self.n_features = n_features  # number of features in the dataset
        self.sequence_length = sequence_length  # length of the sequence
        self.batch_size = batch_size  # size of each batch of data that is feed into the model

        # define placeholders for data-batches
        self.xplaceholder = tf.placeholder('float', [None, self.n_features])
        self.yplaceholder = tf.placeholder('float')

    def recurrent_neural_network_model(self):
        """Design a LSTM model."""
        # define shapes of weights and biases manually
        # random value of shape [rnn_size, n_classes] and [n_classes]
        # automatically do this: https://www.tensorflow.org/api_docs/python/tf/contrib/layers/fully_connected
        layer = {'weights': tf.Variable(tf.random_normal([self.n_units, self.n_classes])),
                 'bias': tf.Variable(tf.random_normal([self.n_classes]))}

        # assign data to x as a sequence: split feature batch along vertical dimension (=1) into 29 slices
        # each slice is an element of the sequence given as input to the LSTM layer
        # (shape of one element of  sequence: [batch_size, num_features / sequence_length])
        x = tf.split(self.xplaceholder, self.sequence_length, 1)
        print(x)  # TODO: delete or replace with logger

        # create LSTM layer and instantiate variables for all gates
        gru_cell = tf.nn.rnn_cell.GRUCell(self.n_units)

        # outputs = outputs of the LSTM layer for each time step
        # states = value of last state of both the hidden states (h and c)
        outputs, states = rnn.static_rnn(gru_cell, x, dtype=tf.float32)

        # take only the last output of the LSTM layer, multiply it with the previouly defined weight matrix
        # and add the bias value
        # result = logit value of forward propagation
        output = tf.matmul(outputs[-1], layer['weights']) + layer['bias']

        # return logit value
        return output

    def train_neural_network(self, X_train, y_train, X_test, y_test):
        """Train and test LSTM model."""
        '''TRAINING'''
        # get logit value = inverse of activation
        logit = self.recurrent_neural_network_model()
        # reshape matrix into vector (shape of labels and logits should be equal for feeding into cost function)
        logit = tf.reshape(logit, [-1])

        # define the cost function
        # sigmoid_cross_entropy_with_logits: because of binary classification
        # (for multi class classification: softmax_cross_entropy_with_logits)
        cost = tf.reduce_mean(
            tf.nn.sigmoid_cross_entropy_with_logits(logits=logit, labels=self.yplaceholder))
        # pass cost to the optimizer
        # AdamOptimizer: because of fairly better performance
        optimizer = tf.train.AdamOptimizer().minimize(cost)

        # create tensorflow session
        with tf.Session() as sess:

            # initialize all global and local variables
            tf.global_variables_initializer().run()
            tf.local_variables_initializer().run()

            # loop over number of iterations (epochs)
            for epoch in range(self.epochs):
                # stop start time
                start_time = time.time()

                # reset epoch loss to 0
                epoch_loss = 0

                # define variable to keep track of start and end computation when splitting data into batches
                i = 0
                # Loop over number of batches
                for step in range(int(len(X_train) / self.batch_size)):
                    # keep track from where data was split in each iteration
                    start = i
                    end = i + self.batch_size

                    # assign a batch of features and labels
                    batch_x = np.array(X_train[start:end])
                    batch_y = np.array(y_train[start:end])

                    # tell tensorflow to run the subgraph necessary to compute the optimizer and the
                    # cost by feeding the values in batch_x and batch_y to the placeholders
                    # compute value of optimizer and cost and assign them to the variables
                    _, c = sess.run([optimizer, cost],
                                    feed_dict={self.xplaceholder: batch_x,
                                               self.yplaceholder: batch_y})
                    # add loss of current batch to epoch_loss
                    epoch_loss += c
                    # raise iterator through data batches
                    i += self.batch_size

                # stop time
                stop_time = time.time()

                # print total loss of epoch
                print('Epoch', epoch, 'completed out of', self.epochs, 'loss:',
                      epoch_loss)  # TODO: delete or replace with logger
                print('Time elapsed: ', stop_time - start_time)

            '''TESTING'''
            # feed testing data set into the model and tell tensorflow to run the subgraph necessary to
            # compute logit
            # pass logit value through a sigmoid activation to get prediction
            # round off to remove decimal places of predicted values
            pred = tf.round(tf.nn.sigmoid(logit)).eval(
                {self.xplaceholder: np.array(X_test), self.yplaceholder: np.array(y_test)})
            # calculate F1 score = weighted average of precision and recall
            f1 = f1_score(np.array(y_test), pred, average='macro')
            # calculate accurarcy score
            accuracy = accuracy_score(np.array(y_test), pred)
            # calculate recall = ratio of correctly predicted positive observations to all positive observations
            recall = recall_score(y_true=np.array(y_test), y_pred=pred)
            # calculate precision = ratio of correctly predicted positive observations to total predicted positive observations
            precision = precision_score(y_true=np.array(y_test), y_pred=pred)
            # print out all calculated scores
            # TODO: delete or replace with logger
            print("F1 Score:", f1)
            print("Accuracy Score:", accuracy)
            print("Recall:", recall)
            print("Precision:", precision)


if __name__ == "__main__":
    print("Main function von models.py")