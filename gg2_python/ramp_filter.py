import math
import numpy as np
from matplotlib import pyplot as plt


def ramp_filter(sinogram, scale, alpha=0.001):
    """ Ram-Lak filter with raised-cosine for CT reconstruction

    fs = ramp_filter(sinogram, scale) filters the input in sinogram (angles x samples)
    using a Ram-Lak filter.

    fs = ramp_filter(sinogram, scale, alpha) can be used to modify the Ram-Lak filter by a
    cosine raised to the power given by alpha."""

    # get input dimensions
    angles = sinogram.shape[0]
    n = sinogram.shape[1]
    max_freq = n

    # Set up filter to be at least as long as input
    m = np.floor(np.log(n) / np.log(2) + 2)
    m = int(2 ** m)

    max_freq = np.pi/scale

    # Linear function set up for filter
    filter_freqs = np.linspace(-max_freq, max_freq, m)

    # Take the absolute value divided by 2*pi to give the Ram-Lak filter
    trunc_filter = abs(filter_freqs)/(2*np.pi)

    # Flip the filter halves to match how the FFT is produced (0->positive, negative->0)
    trunc_filter = np.concatenate((trunc_filter[int(m/2):], trunc_filter[0:int(m/2)]))

    print(trunc_filter)
    plt.plot(trunc_filter)

    print('Ramp filtering...')

    # FFT the current sinogram in the r direction for all angles, with zero padding to match filter length
    current_fft = np.fft.fft(sinogram, axis=1, n=m)
    # Apply the filter to all FFTs
    filtered_fft = current_fft * trunc_filter[np.newaxis, :]
    # Invert the now filtered FFTs, setting the length back to the original input length
    filtered_sinogram = np.fft.ifft(filtered_fft, axis=1)[:, :n]

    return np.real(filtered_sinogram)
