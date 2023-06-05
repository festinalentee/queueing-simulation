class Event:
    def __init__(self, time, customer_id, assigned_server_id, type):
        self.time = time
        self.customer_id = customer_id
        self.assigned_server_id = assigned_server_id
        self.type = type
    
    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f'(event_time: {self.time}, customer_id: {self.customer_id}, assigned_server_id: {self.assigned_server_id}, type: {self.type})'