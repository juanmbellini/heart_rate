import numpy as np


def fft(x):

    """As we know its going to have a complex part, we need to specifically set the type to admit complex"""
    x = np.asarray(x, dtype=np.complex)

    N = len(x)

    if N <= 1:
        return x

    if 2 ** int(round(np.log2(N))) != N:
        raise ValueError("Size of N must be a power of 2")

    evenIndexed = fft(x[0::2])
    oddIndexed = fft(x[1::2])

    x_k = np.concatenate([evenIndexed, oddIndexed])

    for k in range(0, N//2, 1):
        kValue = x_k[k]
        x_k[k] = kValue + np.exp(-2j * np.pi * k / N) * x_k[k + N // 2]
        x_k[k + N // 2] = kValue - np.exp(-2j * np.pi * k / N) * x_k[k + N // 2]
    return x_k


def fftshift(x):

    """Rearranges a Fourier transform X by shifting the zero-frequency component to the center of the array."""

    return np.roll(x,len(x)/2)