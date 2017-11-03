# -*- coding: utf-8 -*-
""" Fast Fourier Transform module
This module is in charge of providing utilities for computing FFTs.
"""
import logging

import numpy as np

_logger = logging.getLogger(__name__)


def fft(x):
    """ Calculates the Fast Fourier Transform to the given series.
    Params:
        x (array): The series to which the FFT must be computed.
    Returns:
        array: The computed FFT of the given series.
    """
    if x is None or not isinstance(x, np.ndarray):
        _logger.debug("The given series is null or is not a numpy array")
        raise ValueError("The series must be a non null numpy array")
    # As we know its going to have a complex part, we need to specifically set the type to admit complex
    x = np.asarray(x, dtype=np.complex)
    n = len(x)
    if n <= 1:
        return x

    if 2 ** int(round(np.log2(n))) != n:
        _logger.debug("The given series length is not a power of 2")
        raise ValueError("Size of n must be a power of 2")

    even_indexed = fft(x[0::2])
    odd_indexed = fft(x[1::2])

    x_k = np.concatenate([even_indexed, odd_indexed])

    for k in range(0, n // 2, 1):
        k_value = x_k[k]
        x_k[k] = k_value + np.exp(-2j * np.pi * k / n) * x_k[k + n // 2]
        x_k[k + n // 2] = k_value - np.exp(-2j * np.pi * k / n) * x_k[k + n // 2]
    return x_k


def fftshift(x):
    """Rearranges a Fourier transform x by shifting the zero-frequency component to the center of the array.
    Params:
        x (array): The series to be shifted
    Returns:
        array: The shifted series.
    """
    if x is None or not isinstance(x, np.ndarray):
        _logger.debug("The given series is null or is not a numpy array")
        raise ValueError("The series must be a non null numpy array")
    return np.roll(x, len(x) / 2)
