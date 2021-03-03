"""Nam Tran
    CS550 Artificial Intelligence
    A03
"""


"""Given a set of polynominal coefficients fpoly for a univariate
    polynomial function, e.g. (3, 6, 2, -24) for 3x^3 + 6x^2 + 0x^2 - 24x^0,
    find the real roots of the polynomial (if any) using the Newton-Raphson
    method. This is an interative method that stops when the change
    in estimators is less than tolerance.
    
    fpoly   a list of coefficients
    a       the initial estimate of the root and start of the search
"""

def NewtonRaphson (fpoly, a, tolerance = 0.00001):
    x = a
    division = polyval(fpoly, x) / polyval(derivative(fpoly), x)
    
    while (abs(division) >= tolerance):
        division = polyval(fpoly, x) / polyval(derivative(fpoly), x)
        
        x = x - division
    
    print("The value of the root is: " + str(x))

"""Given a set of polynomial coefficients from highest order to
    x^0, compute the value of the polynomial at x. We assume zero
    coefficients are present in the coefficient list
"""
def polyval(fpoly,x):
    polyList = list(fpoly)
    listLength = len(polyList)
    value = 0
    for i in range(listLength):
        value += (polyList[i])*(x**(listLength-i-1))
    return value
    
"""Given a set of polynomial coefficients from highest order to
    x^0, compute the derivative polynomial. We assume zero coefficients
    are present in the coefficient list.

"""
def derivative(fpoly):
    derivativeList = list()
    polyList = list(fpoly)
    listLength = len(polyList)
    for i in range(listLength):
        derivative = polyList[i]*(listLength-i-1)
        if (derivative != 0):
            derivativeList.append(derivative)
    return derivativeList
    
nrTesting = [7,3,-5,32,-7]
NewtonRaphson(nrTesting, -50)
NewtonRaphson(nrTesting, 5)
