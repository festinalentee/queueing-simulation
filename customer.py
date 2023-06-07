class Customer:
    def __init__(self, customer_id, arrival_time, assigned_server_id, service_time, event_type):
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.assigned_server_id = assigned_server_id
        self.service_time = service_time
    
    def __repr__(self):
        return f'(arrival_time: {self.arrival_time}, customer_id: {self.customer_id}, assigned_server_id: {self.assigned_server_id}, service_time: {self.service_time})'