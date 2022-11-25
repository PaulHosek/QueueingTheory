import numpy as np
import simpy as sp

class Server():
    """ Class for a single server
    """
    def __init__(self, id, mu=0):
        """ Initialize a server with id and capacity
        """
        self.id = id
        self.mu = mu
        self.queue = []

        print(f"Server {id} started")


    def get_id(self):
        """ return the server ID
        """
        return (self.id)


    def get_load(self):
        """ Return the server load
        """
        return len(self.queue) / self.mu


    def check_capacity(self):
        """ Check if maximum server capacity is reached
            returns 1 if queue is not full 
            returns 0 if queue is full
        """
        if len(self.queue) < self.mu:
            return 1
        else:
            return 0


    def add_queue(self, message):
        """ Add message to the queue if it's not full
        """
        if self.check_capacity():
            self.queue.append(message)
        else:
            print("Maximum capacity reached, message ignored")


    def process_message(self):
        """ Remove message from queue with FIFO ordering
        """
        if len(self.queue != 0):
            print(f"Removed message {self.queue[0]}")
            self.queue.pop(0)
        else:
            print("Queue is empty")