import numpy as np


class simplest_neural_net_ever:
    def __init__(self, input_length=17, output_length=7, nb_hidden_layers=5, hidden_layers_length=20, hidden_layers=None, weights_initial_coeff=4, bias_initial_coeff=2, weights_output_coeff=1):
        self.input_length = input_length
        self.output_length = output_length
        self.nb_hidden_layers = nb_hidden_layers
        self.hidden_layers_length = hidden_layers_length
        self.weights_initial_coeff = weights_initial_coeff
        self.bias_initial_coeff = bias_initial_coeff
        self.weights_output_coeff = weights_output_coeff
        self.input = np.zeros((1, input_length))
        self.output = np.zeros((1, output_length))
        if not hidden_layers:
            self.hidden_layers = []
            self.random_initialize()
        else:
            self.hidden_layers = hidden_layers


    def __repr__(self):
        return "input length: {}\noutput length: {}\nHow many hidden layers: {}\nHidden layers length: {}\nHidden layers: {}\n".format(self.input_length, self.output_length, self.nb_hidden_layers, self.hidden_layers_length, self.hidden_layers)


    def copy(self):
        out = simplest_neural_net_ever(self.input_length, self.output_length, self.nb_hidden_layers, self.hidden_layers_length, self.hidden_layers)
        return out


    def zero_initialize(self):
        self.hidden_layers.append({'weights':np.zeros((self.input_length, self.hidden_layers_length)), 'bias':np.zeros((1, self.hidden_layers_length))})
        for i in range(self.nb_hidden_layers-2):
            self.hidden_layers.append({'weights':np.zeros((self.hidden_layers_length, self.hidden_layers_length)), 'bias':np.zeros((1, self.hidden_layers_length))})
        self.hidden_layers.append({'weights':np.zeros((self.hidden_layers_length, self.output_length)), 'bias':np.zeros((1, self.output_length))})


    def random_initialize(self):
        #np.random.seed(1)
        self.hidden_layers.append({'weights':self.weights_initial_coeff*np.random.random((self.input_length, self.hidden_layers_length)) - self.bias_initial_coeff, 'bias':np.random.random((1, self.hidden_layers_length))})
        for i in range(self.nb_hidden_layers-2):
            self.hidden_layers.append({'weights':self.weights_initial_coeff*np.random.random((self.hidden_layers_length, self.hidden_layers_length)) - self.bias_initial_coeff, 'bias':np.random.random((1, self.hidden_layers_length))})
        self.hidden_layers.append({'weights':self.weights_initial_coeff*np.random.random((self.hidden_layers_length, self.output_length)) - self.bias_initial_coeff, 'bias':np.random.random((1, self.output_length))})


    def feed_forward(self, X):
        flow = np.copy(X)
        for hidden_layer in self.hidden_layers:
            flow = sigmoid(self.weights_output_coeff*np.dot(flow, hidden_layer['weights']) + hidden_layer['bias'])
        return flow


def sigmoid(x, deriv=False):
    if(deriv==True):
        return (x*(1-x))
    return 1/(1+np.exp(-x))


def test():

    nn2 = simplest_neural_net_ever()
    nn2.random_initialize()
    print(nn2.feed_forward([0, 1000, 1, 120, 100, -20, 95, 0, 1000, 1, 120, 100, 220, 95, 0]))

if __name__=="__main__":
    test()
    #create_neural_net_with_tf()
    #neural_net_with_tf()
