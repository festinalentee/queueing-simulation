class Server:
    def __init__(self, server_id, service_time, is_busy, busy_until, current_load, total_load):
        self.server_id = server_id
        self.service_time = service_time
        self.is_busy = is_busy
        self.busy_until = busy_until
        self.current_load = current_load
        self.total_load = total_load
    
    def start_serving(self, time):
        self.is_busy = True
        departure_time = time + self.service_time                    
        self.busy_until = departure_time

    def release_server(self):
        self.is_busy = False
        self.busy_until = None
        self.current_load -= 1
    
    def __repr__(self):
        return f'(server_id: {self.server_id}, service_time: {self.service_time}, is_busy: {self.is_busy}, busy_until: {self.busy_until}, current_load: {self.current_load}, total_load: {self.total_load})'