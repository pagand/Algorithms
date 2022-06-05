import numpy as np

def my_activation(pre_activation_value, activation_type):
    '''

    :param pre_activation_value: single float value or numpy array that is fed to the neuron
    :param activation_type: type of the neuron:
    accepted values: ["relu", "sigmoid", "tanh", or "linear".]
    :return: out: numpy array of the neuron's output
    '''
    # convert it to numpy array if it is not
    if type(pre_activation_value).__module__ != 'numpy':
        pre_activation_value = np.array( [pre_activation_value])


    if activation_type == "relu":
        out = np.where(pre_activation_value > 0, pre_activation_value, 0)
    elif activation_type == "sigmoid":
        out = 1 / (1 + np.exp(- pre_activation_value))
    elif activation_type == "tanh":
        out = np.tanh(pre_activation_value)
    elif activation_type == "linear":
        out = pre_activation_value
    else:
        raise Exception("Error!, the accepted value for activation_type are "
                        "[\"relu\", \"sigmoid\", \"tanh\", \"linear\"]")

    return out

def convolve_filter(input_image, filter, stride, padding):
    '''

    :param input_image: NxM numpy array represent input image
    :param filter: 3x3 numpy array of float values represent convolutional filter
    :param stride: integer value indicating stride for the convolution
    :param padding: integer value indicating padding for the convolution
    :return: out: numpy matrix after convolution and Relu activation
    '''
    if isinstance(padding, int):
        input_image = np.pad(input_image, (padding, padding), constant_values=0)
    else:
        raise Exception("Error!, the accepted value for padding is a integer number ")

    if not isinstance(stride, int):
        raise Exception("Error!, the accepted value for stride is a integer number ")

    r, c = input_image.shape
    kr, kc = filter.shape
    out = np.zeros([int(1+(r-kr)/stride), int(1+(c-kc)/stride)])

    # kernel computation: can be use as a thread for parallel computing
    def _InnerProduct(input_image, filter, row, col ):
        return (np.multiply(input_image[row:row+kr, col:col+kc], filter)).sum()

    for row in range(0, r-kr+1, stride):
        for col in range(0, c-kc+1, stride):
            out[int(row/stride)][int(col/stride)] = _InnerProduct(input_image, filter, row, col)

    # applying the relu

    return my_activation(out, "relu")

def main():
    pre_activation_value = -3.5
    pre_activation_value = np.array([3,-3.3,4])
    print(my_activation(pre_activation_value, "relu"))


    input_image = np.array([[1,2,3],[4,5,6],[7,8,9]])
    filter = np.array([[-1,-1],[-2,2]])
    stride = 2
    padding = 1
    print(convolve_filter(input_image, filter, stride, padding))

if __name__ == "__main__":
    main()




