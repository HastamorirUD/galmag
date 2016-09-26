""" Contains functions to compute the free decay modes of the magnetic
    of the halo of a galaxy """
from scipy.special import j0, j1, jv, jn_zeros
import numpy as N

pi=N.pi
cos = N.cos
tan = N.tan
sin = N.sin
sqrt = N.sqrt

def get_B_a_1(r, theta, phi, C=0.346, k=pi):
    """ Computes the first (pure poloidal) antisymmetric free decay mode.
        Purely poloidal.
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, kspherical polar coordinates
        Output: B_r, B_\theta, B_\phi """

    # Computes radial component
    Q = N.empty_like(r)
    separator = r <=1
    Q[separator] = r[separator]**(-0.5)*jv(3.0/2.0,k*r[separator])
    Q[~separator] = r[~separator]**(-2.0)*jv(3.0/2.0,k)

    Br = C*(2.0/r)*Q*cos(theta)

    # Computes polar component
    # X = d(rQ1)/dr
    # http://is.gd/oBIDQo
    X = N.empty_like(r)
    y = k*r[separator]
    X[separator] = sqrt(2.0/pi)*(y**2*sin(y) - sin(y) +
                                 y*cos(y)) / (k**(-0.5)*y**2)
    X[~separator] = -1.*r[~separator]**(-2.0)*jv(3.0/2.0,k)

    Btheta = C*(-sin(theta)/r)*X

    # Sets azimuthal component
    Bphi   = N.zeros_like(r)

    return Br, Btheta, Bphi

def get_B_a_2(r, theta, phi, C=0.250, k=5.763):
    """ Computes the second antisymmetric free decay mode (one of a
        degenerate pair, with eigenvalue gamma_2=-(5.763)^2 .
        Purely poloidal.
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, k
        Output:
              B_r, B_\theta, B_\phi """
    # TODO This needs checking
    # Computes radial component

    separator = r <=1.
    Q = N.empty_like(r)
    Q[separator] = r[separator]**(-0.5)*jv(7.0/2.0, k*r[separator])
    Q[~separator] = r[~separator]**(-4.0)*jv(7.0/2.0, k)

    Br = Q*cos(theta)*(5.0*cos(2.*theta)-1.)*C*(2.0/r)

    # Computes polar component
    # X = d(rQ1)/dr
    # http://is.gd/B56vg9   k=a, r=x
    # r<=1, first define some auxiliary quantities
    y = k*r[separator]
    siny = sin(y)
    cosy=cos(y)
    A = 15.*siny/(y**3) - 15.*cosy/(y**2) - 6.*(siny/y) + cosy
    B =  -45.*siny/y**3/r[separator] +45.*cosy/y**2/r[separator] \
             +21.*siny/y/r[separator]  -k*siny - 6.*siny/r[separator]
    # Now proceeds analogously to the first decay mode

    X = N.empty_like(r)
    X[separator] = A/sqrt(2.*pi*r[separator]*y) - \
                k*sqrt(r[separator])*A/sqrt(2.*pi)/y**(3./2.) + \
                sqrt(2./pi)*B/sqrt(k)
    X[r>1] = 0.0 #-3.*jv(7.0/2.0,k)*r[~separator]**(-4)
    # Sets Btheta
    Btheta = C*(-sin(theta)/r)*(5.*(cos(theta))**2-1.)*X


    # Sets azimuthal component
    Bphi   = N.zeros_like(r)

    return Br, Btheta, Bphi


def get_B_a_3(r, theta, phi, C=3.445, k=5.763):
    """ Computes the third antisymmetric free decay mode (one of a
        degenerate pair, with eigenvalue gamma_2=-(5.763)^2 .
        Purely toroidal.
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, k
        Output: B_r, B_\theta, B_\phi """

    separator = r <=1.

    # Sets radial component
    Br = N.zeros_like(r)

    # Sets polar component
    Btheta = N.zeros_like(r)

    # Computes azimuthal component
    Q = N.empty_like(r)
    Q[separator] = r[separator]**(-0.5)*jv(5.0/2.0, k*r[separator])
    Q[~separator] = r[~separator]**(-3.0)*jv(5.0/2.0, k)

    Bphi = C*Q*sin(theta)*cos(theta)

    return Br, Btheta, Bphi


def get_B_a_4(r, theta, phi, C=0.244, k=(2.*pi)):
    """ Computes the forth antisymmetric free decay mode (one of a
        degenerate pair, with eigenvalue gamma_2=-(5.763)^2 .
        Purely poloidal.
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, k
        Output: B_r, B_\theta, B_\phi """

    # This happens to have the same form as the 1st antisymmetric mode
    return get_B_a_1(r, theta, phi,C=C,k=k)


