import numpy as np
import json

class Neural_Network():

	def __init__(self, inputs, training_inputs=None, training_outputs=None):
		self.inputs = np.random.randn(1, inputs)
		# self.training_inputs = np.array(training_inputs)
		# self.training_outputs = np.array(training_outputs)
		self.layers = []

	def add_layer(self, n_neurons):
		if len(self.layers) == 0:
			self.layers.append(Layer(self.inputs.size, n_neurons))
		else:
			self.layers.append(Layer(self.layers[len(self.layers)-1].n_neurons,n_neurons))

	def size(self):
		size = 0
		for i in range(len(self.layers)):
			size += self.layers[i].weights.size

		return size
	"""
	def train(self,iterations):
			for iteration in range(iterations):
				#self.forward()

				layer_n = 0
				for layer in self.layers:
					if layer_n == 0:
						last_result = layer.forward(self.inputs)
						layer_n +=1
					else:
						last_result = i.forward(last_result)


					error = self.training_outputs - last_result
					adjustement = np.dot(self.training_inputs.T, error * layer.sigmoid_activation_derivate(last_result))
					print(adjustement)
"""

	def forward(self, inputs=None):
		layer = 0
		if inputs:
			self.inputs = np.array(inputs)
		for i in self.layers:
			if layer == 0:
				last_result = i.forward(self.inputs)
			else:
				last_result = i.forward(last_result)
			layer += 1

		self.output = last_result
		return self.output

	def save(self):
		i = 0
		for layer in self.layers:
			layer.save('layer'+str(i))
			i += 1

	def load(self):
		i = 0
		for layer in self.layers:
			layer.load('layer' + str(i))
			i += 1

class Layer:
	def __init__(self, inputs, neurons):
		self.n_inputs = inputs
		self.n_neurons = neurons
		self.weights = np.random.randn(inputs,neurons)
		self.biases = np.zeros((1,neurons))

	def sigmoid_activation(self,x):
		x = x.astype(np.float64)
		return 1/(1 + np.exp(-x))

	def sigmoid_activation_derivate(self,x):
		return x *(1-x)	

	def forward(self,inputs):
		return self.sigmoid_activation(np.dot(inputs.astype(float),self.weights)+self.biases)

	def save(self, name):
		self.weights.tofile(name, sep=',')
		self.biases.tofile('bias_'+name, sep=',')

	def load(self, name):
		shape_weights = self.weights.shape
		shape_biases = self.biases.shape

		self.weights = np.fromfile(name, sep=',').reshape(shape_weights)
		self.biases = np.fromfile('bias_'+name, sep=',').reshape(shape_biases)
		print('\nloaded data')
		print(self.weights, self.weights.shape)
		print(self.biases, self.biases.shape)

if __name__ == '__main__':
	inputs = [1, 2, 3, 4, 5]
	output = [0, 1, 0, 1, 0]
	red = Neural_Network(6)
	red.add_layer(3)
	red.add_layer(9)
	red.add_layer(1)
	red.add_layer(23)
	red.add_layer(2)
	red.forward()
	print(red.output)
