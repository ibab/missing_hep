
__all__ = ['calc_nbins', 'histpoints']

import numpy as np
import scipy.stats as stats
import scipy as sp

def calc_nbins(x, maximum=150):
    n =  (max(x) - min(x)) / (2 * len(x)**(-1/3) * (np.percentile(x, 75) - np.percentile(x, 25)))
    return min(n, maximum)

def bin_errors(N, errors, confidence=0.6827):
    alpha = 1 - confidence
    upper = np.zeros(len(N))
    lower = np.zeros(len(N))
    if errors == 'gamma':
        lower = stats.gamma.ppf(alpha / 2, N)
        upper = stats.gamma.ppf(1 - alpha / 2, N + 1)
    else:
        raise ValueError('Unknown distribution: {}'.format(errors))
    # clip lower bars
    lower[N==0] = 0
    return N - lower, upper - N

def histpoints(x, nbins=None, xerr=None, yerr='gamma', *kargs, **kwargs):
    import matplotlib.pyplot as plt

    if not nbins:
        nbins = calc_nbins(x)

    h, bins = np.histogram(x, bins=calc_nbins(x), *kargs, **kwargs)
    width = bins[1] - bins[0]
    center = (bins[:-1] + bins[1:]) / 2
    area = sum(h * width)

    lower, upper = bin_errors(h, yerr)

    if xerr == 'binwidth':
        xerr = width / 2

    plt.errorbar(center, h, xerr=xerr, yerr=(lower, upper), fmt='o', color='black', markersize=5)

    return center, h, area

