import des_queue
import simpy as sip
import numpy as np
from collections import deque
import pandas as pd
import os
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import warnings
import DES
from scipy.stats import ttest_ind
plt.figure()
plt.close('all')
plt.rcParams["font.size"] = 15

def find_lowest_sign(col1,col2,alpha):
    """Find min entries needed for significance."""
    right = len(col1)-1
    while is_significant(right, col1, col2, alpha):
        right -= 1
        # print(ttest_ind(col1[:right], col2[:right])[1])
        # print(right)
    # print('last',right)
    return right +1

def is_significant(idx, col1, col2, alpha):
    """Do t-test and return if significant."""
    if ttest_ind(col1[:idx], col2[:idx])[1] < alpha:
        return True
    else:
        return False

def write_signif(n_means, comparison, rho, low_idx_sign, alpha, name):
    """Log the current data to the file with the experiment.
     If the file does not exist, make file and add header row.
     :return void
     """

    if not os.path.exists('signif_data'):
        os.makedirs("signif_data")

    # if file does not exist yet make one and write the column headers in it
    my_file = Path(os.path.join("signif_data", name + ".csv"))

    if not my_file.is_file():
        with open(os.path.join("signif_data", name + ".csv"), "w+") as f:
            wr = csv.writer(f)
            wr.writerow(["n_means","comparison", "rho", "low_idx_sign", "alpha"])

    # log the data
    with open(os.path.join("signif_data", name + ".csv"), "a") as f:

        wr = csv.writer(f)
        wr.writerow([n_means, comparison, rho, low_idx_sign, alpha])
    return None

def gen_signif_csv():
    """Read simulation results and generate the results for the significance comparison."""
    mulamb =  [(1,1.01),(1,1.02),(1,1.06),(1,1.1) ,(1,1.2), (1, 1.25),
               (1, 1.333), (1, 1.429), (1, 1.667), (1, 2.0), (1, 2.5),
               (1, 3.333), (1, 4.0), (1, 5.882), (1, 6.667), (1, 7.692),
               (1, 10.0), (1, 12.5), (1, 16.667), (1, 25.0), (1, 100.0)]
    rhowait = {1:[], 2:[], 4:[]}
    rhos = [l for m,l in mulamb]
    nr_means = 49
    alpha = 0.05
    for mu,lamd in mulamb:
        rho = np.round((1/lamd)/mu,2)

        all_means = np.empty((nr_means,5))
        for _,n in enumerate([1,2,4]):
            name = f"servers_{rho}_50"
            res, cutoffs = DES.waiting_times(name)
            results = res[n]
            ct = cutoffs[n]
            cur_means = [np.mean(results[ct[i]+int((ct[i+1]-ct[i])/2):ct[i+1]]) for i in range(len(ct)-1)]
            all_means[:,n] = cur_means
        for i,(a,b) in enumerate(zip([1,1,2],[2,4,4])):
            low_idx =find_lowest_sign(all_means[:,a],all_means[:,b],alpha)
            write_signif(nr_means, (a,b),rho,low_idx, alpha, f'iters_sign_data{nr_means}')