import numpy as np


class Neural_Network():

	def __init__(self,inputs,training_inputs=None,training_outputs=None):
		self.inputs = np.array(inputs)
		self.training_inputs = np.array(training_inputs)
		self.training_outputs = np.array(training_outputs)
		self.layers = []

	def add_layer(self,n_neurons):
		if len(self.layers) == 0:
			self.layers.append(Layer(self.inputs.size,n_neurons))
		else:
			self.layers.append(Layer(self.layers[len(self.layers)-1].n_neurons,n_neurons))


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
	#
	def forward(self):
		layer = 0
		for i in self.layers:
			if layer == 0:
				last_result = i.forward(self.inputs)
			else:
				last_result = i.forward(last_result)
			layer +=1

		self.output = last_result
		


class Layer:
	def __init__(self,inputs,neurons):
		self.n_inputs = inputs
		self.n_neurons = neurons
		self.weights = np.random.randn(inputs,neurons)
		self.biases = np.zeros((1,neurons))

	def sigmoid_activation(self,x):
		return 1/(1 + np.exp(-x))

	def sigmoid_activation_derivate(self,x):
		return x *(1-x)	

	def forward(self,inputs):
		return self.sigmoid_activation(np.dot(inputs.astype(float),self.weights)+self.biases)


if __name__ == '__main__':
	inputs = [1,2,3,4,5]
	output = [0,1,0,1,0]
	red = Neural_Network([6],inputs,output)
	red.add_layer(3)
	red.add_layer(9)
	red.add_layer(1)
	red.add_layer(23)
	red.add_layer(1)
	red.forward()
	print(red.output)

	