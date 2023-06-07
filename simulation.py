import random
import heapq
import numpy as np
from event import Event
from customer import Customer
from server import Server

class Simulation:
    def __init__(self, arrival_rate, service_rate, num_customers, num_servers, servers_speed):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.num_customers = num_customers
        self.num_servers = num_servers
        self.servers_speed = servers_speed
        self.current_customers = 0
        self.servers = self.initialize_servers(self.get_service_rates())
        self.customers = self.initialize_customers()
        self.event_queue = []
        self.waiting_queue = []
        self.total_time_spent = 0
        self.max_time_spent = 0
        self.queue_size = [0]
    
    def get_interarrival_time(self, arrival_rate):
        return random.expovariate(arrival_rate)
    
    def get_service_time(self, service_rate):
        return random.expovariate(service_rate)

    def get_service_rates(self):
        service_rates = []
        for i in range(self.num_servers):
            if self.servers_speed == 'same':
                service_rates.append(self.service_rate)
            if self.servers_speed == 'different_1':
                service_rates.append(2.0 ** i)
            elif self.servers_speed == 'different_2':
                service_rates.append(i)
            elif self.servers_speed == 'different_3':
                service_rates.append(0.1 if i < (self.num_servers / 2) else 1.0)
        return service_rates

    def initialize_servers(self, service_rates):
        return [Server(i, service_rates[i], False, None, 0, 0) for i in range(self.num_servers)]

    def initialize_customers(self):
        return [Customer(i, 0, 0, 0, None) for i in range(self.num_customers)]

    def schedule_new_event(self, time, customer_id, assigned_server_id, type):
        heapq.heappush(self.event_queue, Event(time, customer_id, assigned_server_id, type))

    def select_server_uniformly(self):
        return random.choice(self.servers)
    
    def select_server_uniformly_with_power_of_d_choices(self, d_choices, servers_speed):
        d_servers = random.sample(self.servers, d_choices)
        minimum_load = min(server.current_load for server in d_servers)
        servers_with_equal_load = [server for server in d_servers if server.current_load == minimum_load]
        if servers_speed == 'different':
            fastest_from_equal_load = [server for server in servers_with_equal_load if server.service_time == min(server.service_time for server in servers_with_equal_load)]
            return fastest_from_equal_load[0]
        else:
            return random.choice(servers_with_equal_load)
            # Try choose first from list server_with_equal_load

    def run(self, scenario, d_choices, servers_speed):
        self.schedule_new_event(0, 0, None, 'arrival')
        interarrival_time = self.get_interarrival_time(self.arrival_rate)

        while self.event_queue:
            event = heapq.heappop(self.event_queue) # time, customer_id, assigned_server_id, type
        
            if event.type == 'arrival':
                self.current_customers += 1

                if self.current_customers < self.num_customers:
                    # Schedule next customer arrival
                    self.schedule_new_event(event.time + interarrival_time, event.customer_id + 1, None, 'arrival')
                
                if scenario == 'uniform server selection':
                    choosen_server = self.select_server_uniformly()
                
                elif scenario == 'uniform server selection with power of d-choices':
                    choosen_server = self.select_server_uniformly_with_power_of_d_choices(d_choices, servers_speed)
                else:
                    raise Exception('Unknown scenario')

                choosen_server.current_load += 1
                choosen_server.total_load += 1
                customer = self.customers[event.customer_id]
                customer.arrival_time = event.time
                customer.assigned_server_id = choosen_server.server_id
                customer.service_time = self.get_service_time(choosen_server.service_rate)

                if not choosen_server.is_busy:
                    choosen_server.start_serving(event.time, customer.service_time)
                    self.total_time_spent += customer.service_time
                    self.max_time_spent = max(self.max_time_spent, customer.service_time)
                    # Schedule the departure event for the customer
                    self.schedule_new_event(choosen_server.busy_until, event.customer_id, choosen_server.server_id, 'departure')
                else:
                    # If the chosen server is busy, add a customer to the waiting queue
                    self.waiting_queue.append(customer)
                    self.queue_size.append(len(self.waiting_queue))  
            
            elif event.type == 'departure': 
                server = self.servers[event.assigned_server_id]
                server.release_server()

                # If for this server is assigned customer in waiting_queue, start serving first from the list
                for waiting_customer in self.waiting_queue:
                    if waiting_customer.assigned_server_id == event.assigned_server_id:
                        server.start_serving(event.time, waiting_customer.service_time)
                        waiting_time = event.time - waiting_customer.arrival_time
                        time_spent = waiting_time + waiting_customer.service_time
                        self.total_time_spent += time_spent
                        self.max_time_spent = max(self.max_time_spent, time_spent)
                        # Schedule the departure event for the customer
                        self.schedule_new_event(server.busy_until, event.customer_id, event.assigned_server_id, 'departure')
                        # Remove customer from the waiting queue
                        self.waiting_queue.remove(waiting_customer)
                        break   

        avg_time_spent = (self.total_time_spent) / (self.current_customers)
        server_utilization = [round((server.total_load / self.current_customers) * 100, 4) for server in self.servers]
        avg_queue_size = np.mean(self.queue_size)

        return avg_time_spent, self.max_time_spent, server_utilization, avg_queue_size