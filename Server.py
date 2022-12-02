import simpy as sip
# import Message as message
from collections import deque

class Server(object):

    def __init__(self, env, n, mu, resource_func=sip.Resource):
        # pass the number of servers to the resource function
        self.resource = resource_func(env, n)
        self.env = env
        self.mu = mu
        self.n = n
        # change resource function for different queuing order
        self.resource_f = resource_func
        self.queue = deque()

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
    
    def add_queue(self, message):
        if type(message) == int:
            self.queue.appendleft(message)
            return 1
        else:
            return 0

    def remove_queue(self, message):
        if message in self.queue:
            self.queue.remove(message)
            return 1
        else:
            return 0
    
    def queue_len(self):
        return len(self.queue)

    def do_job(self, message):
        """
        Do job with duration of message object duration work.
        :param message: message object
        :return: void
        """
        # "process" the job from the message and yield timepoint of finishing
        yield self.env.timeout(message.duration_work)