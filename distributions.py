import numpy as np

def hyperexponential(seed_1=None, seed_2=None, loopidx=None):
    """
    Generate long-tailed hyperexponential distribution.
    :param seed_1:
    :param seed_2:
    :param loopidx: index of the loop/ message id (e.g, id)
    :return:
    """
    if loopidx != None:
        seed_1 += loopidx
        seed_2 += loopidx*2
    rng_1 = np.random.default_rng(seed_1)
    rng_2 = np.random.default_rng(seed_2)
    if rng_2.integers(0,4,1) == 0:
        return rng_1.exponential(5)
    else:
        return rng_1.exponential(1)

def constant_dist(mean):
    """Constant distribution."""
    return mean

