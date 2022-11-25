import numpy as np
import simpy
import simpy as sip
from collections import deque

current_queue = deque()


class Message():
    """
    Class Message to send to the server. If needs queueing will be queued.
    """

    def __init__(self, env, duration_work, id):
        self.env = env
        self.duration_work = duration_work
        self.id = id


    def __repr__(self):
        return f"This is an instance of class Message with duration work of {self.duration_work}, id {self.id}."

    def request_server(self, env, server):
        """
        Request a server to be allocated to do the work of the message and execute job when server is freed.
        Also, log timestamps for waiting time before reaching server/ in queue and total execution time.
        :param env: simpy.environment object
        :param server: server instance to process the message
        :return:
        """
        start_request_time = env.now
        current_queue.appendleft(self.id)

        # getting a process token
        with server.resource.request() as cur_request:
            yield cur_request
            # Found server
            # remove element if process granted access to server
            current_queue.remove(self.id)
            entry_time = env.now
            # do job in current message
            yield env.process(server.do_job(self))
            exit_time = env.now

            #####################
            # logging

            print("start_request_time", "entry_time", "exit_time", "exit_time - entry_time", "len(current_queue)")
            print(start_request_time, entry_time, exit_time, exit_time - entry_time, len(current_queue))

            # save results somewhere entry time, exit time, delta_time, len(current_queue)
            # Neet to be done here:
            # save results
            ######################


class Server(object):

    def __init__(self, env, n, mu, resource_func=sip.Resource):
        # pass the number of servers to the resource function
        self.resource = resource_func(env, n)
        self.env = env
        self.mu = mu
        self.n = n
        # change resource function for different queuing order
        self.resource_f = resource_func

    def __repr__(self):
        if isinstance(self.resource_f, sip.Resource):
            cur_resource_f = "FIFO-queue"
        elif isinstance(self.resource_f, sip.PriorityResource):
            cur_resource_f = "shortest-job-first-scheduling queue"
        else:
            cur_resource_f = self.resource_f
        return f"This is an instance of the Server class {self.n} servers, capacity mu of {self.mu}" \
               f" and queue of type {cur_resource_f}. "

    def set_queue_type(self, new_resource_func):
        """
        Change the type of the queue used.
        :param new_resource_func: simpy resources class
        :return: void
        """
        self.resource = new_resource_func
        assert isinstance(self.resource, sip.resources), \
        f"new resource is not of type {type(sip.Resource)}" \
        f" but of type {type(self.resource)}"
        return None

    def do_job(self, message):
        """
        Do job with duration of message object duration work.
        :param message: message object
        :return: void
        """
        # "process" the job from the message and yield timepoint of finishing
        yield self.env.timeout(message.duration_work)


def des_simulation(env, n, mu, lamd, mean_duration_work, a, b, queue_type):
    """
    :param n: number of servers
    :param env: simpy environment
    :param mu: capacity per server/ single-server serving rate
    :param lamd: mean inter-arrival time
    :param mean_duration_work:
    :param a: inter-arrival time distribution function with mean(lamb)
    :param b: service-time distribution function with mean (mean_duration_work) generating (random) numbers according to some distibution
    :return: void
    """
    # Generate as many servers as needed
    cur_server = Server(env, n, mu, queue_type)
    # Give incomming messages unique idss such that we can identify them later.
    id = 0
    # keep generating messages in whilst Servers process them
    # now the queue can grow up if rho > 1
    while True:
        # generate new message with some duration_work according to b
        cur_message = Message(env, b(mean_duration_work), id)
        id += 1

        # enter queue and wait until served
        env.process(cur_message.request_server(env, cur_server))

        if n ==1:
            # may want to simulate multiple servers with a single one than use this.
            yield env.timeout(a(lamd)/n)
        else:
            yield env.timeout(a(lamd)) # not sure if this works


def main_des(max_iter, n, mu, lamd, mean_duration_work, a=np.random.poisson, b=np.random.poisson,
             queue_type=sip.Resource):
    env = sip.Environment()
    env.process(des_simulation(env, n, mu, lamd, mean_duration_work, a, b, queue_type))
    env.run(until=max_iter)
    print("DES finished.")


if __name__ == "__main__":
    max_iter = 1000
    n = 1
    mu = 10
    lamd = 1
    mean_duration_work = 1
    a = np.random.poisson
    b = np.random.poisson
    queue_type = sip.Resource

    main_des(max_iter, n, mu, lamd, mean_duration_work, a, b, queue_type)
