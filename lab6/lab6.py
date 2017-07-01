# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
INF = float('inf')

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    #print "x",x
    #print "T",threshold
    if x >= threshold:
        return 1
    else:
        return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    import math
    power=-steepness*(x-midpoint)
    return 1/(1+math.exp(power))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    if x<0:
        return 0
    else:
        return x

# Accuracy function
def accuracy(desired_output, actual_output):
    import math
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -0.5*math.pow((desired_output-actual_output),2)

# Forward propagation

def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    
    neuron_outputs={}
    for neuron in net.topological_sort():
        output=0
        wires=net.get_wires(endNode=neuron)
        for wire in wires:
                weight_input=wire.get_weight()*node_value(wire.startNode,input_values,neuron_outputs)
                output+=weight_input
        neuron_outputs[neuron]=threshold_fn(output)
    for value in net.inputs:
            if isinstance(value,str):
                neuron_outputs[value]=input_values[value]
            else:
                neuron_outputs[value]=value
    return (neuron_outputs.get(net.get_output_neuron()),neuron_outputs)

def helper_function(inputs,step_size):
    import itertools
    comb_list=[]
    combinations=[0,step_size,-step_size]
    comb_list.append([inputs[0]+i for i in combinations])
    comb_list.append([inputs[1]+i for i in combinations])
    comb_list.append([inputs[-1]+i for i in combinations])

    return list(itertools.product(*comb_list))

# Backward propagation warm-up
def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    value_list=[]
    input_list=helper_function(inputs,step_size)
    for value in input_list:
        value_list.append(func(*value))

    return (max(value_list), list(input_list[value_list.index(max(value_list))]))
    
def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    result=set()
    l1=[wire.startNode,wire.endNode,wire]
    result.update(set(l1))
    for neighbor in net.get_outgoing_neighbors(wire.endNode):
            for w in net.get_wires(wire.endNode, neighbor):
                result.update(get_back_prop_dependencies(net,w))
                              
    return result
                          
            


# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    result={}
    neurons=net.topological_sort()
    neurons.reverse()
    #print neurons
    for neuron in neurons:
        outB=neuron_outputs.get(neuron)
        output=neuron_outputs.get(neurons[0])

        if net.is_output_neuron(neuron):
            delta_B=outB*(1-outB)*(desired_output-output)
            result[neuron]=delta_B
        else:
            summation=0
            for wire in net.get_wires(neuron):
                    #print "wire",net.get_wires(neuron)
                    weight=wire.get_weight()
                    summation+=weight*result[wire.endNode]
            delta_B=outB*(1-outB)*summation
            result[neuron]=delta_B

    return result
            

def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    delta_values=calculate_deltas(net,desired_output,neuron_outputs)
    
    
    for wire in net.get_wires(None,None):
        new_weight=wire.get_weight()
        if wire.startNode not in neuron_outputs:
            new_weight+=r*input_values.get(wire.startNode,-1)*delta_values[wire.endNode]
        else:
            new_weight+=r*neuron_outputs[wire.startNode]*delta_values[wire.endNode]
        wire.set_weight(new_weight)
    return net

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""

    num_evals=0
    real_output=forward_prop(net,input_values,sigmoid)[0]
    neuron_outputs=forward_prop(net,input_values,sigmoid)[1]

    while minimum_accuracy>accuracy(desired_output,real_output):
        net=update_weights(net,input_values,desired_output,neuron_outputs,r)
        real_output=forward_prop(net,input_values,sigmoid)[0]
        neuron_outputs=forward_prop(net,input_values,sigmoid)[1]
        num_evals+=1

    return (net,num_evals)
    


# Training a neural net

ANSWER_1 =13
ANSWER_2 =38
ANSWER_3 =8
ANSWER_4 =194
ANSWER_5 =52

ANSWER_6 =1
ANSWER_7 ='checkerboard'
ANSWER_8 =['small','medium','large']
ANSWER_9 ='B'

ANSWER_10 = 'D'
ANSWER_11 = ['A','C']
ANSWER_12 =['A','E']


#### SURVEY ####################################################################

NAME ='Nandhini Rengaraj'
COLLABORATORS ='None'
HOW_MANY_HOURS_THIS_LAB_TOOK ='6'
WHAT_I_FOUND_INTERESTING ='The Threshold functions'
WHAT_I_FOUND_BORING ='None'
SUGGESTIONS ='None'
