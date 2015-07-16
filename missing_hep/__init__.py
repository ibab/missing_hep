
from __future__ import division


from fourmomentum import FourMomentum
__all__ = ['calc_nbins', 'histpoints', 'FourMomentum']

import numpy as np
import scipy.stats as stats
import scipy as sp
import logging

def calc_nbins(x, maximum=150):
    n =  (max(x) - min(x)) / (2 * len(x)**(-1/3) * (np.percentile(x, 75) - np.percentile(x, 25)))
    return min(n, maximum)

def poisson_limits(N, kind, confidence=0.6827):
    alpha = 1 - confidence
    upper = np.zeros(len(N))
    lower = np.zeros(len(N))
    if kind == 'gamma':
        lower = stats.gamma.ppf(alpha / 2, N)
        upper = stats.gamma.ppf(1 - alpha / 2, N + 1)
    elif kind == 'sqrt':
        lower = sqrt(N)
        upper = lower
    else:
        raise ValueError('Unknown distribution: {}'.format(kind))
    # clip lower bars
    lower[N==0] = 0
    return N - lower, upper - N

def histpoints(x, bins=None, xerr=None, yerr='gamma', normed=False, **kwargs):
    import matplotlib.pyplot as plt

    if bins is None:
        bins = calc_nbins(x)

    h, bins = np.histogram(x, bins=bins)
    width = bins[1] - bins[0]
    center = (bins[:-1] + bins[1:]) / 2
    area = sum(h * width)

    if isinstance(yerr, str):
        yerr = poisson_limits(h, yerr)

    if xerr == 'binwidth':
        xerr = width / 2

    if normed:
        h = h / area
        yerr = yerr / area

    if not 'color' in kwargs:
        kwargs['color'] = 'black'

    if not 'fmt' in kwargs:
        kwargs['fmt'] = 'o'

    if not 'markersize' in kwargs:
        kwargs['markersize'] = 5

    plt.errorbar(center, h, xerr=xerr, yerr=yerr, **kwargs)

    return center, h, area