def get_B_s_1(r, theta, phi, C=0.653646562698, k=4.493409457909):
    """ Computes the first (poloidal) symmetric free decay mode.
        Purely poloidal
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, kspherical polar coordinates
        Output: B_r, B_\theta, B_\phi """

    separator = r <=1.

    # Computes radial component
    Q = N.empty_like(r)
    Q[separator] = r[separator]**(-0.5)*jv(5.0/2.0,k*r[separator])
    Q[~separator]  = r[~separator]**(-3.0)*jv(5.0/2.0,k)

    Br = C*Q*(3.0*cos(theta)**2-1)/r

    # Computes theta component
    X = N.zeros_like(r)
    y = k*r[separator]
    siny = sin(y)
    cosy = cos(y)
    X[separator] = (3*siny/y**2 - siny - 3.*cosy/y)/sqrt(2*pi*y*r[r<=1]) \
      - k*sqrt(r[r<=1])*(3.*siny/y**2-siny-3.*cosy/y)/sqrt(2*pi)*y**(-3./2.)\
      + sqrt(2./pi*r[r<=1])*(-6.*siny*k/y**3+6.*cosy*k/y**2+3*siny*k/y-k*cosy)/(
                                                                        sqrt(y))
    X[~separator] = -2.0*r[~separator]**(-3.0)*jv(5.0/2.0,k)

    Btheta = C*(-sin(theta)*cos(theta)/r)*X

    # Sets azimuthal component
    Bphi   = N.zeros_like(r)

    return Br, Btheta, Bphi


def get_B_s_2(r, theta, phi, C=1.32984358196, k=4.493409457909):
    """ Computes the second symmetric free decay mode (one of a
        degenerate pair, with eigenvalue gamma_2=-(5.763)^2 .
        Purely toroidal.
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, k
        Output: B_r, B_\theta, B_\phi """

    separator = r <=1.

    # Sets radial component
    Br = N.zeros_like(r)

    # Sets theta component
    Btheta = N.zeros_like(r)

    # Computes azimuthal component
    Q = N.empty_like(r)
    Q[separator] = r[separator]**(-0.5)*jv(3.0/2.0, k*r[separator])
    Q[~separator] = r[~separator]**(-2.0)*jv(3.0/2.0, k)

    Bphi = C*Q*sin(theta)

    return Br, Btheta, Bphi

def get_B_s_3(r, theta, phi, C=0.0169610298034, k=6.987932000501):
    """ Computes the third symmetric free decay mode.
        Purely poloidal
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, kspherical polar coordinates
        Output: B_r, B_\theta, B_\phi """

    separator = r <=1.

    # Auxiliary
    cost = cos(theta)
    sint = sin(theta)
    y = k*r[separator]

    # Computes radial component
    Q = N.empty_like(r)
    Q[separator] = r[separator]**(-0.5)*jv(9.0/2.0,y)
    Q[~separator]  = r[~separator]**(-5.0)*jv(9.0/2.0,k)
    S = -700.*cost**4+600.*cost**2-60

    Br = C*Q*S/r

    # Computes theta component
    Q[separator] = Q[separator]/2.0 + r[separator]**(0.5)/2.0 * k  \
                                        * (jv(7.0/2.0,y) - jv(11.0/2.0,y))
    Q[~separator] = -4*r[~separator]**(-5.0)*jv(9.0/2.0,k)
    S = -140.0*cost**3*sint+60*cost*sint

    Btheta = -C * Q * S/r

    # Sets azimuthal component
    Bphi = N.zeros_like(r)

    return Br, Btheta, Bphi


def get_B_s_4(r, theta, phi, C=0.539789362061, k=6.987932000501):
    """ Computes the fourth symmetric free decay mode.
        Purely toroidal.
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              optional: C, k
        Output: B_r, B_\theta, B_\phi """

    separator = r <=1.

    # Sets radial component
    Br = N.zeros_like(r)

    # Sets theta component
    Btheta = N.zeros_like(r)

    # Computes azimuthal component
    Q = N.empty_like(r)
    Q[separator] = r[separator]**(-0.5)*jv(7.0/2.0, k*r[separator])
    Q[~separator] = r[~separator]**(-4.0)*jv(7.0/2.0, k)
    S = 3.*sin(theta)*(1.-5.*(cos(theta))**2)

    Bphi = -C*Q*S

    return Br, Btheta, Bphi

# Useful global variables
gamma_s = [-4.493409457909**2, -4.493409457909**2,
           -6.987932000501**2, -6.987932000501**2]
gamma_a = [-pi**2, -5.763**2, -5.763**2, -(2.*pi)**2]

symmetric_modes_list = [get_B_s_1, get_B_s_2, get_B_s_3, get_B_s_4]
antisymmetric_modes_list = [get_B_a_1, get_B_a_2, get_B_a_3, get_B_a_4]


def get_mode(r, theta, phi, n_mode, symmetric):
    """ Computes the n_mode'th free decay mode.
        (This is actually a wrapper invoking other functions)
        Input:
              r, theta, phi: NxNxN arrays containing, repectively,
              the radial, polar and azimuthal coordinates.
              n_mode: the index of the mode
              symmetry: 'symmetric' or 'antisymmetric'
        Output: B_r, B_\theta, B_\phi """

    if n_mode>4:
        raise NotImplementedError

    if symmetric:
        return symmetric_modes_list[n_mode-1](r, theta, phi)
    else:
        return antisymmetric_modes_list[n_mode-1](r, theta, phi)

