import numpy as np


def k(T):
    '''
    k( T ) - Thermal conductivity for Silicon
    dependancy with Temperature
    from 50K to 1681K 

    Reference:
      Glassbrenner, C. J., & Slack, G. A. (1964).
      Thermal Conductivity of Silicon and Germanium from 3°K to the Melting Point.
      Physical Review, 134(4A), A1058–A1069.
      https://doi.org/10.1103/PhysRev.134.A1058

    Units :
      T in Kelvin
      k in W/m/K
    ''' 
    T_exp = np.array([50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 250, 300,
             400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300,
             1400, 1500, 1600, 1681])  # K

    K_exp = np.array([26., 21., 17, 13.9, 11.4, 9.5, 6.0, 4.2, 3.25, 2.66, 
             1.95, 1.56, 1.05, 0.80, 0.64, 0.52, 0.43, 0.356, 0.31, 
             0.280, 0.261, 0.248, 0.237, 0.227, 0.219, 0.216]) # Kexp in  W/cm/deg
    K_exp = K_exp * 100  # conversion to  W/m/deg

    k = np.interp(T, T_exp, K_exp)
    return k



def Cp( T ):
    '''
    Cpi(T) - Specific heat capacity for Silicon
    per unit mass
    dependancy with Temperature
    from 60K to 1681K 

    Reference:
    http://www.matweb.com/search/DataSheet.aspx?MatGUID=7d1b56e9e0c54ac5bb9cd433a0991e27&ckck=1

    Units :
        T in Kelvin
        Cp in J/kg/K
    '''
    
    T_exp = np.array([-213, -173, -73, 27, 127, 227, 327, 427, 527, 627, 727, 
        827, 927, 1027, 1127, 1227, 1412 ])  #  in degC
    Cp_exp = np.array([0.115, 0.259, 0.557, 0.713, 0.785, 0.832, 0.849, 0.866,
        0.883, 0.899, 0.916, 0.933, 0.950, 0.967, 0.983, 1, 1.01])  # in J/g/K
     
    T_exp = T_exp + 273.15  # conversion to K
    Cp_exp = Cp_exp*1e3  # conversion to J/kg/K
    
    Cp = np.interp(T, T_exp, Cp_exp)
    return Cp


def CTE(T):
    """ tangent CTE for silicon
        from Okada, Y., & Tokumaru, Y. (1984).
        Precise Determination of Lattice-Parameter and Thermal-Expansion
        Coefficient of Silicon between 300 K and 1500 K.
        Journal of Applied Physics, 56(2), 314–320.
        https://doi.org/10.1063/1.333965
        
        Units :
            T in Kelvin
            alpha in 1/K
    """
    #return (1-np.exp(-5.88e-3*(T-124)))*3.725e-6 + 5.548e-10*T   # another source...
    return 3.725*(1 - np.exp(-5.88e-3*(T - 124)) + 5.548e-4*T )*1e-6
    
