""" romberg.py -- Romberg numerical integration routine
     
    Language: Python 3
    Mark A. Caprio
    University of Notre Dame
    Written for Computational Methods in Physics, Spring 2014.
"""

def romberg(f,interval,tolerance,
            verbose=False,min_order=0,max_order=None,reference=None):
    """ Evaluate integral by Romberg integration.

    Note: The Romberg extrapolation order is taken 0-based in the code
    and diagnostic output.  That is, R(i,0) is the trapezoidal rule
    with 2**i steps.  (In Newman the extrapolation order is taken
    1-based, instead.)

    f: function to integrate
    interval: tuple integration region (a,b)
    tolerance: desired absolute error
    verbose (optional):  controls diagnostic output
    min_order (optional): lowest order to carry to, regardless of tolerance
    max_order (optional): limit on order of calculation, giving failure (or None)
    reference (optional): reference value for comparison output (or None)
    """

    # set up integral interval
    (a,b) = interval  # endpoints

    # give initial diagnostic output
    if (verbose):
        print("integrating on range {0}".format(interval))
        if (reference != None):
            print("  reference value {:+.5e}".format(reference))
        print()


    # set up base case -- i=0, i.e., single-step trapezoidal rule
    i = 0  # exponent for number of steps
    h = (b-a)/(2**i)  # step size
    R0 = (1/2)*(b-a)*(f(a)+f(b))   # basic trapezoidal estimate
    R_values = [R0]  # current list of Romberg values
    
    # give diagnostic output for base case
    if (verbose):
        print("R({0},{1}) {2:+.15e}".format(i,i,R0),end="")
        if (reference != None):
            residual = reference - R0 
            print(" ... residual {:+.4e}".format(residual))
        else:
            print()
        print()

    # iterate Romberg to next higher number of steps
    eik = 2 * tolerance # make up error estimate to get past while condition
    while ((i < min_order) or (abs(eik) > tolerance)):
        # advance parameters to next step size
        i += 1
        h /= 2

        # check for excessive order
        if ((max_order != None) and (i >  max_order)):
            return None

        # evaluate new trapezoidal estimate as "update" to old trapezoid rule
        # R(i,0) - 1/2 R(i-1,0) = h_i *sum_(odd indices m) f(x_m)
        R0 = (1/2) * R0
        for m in range(1,2**i,2):
            R0 += h*f(a+m*h)

        # generate new R list
        #   Given R(i,0) and previous R(i-1,k),
        #   we must must calculate R(i,1), ..., R(i,i).
        #   Loop over k=0..i-1.
        #   Use extrapolation formula for R(i,k+1)
        #     R(i,k+1) = 1/(2**(2*k+2)-1)*(2**(2*k+2)*R(i,k) - R(i-1,k))
        #   Also calculate error estimate
        #     error(i,k) = 1/(2**(2*k+2)-1)*(R(i,k) - R(i-1,k))
        R_values_old = R_values
        R_values = [R0]
        for k in range(0,i):
            # assemble values at order k
            Rim1k = R_values_old[k]   # R(i-1,k)
            Rik = R_values[k]   # R(i,k)
            eik = 1/(2**(2*k+2)-1)*(Rik - Rim1k) # error(i,k)

            # give diagnostic output for order k
            if (verbose):
                print("R({0},{1}) {2:+.15e} epsilon({0},{1}) {3:+.4e}".format(i,k,Rik,eik),end="")
                if (reference != None):
                    residual = reference - Rik 
                    print(" ... residual {:+.4e}".format(residual))
                else:
                    print()

            # extrapolate to order k+1
            Rikp1 = 1/(2**(2*k+2)-1)*(2**(2*k+2)*Rik - Rim1k) # R(i,k+1)
            R_values.append(Rikp1)

        # give final diagnostic output for order i+1
        if (verbose):
            print("R({0},{1}) {2:+.15e}".format(i,i,Rikp1),end="")
            if (reference != None):
                residual = reference - Rikp1 
                print(" ... residual {:+.4e}".format(residual))
            else:
                print()
            print()

    # return last computed value
    return Rikp1

# test code
if (__name__ == "__main__"):

    import math
    
    # benchmark function
    def f_decay(x):
        return math.exp(-x)
    int_decay = 1 - 1/math.e

    print(romberg(f_decay,(0,1),tolerance=1e-10,verbose=True,reference=int_decay))

