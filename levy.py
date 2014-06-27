#    Copyright (C) 2005 Paul Harrison
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""\
This is a package for calculation of Levy stable distributions
(probability density function and cumulative density function) and for
fitting these distributions to data.

It operates by interpolating values from a table, as direct computation 
of these distributions requires a lengthy numerical integration. This 
interpolation scheme allows fast fitting of Levy stable distributions 
to data using the Maximum Likelihood technique.

Does not support alpha values less than 0.5.
"""


__version__ = "0.4"

import sys

import numpy as N
import numpy.random as RandomArray


def _make_range(min, max, n):
    """ Create a sequence of values. """
    return (N.arange(n)) * ((max-min)/(n-1.0)) + min


def _calculate_levy(x, alpha, beta, cdf=False):
    """ Calculation of Levy stable distribution via numerical integration.
        This is used in the creation of the lookup table. """
    # "0" parameterization as per http://academic2.american.edu/~jpnolan/stable/stable.html
    # Note: fails for alpha=1.0
    #       (so make sure alpha=1.0 isn't exactly on the interpolation grid)
    from scipy import integrate

    C = beta * N.tan(N.pi*0.5*alpha)
    
    def func_cos(u):
        ua = u ** alpha
        if ua > 700.0: return 0.0
        return N.exp(-ua)*N.cos(C*ua-C*u)

    def func_sin(u):
        ua = u ** alpha
        if ua > 700.0: return 0.0
        return N.exp(-ua)*N.sin(C*ua-C*u)

    if cdf:
        # Cumulative density function
        return (integrate.quad(lambda u: u and func_cos(u)/u or 0.0, 0.0, integrate.Inf, weight="sin", wvar=x, limlst=1000)[0]
               + integrate.quad(lambda u: u and func_sin(u)/u or 0.0, 0.0, integrate.Inf, weight="cos", wvar=x, limlst=1000)[0] 
               ) / N.pi + 0.5
    else:
        # Probability density function
        return ( integrate.quad(func_cos, 0.0, integrate.Inf, weight="cos", wvar=x, limlst=1000)[0]
               - integrate.quad(func_sin, 0.0, integrate.Inf, weight="sin", wvar=x, limlst=1000)[0] 
               ) / N.pi


def _levy_tan(x, alpha, beta, cdf=False):
    """ Calculate the values stored in the lookup table. 
        The tan mapping allows the table to cover the range from -INF to INF. """
    x = N.tan(x)
    return _calculate_levy(x,alpha,beta,cdf)


def _interpolate(points, grid, lower, upper):
    """ Perform multi-dimensional Catmull-Rom cubic interpolation. """
    point_shape = N.shape(points)[:-1]
    points = N.reshape(points, (N.multiply.reduce(point_shape), N.shape(points)[-1]))

    grid_shape = N.array(N.shape(grid))
    dims = len(grid_shape)
    
    points = (points-lower) * ((grid_shape-1) / (upper-lower))
    
    floors = N.floor(points).astype('int')
    
    offsets = points - floors
    offsets2 = offsets * offsets
    offsets3 = offsets2 * offsets
    weighters = [
        -0.5*offsets3    +offsets2-0.5*offsets,
         1.5*offsets3-2.5*offsets2            +1.0, 
        -1.5*offsets3  +2*offsets2+0.5*offsets,
         0.5*offsets3-0.5*offsets2,
    ]
    
    ravel_grid = N.ravel(grid)

    result = N.zeros(N.shape(points)[:-1], 'float64')
    for i in xrange(1 << (dims*2)):
        weights = N.ones(N.shape(points)[:-1], 'float64')
        ravel_offset = 0
        for j in xrange(dims):
            n = (i >> (j*2)) % 4
            ravel_offset = ravel_offset * grid_shape[j] + \
                N.maximum(0,N.minimum(grid_shape[j]-1,floors[:,j] + (n-1)))
            weights *= weighters[n][:,j]
        
        result += weights * N.take(ravel_grid, ravel_offset)

    return N.reshape(result, point_shape)



# Dimensions: 0 - x, 1 - alpha, 2 - beta
_lower = N.array([-N.pi/2 * 0.999, 0.5, -1.0])
_upper = N.array([N.pi/2 * 0.999, 2.0, 1.0])

def _make_data_file():
    """ Generates the lookup table, writes it to a .py file. """
    import base64
    
    size = (200, 50, 51)
    pdf = N.zeros(size, 'float64')
    cdf = N.zeros(size, 'float64')
    ranges = [ _make_range(_lower[i],_upper[i],size[i]) for i in xrange(len(size)) ]

    print "Generating levy_data.py ..."
    for i in xrange(size[1]):
        for j in xrange(size[2]):
            print "Calculating alpha =", ranges[1][i], "beta = ", ranges[2][j]
            for k in xrange(size[0]):
                pdf[k,i,j] = _levy_tan(ranges[0][k], ranges[1][i], ranges[2][j])
                cdf[k,i,j] = _levy_tan(ranges[0][k], ranges[1][i], ranges[2][j], True)

    file = open("levy_data.py", "wt")
    file.write("""
