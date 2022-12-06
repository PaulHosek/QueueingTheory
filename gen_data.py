import DES
import numpy as np
import simpy as sip

# generate data
if __name__ == "__main__":
    mulamb = [(1, 1.25), (1, 1.333), (1, 1.429), (1, 1.667), (1, 2.0), (1, 2.5),
              (1, 3.333), (1, 4.0), (1, 5.0), (1, 5.882), (1, 6.667), (1, 7.692),
              (1, 10.0), (1, 12.5), (1, 16.667), (1, 25.0), (1, 5.0), (1, 100.0)]



    for mu,lamd in mulamb:
        rho = np.round((1/lamd)/mu,2)
        name = f'servers_{rho}'
        DES.run_simu(name, sip.Resource, mu, lamd, 50)
    # res, cutoffs = DES.waiting_times(name)
    print('done')