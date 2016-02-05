""" This module is part of GMF tool

    A set of functions that compute the magnetic field produced by a
    galactic disk dynamo.

    All the functions receive a dictionary of parameters as input.
    The parameters are:
           'D_d'      -> the dynamo number
           'Ralpha_d' -> a measure of the mean induction by interstellar turb.
           'R_d' -> The radius of the dynamo active disk
           'Cn_d'     -> N-array containing the coefficients
           'h_d'      -> scale height of the dynamo active disk

    This will later be refactored to support a 'galaxy magnetic field' object,
    which will mostly behave as a numpy array, but supporting changing of
    coordinate system and containing generation/modification class methods.
"""

from scipy.special import j0, j1, jv, jn_zeros
import numpy as N
from scipy.integrate import nquad

import threading
lock = threading.Lock()

sqrt = N.sqrt
pi = N.pi
arctan2 = N.arctan2
cos = N.cos
sin = N.sin

B_norm = dict()

def get_B_disk_cyl_unnormalized(r, phi, z, kn, p):
    """ Computes the n component of the magnetic field produced  by a
        dynamo at a galactic disc. In cylindrical coordinates.
        Input:
            r,phi,z: cylindrical coordinatees (either scalar or
                     NxNxN-arrays generated by numpy.meshgrid)
            p: dictionary containing the parameters Ralpha and D
        Output:
            Br, Bphi, Bz: repectively the radial, azimuthal and
            vertical components of the computed field (format
            compatible with r,phi,z).
    """

    # Unpacks the parameters
    Ralpha = p['Ralpha_d']
    D =  p['D_d']

    # Computes the radial component
    Br = Ralpha*j1(kn*r) * (cos(pi*z/2.0) \
                                  +3.0*cos(3*pi*z/2.0)/(4.0*pi**1.5*sqrt(-D)))

    # Computes the azimuthal component
    Bphi = -2.0*j1(kn*r) * sqrt(-D/pi)*cos(pi*z/2.0)

    # Computes the vertical component
    Bz = -2.0 * Ralpha/pi * (j1(kn*r)+0.5*kn*r*(j0(kn*r)-jv(2,kn*r))) *(
         sin(pi*z/2.0)+sin(3*pi*z/2.0)/(4.0*pi**1.5*sqrt(-D)))

    return Br, Bphi, Bz

def __intregrand_compute_normalization(r, phi, z, kn, p):
    """ Private helper function for compute_normalization """
    Br, Bphi, Bz = get_B_disk_cyl_unnormalized(r,phi,z,kn,p)
    return r * Br*Br + Bphi*Bphi + Bz*Bz

def compute_normalization(kn, p):
    """ Renormalizes the magnetic field
        Input:
            kn:
            p:
        Ouptput:
            normalization factor
    """

    # Sets integration intervals
    r_range = [ 0, 1 ]
    phi_range = [ 0, 2.0*pi ]
    z_range = [ -1, 1 ]

    # Integrates
    lock.acquire()
    tmp = nquad(__intregrand_compute_normalization,
                [r_range, phi_range,z_range], args=(kn,p))
    lock.release()

    return tmp[0]**(-0.5)


def get_B_disk_cyl_component(r,phi,z,kn, p):
    """ Returns vector containing one _normalized_ component of the magnetic
        field produced  by a dynamo at a galactic disc. In cylindrical
        coordinates.
        Input: position vector with (r, phi, z) coordinates, the mode kn and
        the parameters dictionary, containing R_\alpha and the Dynamo number.
    """
    global B_norm

    # The normalization factors are _cached_ in the B_norm global
    # dictionary to allow faster re-execution
    if kn not in B_norm:
        B_norm[kn] = compute_normalization(kn, p)

    Br, Bphi, Bz = get_B_disk_cyl_unnormalized(r,phi,z,kn,p)

    return B_norm[kn]*Br, B_norm[kn]*Bphi, B_norm[kn]*Bz


def get_B_disk_cyl(r,phi,z, p):
    """ Computes the magnetic field associated with a disk galaxy
        Input:
            r,phi,z: NxNxN arrays containing the dimensionless cylindrical
                     coordinates
            p: dictionary containing the parameters (see module doc)
        Output:
            Bx, By, Bz: NxNxN arrays containing the components of the
                        disk magnetic field
    """
    Cns = p['Cn_d']
    number_of_bessel = len(Cns)
    mu_n =  jn_zeros(1, number_of_bessel)
    kns = mu_n

    for i, (kn, Cn) in enumerate(zip(kns,Cns)):
        if i==0:
            Br=0; Bphi=0; Bz=0

        Br_tmp, Bphi_tmp, Bz_tmp = get_B_disk_cyl_component(r,phi,z, kn,p)
        Br+=Cn*Br_tmp; Bz+=Cn*Bz_tmp; Bphi+=Cn*Bphi_tmp

    # Field should vanish outside h
    Br[abs(z)>1]=0
    Bphi[abs(z)>1]=0
    Bz[abs(z)>1]=0

    return Br, Bphi, Bz


def get_B_disk(r, p):
    """ Computes the magnetic field associated with a disk galaxy
        Input:
            r: 3xNxNxN array containing the cartesian coordinates
            p: dictionary containing the parameters (see module doc)
        Output:
            B: 3xNxNxN array containing the components of the
                        disk magnetic field
    """

    # Make variables dimensionless
    z_dl = r[2,...] / p['h_d']
    y_dl = r[1,...] / p['R_d']
    x_dl = r[0,...] / p['R_d']

    # Cylindrical coordinates
    rr = sqrt(x_dl**2+y_dl**2)
    phi = arctan2(y_dl,x_dl)  # Chooses the quadrant correctly!
                        # -pi < phi < pi
    # Computes the field
    Br, Bphi, Bz = get_B_disk_cyl(rr,phi,z_dl, p)

    # Converts back to cartesian coordinates
    B = N.empty_like(r)
    sin_phi = sin(phi) # this is probably more accurate than using phi
    cos_phi = cos(phi) # idem
    #sin_phi = y_dl/r # this is probably more accurate than using phi
    #cos_phi = x_dl/r # idem
    B[0,...] = (Br*cos_phi - Bphi*sin_phi)
    B[1,...] = (Br*sin_phi + Bphi*cos_phi)
    B[2,...] = Bz

    return B
