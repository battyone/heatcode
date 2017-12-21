
""" Theoritcal solutions for some heat transfert problem
    from the book:
        Conduction of heat in solids
        Horatio Scott Carslaw, John Conrad Jaeger
        Clarendon Press, Dec 31, 1959
"""

""" semi-infinite solid. Initial temperature zero.
    Surface at temperature phi(t)
"""

import numpy as np
from scipy.special import erfc

def dealwithtype( x, t ):
    """ return x and t as an array
        broadcast values if shape of x != shape of y
        and neither x or t are scalar
    """
    x = np.asarray( x )
    t = np.asarray( t )

    if not x.shape and not t.shape:
        pass
    elif not x.shape:
        x = x*np.ones_like( t )
    elif not t.shape:
        t = t*np.ones_like( x )
    else:
        x, t = np.meshgrid( x, t )

    return x, t


def semiinfiniteconstant( x, t, V0, V1, T, khi ):
    """ Semi-infinite solid. Initial temperature zero.
        Surface at temperature phi(t)

        special case (i) :
            phi(t) = V0, constant, 0<t<T
            phi(t) = V1, constant, t>T

        ref. p. 63 - special case (i)

        Args:
            x: float, list, nd-array, position from the surface (x>0)
            t: float, list, nd-array, time
            V0, V1: float, surface temperatures before and after the transition
            T: float, transition time
            khi: float, material diffusivity (K/rhoC)

        Return:
            array of temperature, dim n*m
    """

    x, t = dealwithtype( x, t )

    condlist = [ t <= 0,
                 np.logical_and( t > 0 , t <= T ),
                 t > T ]

    my_erfc =  lambda t, x : erfc( x/2.0/np.sqrt(khi*t) )
    funclist = [ 0,
                 lambda t : V0*my_erfc( t, x[condlist[1]] ) ,
                 lambda t : V0*my_erfc( t, x[condlist[2]] ) + (V1-V0)*my_erfc( t-T, x[condlist[2]] ) ]

    v = np.piecewise( t, condlist, funclist )

    return v


def caractime( khi, d ):
    """ caracteristic diffusion time (c.a.d. the order of magnitude)
        for material diffusivity khi at the distance d
    """
    return d**2 / khi

def caracdistance( khi, t ):
    """ caracteristic diffusion distance (c.a.d. the order of magnitude)
        for material diffusivity khi at the time t
    """
    return np.sqrt( khi * t )



def semiinfiniteharmonic( x, t, A, T, khi ):
    """ Semi-infinite solid. Surface temperature a harmonic function of time
        Initial temperature zero. (Rq. no transient term)

        v(t) = A.cos( w.t )

        ref. p. 64 - paragraph 2.6

        Args:
            x: float, list, nd-array, position from the surface (x>0)
            t: float, list, nd-array, time
            A: float, amplitude of the temperatures variations
            T: float, period (second)
            khi: float, material diffusivity (K/rhoC)

        Return:
            array of temperature, dim n*m
    """

    x, t = dealwithtype( x, t )

    w = 2*np.pi/T
    k = np.sqrt( w/2.0/khi )

    v = A*np.exp(-k*x)*np.cos( w*t - k*x )

    return v
