import random

class Server:
    def __init__(self, server_id, service_rate, is_busy, busy_until, current_load, total_load, total_queue_time):
        self.server_id = server_id
        self.service_rate = service_rate
        self.is_busy = is_busy
        self.busy_until = busy_until
        self.current_load = current_load
        self.total_load = total_load
        self.total_queue_time = total_queue_time
    
    def start_serving(self, time, service_time):
        self.is_busy = True
        departure_time = time + service_time                    
        self.busy_until = departure_time

    def release_server(self):
        self.is_busy = False
        self.busy_until = None
        self.current_load -= 1
    
    def __repr__(self):
        return f'(server_id: {self.server_id}, service_rate: {self.service_rate}, is_busy: {self.is_busy}, busy_until: {self.busy_until}, current_load: {self.current_load}, total_load: {self.total_load})'