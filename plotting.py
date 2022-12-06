import DES
import numpy as np
import simpy as sip
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import statistics as st


def confidint(sigma, n, z):
    """
    Return confidence interval for random variable with n samples, std sigma, 
    and confidence level z
    :param sigma: Standard deviation of RV
    :param n: sample size
    :param z: confidence level
    :return: confidence interval
    """
    return (sigma * z) / np.sqrt(n)


def rho_v_wait(smallname):
    mulamb = [(1,1.2), (1,1.1), (1,1.06), (1,1.02), (1,1.01)]
    c = ['_', 'blue', 'black', '_', 'red']
    line = ['_', '-', ':', '_', '-']
    rhowait = {1:[], 2:[], 4:[]}
    rhos = [np.round((1/l)/m, 2) for m,l in mulamb]

    for rho in rhos:
        name = f"{smallname}_{rho}_50"
        res, cutoffs = DES.waiting_times(name)
        for n in [1,2,4]:
            results = res[n]
            ct = cutoffs[n]
            
            means_n = [np.mean(results[ct[i]+int((ct[i+1]-ct[i])/2):ct[i+1]]) for i in range(len(ct)-1)]
            means_n.append(np.mean(results[ct[-2]:ct[-1]]))
            t = rhowait[n]
            t.append([np.mean(means_n), confidint(np.std(means_n), 50, 1.96)])
            rhowait[n] = t

    fig, ax = plt.subplots()
    for k, v in rhowait.items():
        _, _, err = plt.errorbar(   rhos, np.array(v)[:,0], np.array(v)[:,1], 
                                    marker='o', markersize=4, label=k, 
                                    capsize=8, elinewidth=1, color=c[k])
        for e in err: e.set_linestyle(':')
    ax.set_xlabel('rho')
    ax.set_ylabel('Mean waiting times')
    plt.grid()
    plt.legend()
    plt.show()


def plots(res_dict, cutoffs):
    c = ['_', 'blue', 'black', '_', 'red']
    fig, ax = plt.subplots()
    for n in [4,2,1]:
        results = res_dict[n]
        ct = cutoffs[n]
        # ignore the fires half of the values, warmup
        means_n = [np.mean(results[ct[i]+int((ct[i+1]-ct[i])/2):ct[i+1]]) for i in range(len(ct)-1)]
        means_n.append(np.mean(results[ct[-2]:ct[-1]]))

        # Normal distribution plots
        mu, std = np.mean(means_n), np.std(means_n)
        x = np.linspace(mu - 3*std, mu + 5*std, 75)
        
        plt.plot(x, stats.norm.pdf(x, mu, std), 
                 label=f'{n} server normal distribution', color=c[n])
        print(f"{n} server mean waiting times: {mu}")

        # Histogram
        plt.hist(means_n, bins=int(len(means_n)/3), label=f'{n} server means', 
                 alpha=0.5, color=c[n], density=True,stacked=True)
    ax.set_xlim(0,max(means_n)*3/4)
    ax.set_xlabel('Waiting times')
    ax.set_ylabel('Frequency')
    plt.legend()
    plt.show()