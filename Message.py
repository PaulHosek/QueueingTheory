import os
from pathlib import Path

import csv
from datetime import datetime
import Server as sv

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
    def __log_row(experiment_name,item_id,queue_len,start_request_time,entry_time,exit_time):
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
                wr.writerow(["ID","wait_time"])

        # log the data
        # cur_time = datetime.now()
        wait_time = entry_time - start_request_time
        with open(os.path.join("logged_data", experiment_name+".csv"), "a") as f:

            wr = csv.writer(f)
            wr.writerow([item_id,wait_time])
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
        server.add_queue(self.id)

        # getting a process token
        with server.resource.request() as cur_request:
            yield cur_request
            # Found server
            # remove element if process granted access to server
            item_id = self.id
            server.remove_queue(self.id)
            entry_time = env.now
            # do job in current message
            yield env.process(server.do_job(self))
            exit_time = env.now

            #####################
            # logging
            self.__log_row( self.experiment_name,
                            item_id,
                            server.queue_len(),
                            start_request_time,
                            entry_time,
                            exit_time)

            # Need to be done here:
            # save results
            ######################
            return None