# This is a generated file, do not edit.
import numpy, base64

pdf = numpy.loads(base64.decodestring(
\"\"\"%s\"\"\"))\n
cdf = numpy.loads(base64.decodestring(
\"\"\"%s\"\"\"))\n""" % 
        (base64.encodestring(pdf.dumps()), base64.encodestring(cdf.dumps())) )
    file.close()




def levy(x, alpha, beta, cdf=False):
    """ Interpolate densities of the Levy stable distribution specified by alpha and beta.
    
        Specify cdf=True to obtain the *cumulative* density function. 
    
        Note: may sometimes return slightly negative values, due to numerical inaccuracies.
    """
    import levy_data

    points = N.empty(N.shape(x) + (3,), 'float64')
    points[..., 0] = N.arctan(x) 
    points[..., 1] = alpha
    points[..., 2] = beta
    
    if cdf:
        what = levy_data.cdf
    else:
        what = levy_data.pdf 
    return _interpolate(points, what, _lower, _upper)


def neglog_levy(x, alpha, beta):
    """ Interpolate negative log densities of the Levy stable distribution specified by alpha and beta. 
    
        Small/negative densities are capped at 1e-100 to preserve sanity.
    """
    return -N.log(N.maximum(1e-100, levy(x, alpha, beta)))


def _reflect(x, lower, upper):
    while 1:
        if x < lower:
            x = lower - (x-lower)
        elif x > upper:
            x = upper - (x-upper)
        else:
            return x


def fit_levy(x, alpha=None, beta=None, location=None, scale=None):
    """ Estimate parameters of Levy stable distribution given data x,
        uN.sing the Maximum Likelihood method. 
        
        By default, searches all possible Levy stable distributions. However 
        you may restrict the search by specifying the values of one or more
        parameters.
        
        Examples:
        
            levy(x) -- Fit a stable distribution to x
            
            levy(x, beta=0.0) -- Fit a symmetric stable distribution to x
            
            levy(x, beta=0.0, location=0.0) -- Fit a symmetric distribution centered on zero to x
            
            levy(x, alpha=1.0, beta=0.0) -- Fit a Cauchy distribution to x
        
        Returns a tuple of (alpha, beta, location, scale, negative log density)        
        """

    from scipy import optimize
    
    if location == None or scale == None:
        x = N.sort(x)
        
        last = len(x)-1
        guess_location = x[last/2]
        guess_scale = (x[last-last/4] - x[last/4])/2.0
        
        # Maybe there are lots of zeros or something...
        if guess_scale == 0:
            guess_scale = (x[last] - x[0]) / 2.0
        
    parameters = [ ]
    
    if alpha != None:
        get_alpha = lambda parameters: alpha
    else:
        get_alpha = lambda parameters, nth=len(parameters): \
            _reflect(parameters[nth],_lower[1],_upper[1])
        parameters.append(1.0)

    if beta != None:
        get_beta = lambda parameters: beta
    else:
        get_beta = lambda parameters, nth=len(parameters): \
            _reflect(parameters[nth],_lower[2],_upper[2])
        parameters.append(0.0)
        
    if location != None:
        get_location = lambda parameters: location
    else:
        get_location = lambda parameters, nth=len(parameters): parameters[nth]
        parameters.append(guess_location)
    
    if scale != None:
        get_scale = lambda parameters: scale
    else:
        get_scale = lambda parameters, nth=len(parameters): N.exp(parameters[nth])
        parameters.append(N.log(guess_scale))
        
    def neglog_density(parameters):
        location = get_location(parameters)
        scale = get_scale(parameters)
        return N.sum(neglog_levy((x-location)/scale, get_alpha(parameters), get_beta(parameters))) \
               + (len(x) * N.log(scale))
              
    parameters = optimize.fmin(neglog_density, parameters, disp=0)

    return (get_alpha(parameters), get_beta(parameters), 
            get_location(parameters), get_scale(parameters),
            neglog_density(parameters))



def random(alpha, beta, shape=()):
    """ Generate random values sampled from an alpha-stable distribution. 
    """

    if alpha == 2:
        return RandomArray.standard_normal(shape) * N.sqrt(2.0)
    
    # Fails for alpha exactly equal to 1.0
    # but works fine for alpha infinitesimally greater or less than 1.0    
    radius = 1e-15 # <<< this number is *very* small
    if N.absolute(alpha-1.0) < radius: 
        # So doing this will make almost exactly no difference at all
        alpha = 1.0 + radius

    r1 = RandomArray.random(shape)
    r2 = RandomArray.random(shape)
    
    a=(1.0-alpha); b=(r1-0.5); c=((a*b)*3.1415926535897931); d=N.absolute((1.0-N.absolute(a))); e=N.tan((((((alpha*d)*-2.0)*N.arctan((beta*N.tan(((3.1415926535897931*alpha)/2.0)))))*3.1415926535897931)/((6.2831853071795862*d)*alpha))); f=(((-((N.cos(c)+(e*N.sin(c))))/(N.log(r2)*N.cos((b*3.1415926535897931))))**(a/alpha))-1.0); g=N.tan(((3.1415926535897931*b)/2.0)); h=N.tan((((3.1415926535897931*a)*b)/2.0)); i=(1.0-(g*g)); j=((((((a*f)/a)+1.0)*(((2.0*(g-h))*((g*h)+1.0))-(((((((((h*i)-(2.0*g))*b)*3.1415926535897931)*a)*e)*2.0)*h)/c)))/(i*((h*h)+1.0)))+(((a*e)*f)/a))
    
    return j

    #k_alpha = N.abs(1-N.abs(1-alpha))
    #beta_A = 2.0 * N.arctan(-beta * N.tan(N.pi*0.5*alpha)) / (N.pi*k_alpha)
    #gamma_B = N.cos(N.pi*beta_A*k_alpha*0.5)
        
    #Phi_0 = -0.5*N.pi*beta_A*k_alpha/alpha
    
    #beta_prime = -N.tan(0.5*N.pi*(1.0-alpha)) * N.tan(alpha*Phi_0)

    #epsilon = 1-alpha

    #Phi = (r1-0.5) * N.pi
    #W = -log(r2)
    
    #tau = -epsilon*N.tan(alpha*Phi_0)
    #a = N.tan(0.5*Phi)
    #b = N.tan(0.5*epsilon*Phi)
    
    #B = N.tan(0.5*epsilon*Phi)/(0.5*epsilon*Phi)
        
    #z = (N.cos(epsilon*Phi)-N.tan(alpha*Phi_0)*N.sin(epsilon*Phi)) / (W * N.cos(Phi))    
    #d = (z ** (epsilon/alpha) - 1.0) / epsilon
    
    #Y = ( 2.0*(a-b)*(1+a*b) - Phi*tau*B*(b*(1-a*a)-2*a) ) \
    #      / ((1-a*a)*(1+b*b)) \
    #      * (1+epsilon*d) \
    #    + tau*d

    #return Y


if __name__ == "__main__":
    if "build" in sys.argv[1:]:
        _make_data_file()
        
    print "Testing fit_levy."
    
    print "Should give 1.5, 0.5, 0.0, 1.0 ..."
    print fit_levy(random(1.5, 0.5, 1000))
    print
    
    print "Does it die when given silly data? ..."
    print fit_levy(N.array([0,0,0,0,0,0,0,0,0,0,1]))
    print
        
    
    print "Testing random."
    
    import pylab
    
    the_range = _make_range(-10.0, 10.0, 1000)
    for alpha, beta, nth in [ (0.5,0.0,421), (0.5,1.0,422), (1.0,0.0,423), (1.0,1.0,424),  (1.5,0.0,425), (1.5,1.0,426), (2.0, 0.0, 427), (2.0, 1.0, 428) ]:
        pylab.subplot(nth)    
        pylab.title("alpha=%.2f beta=%.2f" % (alpha, beta))
        pylab.hist(random(alpha, beta, 10000), bins=_make_range(-10.0, 10.0, 100), normed=1)
        pylab.plot(the_range, levy(the_range, alpha, beta), "r", linewidth=2.0)
        pylab.xlim(-10.0, 10.0)
        pylab.ylim(0.0, 0.55)
    
    pylab.show()
    
    print "Just being pretty."

    pylab.subplot(211)        
    for alpha in _make_range(0.5, 2.0, 10):
        for beta in _make_range(-1.0, 1.0, 10):
            pylab.plot(levy(_make_range(-5.0,5.0,1000), alpha, beta), 'g')
            
    pylab.subplot(212)        
    for alpha in _make_range(0.5, 2.0, 10):
        for beta in _make_range(-1.0, 1.0, 10):
            pylab.plot(levy(_make_range(-5.0,5.0,1000), alpha, beta, True), 'g')
            
    pylab.show()


