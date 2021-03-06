import numpy as np
import scipy
from scipy import interpolate
from ct_scan import ct_scan


def ct_calibrate(photons, material, sinogram, scale, correct=True):
    """ ct_calibrate convert CT detections to linearised attenuation
    sinogram = ct_calibrate(photons, material, sinogram, scale) takes the CT detection sinogram
    in x (angles x samples) and returns a linear attenuation sinogram
    (angles x samples). photons is the source energy distribution, material is the
    material structure containing names, linear attenuation coefficients and
    energies in mev, and scale is the size of each pixel in x, in cm."""

    # Get dimensions and work out detection for just air of twice the side
    # length (has to be the same as in ct_scan.m)
    n = sinogram.shape[1]

    # perform calibration, simulate with only air
    # Use ct_scan with an empty phantom, since it fills surrounding space with air
    calib_phantom = np.zeros((n, n))
    calib_phantom.fill(material.name.index('Air'))
    calib_sinogram = ct_scan(photons, material, calib_phantom, scale, 1)

    attenuation = -np.log(sinogram/calib_sinogram)

    return attenuation



