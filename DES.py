import Server as sv
import Message as ms

import simpy as sip
import numpy as np


def des_simulation(env, n, mu, lamd, a, b, queue_type, experiment_name):
    """
    :param n: number of servers
    :param env: simpy environment
    :param mu: capacity per server/ single-server serving rate
    :param lamd: mean inter-arrival time
    :param a: inter-arrival time distribution function with mean(lamb)
    :param b: service-time distribution function with mean (mu) generating (random) numbers according to some distibution
    :param experiment_name: string; name of the logging file
    :return: void
    """
    # Generate as many servers as needed
    cur_server = sv.Server(env, n, mu, queue_type)
    
    # Give incomming messages unique idss such that we can identify them later.
    id = 0
    # keep generating messages in whilst Servers process them
    # now the queue can grow up if rho > 1
    while True:
        # generate new message with some duration_work according to b
        cur_message = ms.Message(env, b(mu), id, experiment_name)
        id += 1

        # enter queue and wait until served
        env.process(cur_message.request_server(env, cur_server))
        yield env.timeout(a(lamd))


def main_des(max_iter, n, mu, lamd, a, b, queue_type, experiment_name):
    env = sip.Environment()
    env.process(des_simulation(env, n, mu, lamd, a, b, queue_type,experiment_name))
    env.run(until=max_iter)
    # print(f"DES {n} servers finished.")


def loading_bar(i):
    if i == 99:
        done = 10 * u"\u2588"
        print(f"Running simulations: {done}")
    else:
        if i % 2 == 0:
                loading = '+'
        else:
            loading = 'x'
        done, todo = int(i/10) * u"\u2588", int(np.floor((100 - i) / 10)-1) * "_"
        print(f"Running simulations: {done}{loading}{todo}", end ='\r', flush=True)


def des_tests():
    """ TO DO: add tests 
    """
    pass