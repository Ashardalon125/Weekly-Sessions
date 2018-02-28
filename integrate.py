#Original Author Mark Caprio
#University of Notre Dame
#Spring 2014

#Modifications by Danielle McDermott
#meant for plotting/sloving Newman problems
#Spring 2018

import math
import numpy as np

# Newton-Cotes integration weights
endpoint_weights = [1/2,1/3,3/8,14/45]
interior_weights = [
    [1],
    [2/3,4/3],
    [3/4,9/8,9/8],
    [28/45,64/45,8/15,64/45]
    ]


def integrate(f,interval,steps,order=1,float_type=float):
    """ Evaluate integral by Newton-Cotes rule (trapezoidal, Simpson's, etc.).

    f: function to integrate
    interval: tuple integration region (a,b)
    steps: number of integration steps (must be valid for order chosen)
    order (optional): integer order for integration (1..4)
    float_type: float type to which each term is converted before addition

    returns:
        total_integral (floating point number)
        x_array (1D np.array containing independent variable)
        I_array (1D np.array containing integrated values)
    """

    # set up interval properties
    (a,b) = interval  # endpoints
    h = (b-a)/steps  # step size
    I_array = np.empty(int(steps+1))
    x_array = np.linspace(a,b,int(steps+1))

    # validate number of steps
    # must be positive and must be multiple of order
    if (not((steps>0) and ((steps%order)==0))):
        raise ValueError("invalid number of steps for given order")

    # accumulate sum
    s = float_type(0.)
    for k in range(steps+1):
        # find weight w_k
        if ((k==0) or (k==steps)):
            # endpoint
            wk = endpoint_weights[order-1]
        else:
            # interior point
            wk = interior_weights[order-1][k%order]


        # find function value f(x_k)
        xk = a + h*k   # x value
        fk = f(xk)     # function value

        # accumulate term
        ## print("k",k,"wk",wk,"xk",xk,"fk",fk)
        s += float_type(wk*fk)
        I_array[k] = s*h
    # scale by step size prefactor
    result = h*s

    return result, x_array, I_array
