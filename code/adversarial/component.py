from __future__ import division
from __future__ import print_function

import gym

__author__ = 'David'


import numpy as np
np.random.seed(123)
from six.moves import cPickle

from keras import backend as K
from keras.models import Model
from keras.layers import Input, Dense, Flatten
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
from keras.optimizers import Adam


# ---------------------------------------------------------- #







"""Generic classes and functions for creating experiment components."""


class Component(object):
    """Base class from which all components should inherit.

    args:
        config_params: Dictionary of parameters used to configure the component.
    """

    def __init__(self, config_params):
        self.config_params = config_params

    def reset(self):
        """Reset the component to defaults."""
        print('Not Implemented')

    def update_config_params(self, config_params):
        """Update the default config params with new parameters."""
        # TODO: Do this more intelligently
        self.config_params = config_params


class Experiment(Component):
    """Object used to initialize, run, and store modeling experiments.

    Args:
        environment: Environment used to produce training data.
        model: Model to be trained.
        name: Unique name for experiment.
        state_base_directory: Location where new directory containing state info for experiment should be created.
        db_params: Info for connecting to database to validate other input values.
    """

    def __init__(self, config_params):
        super(Experiment, self).__init__(config_params)
        self.model = None
        self.history = None

    def start(self):
        """Begin running the experiment."""
        self.model.train(self.environment)
    
    def start_fit_gen (self, train_generator, samples_per_epoch, nb_epoch, callbacks, val_generator, N_seq_val):
        slef.model.fit_generator(train_generator, samples_per_epoch, nb_epoch, callbacks=callbacks,
                    validation_data=val_generator, nb_val_samples=N_seq_val)
    
    def start_predict(self, model, X_test, batch_size):
        
        return model.predict(X_test, batch_size)

    def pause(self):
        """Pause a running experiment."""
        print('Not Implemented')

    def resume(self):
        """Resume a paused experiment."""
        print('Not Implemented')

    def reset(self):
        """Stop experiment if running and reset values to defaults."""
        print('Not Implemented')

    def clone(self):
        """Make a copy of the current experiment, assign default name."""
        print('Not Implemented')

    def configure(self):
        """Do any setup work beyond simple input validation."""
        print('Not Implemented')


class Model_(Component):
    """Base class from which all models should inherit.

    args:
        config_params: Dictionary of parameters used to configure the model.
    """

    def __init__(self, config_params):
        super(Model_, self).__init__(config_params)
        self.X_pl = None
        self.y_pred = None
        self.model = None

    def configure(self, num_input, num_output):
        """Use parameters to configure model."""
        
        return Model(input=num_input, output= num_output )
        
        print('Not Implemented')
        


class DataFeed(Component):
    """Base class from which all environments should inherit.

    args:
        config_params: Dictionary of parameters used to configure the environment.
        env_name: name of OpenAI env object
    """

    def __init__(self, config_params):
        super(DataFeed, self).__init__(config_params)
        self._step = None
        self.action_space = None
        self.observation_space = None

    def step(self, action):
        """Take a step in the environment, generating a new observation and reward."""
        print("Not Implemented")

    def reset(self):
        print("Not Implemented")


class Optimizer(Component):
    """Base class from which all optimizers should inherit.

    args:
        config_params: Dictionary of parameters used to configure the environment.
    """

    def __init__(self, config_params):
        super(Optimizer, self).__init__(config_params)
        self.y_target = None
        self.update_model = None
        self.update_model = None
        self.optimized_model = None

    def configure(self, num_output):
        """Use parameters to configure optimizer."""
        print("Not Implemented")
        
    def config_compile(self, model, optimizer1, loss1, metrics1, loss_weights1, sample_weight_mode1 ):
        model.compile(self, optimizer=optimizer1, loss=loss1, metrics=metrics1, loss_weights=loss_weights1, sample_weight_mode=sample_weight_model1)
        #self.optimized_model.compile(self, optimizer=optimizer1, loss=loss1, metrics=metrics1, loss_weights=loss_weights1, sample_weight_mode=sample_weight_model1)
       
        return model