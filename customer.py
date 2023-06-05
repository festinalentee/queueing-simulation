class Customer:
    def __init__(self, arrival_time, customer_id, assigned_server_id, event_type):
        self.arrival_time = arrival_time
        self.customer_id = customer_id
        self.assigned_server_id = assigned_server_id
        self.event_type = event_type
    
    def __repr__(self):
        return f'(arrival_time: {self.arrival_time}, customer_id: {self.customer_id}, assigned_server_id: {self.assigned_server_id}, type: {self.event_type})'