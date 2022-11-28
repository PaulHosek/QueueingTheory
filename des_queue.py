import csv

import numpy as np
import simpy as sip
from collections import deque
import os
from datetime import datetime
from pathlib import Path
current_queue = deque()


class Message():
    """
    Class Message to send to the server. If needs queueing will be queued.
    """

    def __init__(self, env, duration_work, id, experiment_name):
        self.env = env
        self.duration_work = duration_work
        self.id = id
        self.experiment_name = experiment_name


    def __repr__(self):
        return f"This is an instance of class Message with duration work of {self.duration_work}, id {self.id}."

    # private method to avoid name collisions
    @staticmethod
    def __log_row(experiment_name,item_id,queue_len, start_request_time,entry_time,exit_time):
        """Log the current data to the file with the experiment.
         If the file does not exist, make file and add header row.
         :return void
         """

        if not os.path.exists('logged_data'):
            os.makedirs("logged_data")

        # if file does not exist yet make one and write the column headers in it
        my_file = Path(os.path.join("logged_data", experiment_name+".csv"))

        if not my_file.is_file():
            with open(os.path.join("logged_data", experiment_name+".csv"),"w+") as f:
                wr = csv.writer(f)
                wr.writerow(["experiment_name","ID","Queue_length","start_request_time","entry_time","exit_time","current_time"])

        # log the data
        cur_time = datetime.now()
        with open(os.path.join("logged_data", experiment_name+".csv"), "a") as f:

            wr = csv.writer(f)
            wr.writerow([experiment_name,item_id,queue_len, start_request_time,entry_time,exit_time,cur_time])
        return None


    def request_server(self, env, server):
        """
        Request a server to be allocated to do the work of the message and execute job when server is freed.
        Also, log timestamps for waiting time before reaching server/ in queue and total execution time.
        :param env: simpy.environment object
        :param server: server instance to process the message
        :return void
        """
        start_request_time = env.now
        current_queue.appendleft(self.id)

        # getting a process token
        with server.resource.request() as cur_request:
            yield cur_request
            # Found server
            # remove element if process granted access to server
            item_id = self.id
            current_queue.remove(self.id)
            entry_time = env.now
            # do job in current message
            yield env.process(server.do_job(self))
            exit_time = env.now

            #####################
            # logging
            self.__log_row(self.experiment_name,item_id,len(current_queue), start_request_time,entry_time,exit_time)
            # print("start_request_time", "entry_time", "exit_time", "exit_time - entry_time", "len(current_queue)")
            # print(start_request_time, entry_time, exit_time, exit_time - entry_time, len(current_queue))

            # Neet to be done here:
            # save results
            ######################
            return None


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


def des_simulation(env, n, mu, lamd, mean_duration_work, a, b, queue_type, experiment_name):
    """
    :param n: number of servers
    :param env: simpy environment
    :param mu: capacity per server/ single-server serving rate
    :param lamd: mean inter-arrival time
    :param mean_duration_work:
    :param a: inter-arrival time distribution function with mean(lamb)
    :param b: service-time distribution function with mean (mean_duration_work) generating (random) numbers according to some distibution
    :param experiment_name: string; name of the logging file
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
        cur_message = Message(env, b(mean_duration_work), id, experiment_name)
        id += 1

        # enter queue and wait until served
        env.process(cur_message.request_server(env, cur_server))

        if n ==1:
            # may want to simulate multiple servers with a single one than use this.
            yield env.timeout(a(lamd)/n)
        else:
            yield env.timeout(a(lamd)) # not sure if this works


def main_des(max_iter, n, mu, lamd, mean_duration_work, a=np.random.exponential, b=np.random.exponential,
             queue_type=sip.Resource, experiment_name="testing"):
    env = sip.Environment()
    env.process(des_simulation(env, n, mu, lamd, mean_duration_work, a, b, queue_type,experiment_name))
    env.run(until=max_iter)
    print("DES finished.")


if __name__ == "__main__":
    max_iter = 1000
    n = 1
    mu = 10
    lamd = 1
    mean_duration_work = 1
    a = np.random.exponential
    b = np.random.exponential
    queue_type = sip.Resource
    experiment_name = "testing"

    main_des(max_iter, n, mu, lamd, mean_duration_work, a, b, queue_type,experiment_name)
