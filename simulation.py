import random
import heapq
import numpy as np
from event import Event
from customer import Customer
from server import Server


class Simulation:
    def __init__(self, arrival_rate, service_rate, num_servers, num_customers, servers_speed):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.num_servers = num_servers
        self.num_customers = num_customers
        self.servers_speed = servers_speed
        self.current_customers = 0
        self.servers = self.initialize_servers(self.get_service_rates())
        self.customers = self.initialize_customers()
        self.event_queue = []
        self.waiting_queue = []
        self.total_time_spent = 0
        self.max_time_spent = 0
        self.busy_servers = 0 
        self.queue_size = []
        self.interarrivals = []
    
    def get_interarrival_time(self, arrival_rate):
        return random.expovariate(arrival_rate)

    def get_service_time(self, service_rate):
        return random.expovariate(service_rate)

    def get_service_rates(self):
        service_rates = []
        for i in range(1, self.num_servers + 1):
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
        return [Server(i, service_rates[i], False, None, 0, 0, 0) for i in range(self.num_servers)]

    def initialize_customers(self):
        return [Customer(i, 0, 0, 0, None) for i in range(self.num_customers)]

    def schedule_new_event(self, time, customer_id, assigned_server_id, type):
        heapq.heappush(self.event_queue, Event(time, customer_id, assigned_server_id, type))

    def select_server_uniformly(self):
        return random.choice(self.servers)
    
    def select_server_uniformly_with_power_of_d_choices(self, d_choices):
        d_servers = random.sample(self.servers, d_choices)
        if self.servers_speed == 'same':
            min_load = min(server.current_load for server in d_servers)
            servers_with_equal_load = [server for server in d_servers if server.current_load == min_load]
            return random.choice(servers_with_equal_load)
        elif self.servers_speed.startswith('different'):
            for server in d_servers:
                server.total_queue_time = server.current_load * server.service_rate
            min_total_queue_time = min(server.total_queue_time for server in d_servers)
            servers_with_equal_total_queue_time = [server for server in d_servers if server.total_queue_time == min_total_queue_time]
            return random.choice(servers_with_equal_total_queue_time)
            

    def run(self, scenario, d_choices):
        self.schedule_new_event(0, 0, None, 'arrival')

        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            
            interarrival_time = self.get_interarrival_time(self.num_servers * self.arrival_rate)
            self.interarrivals.append(interarrival_time)
            if event.type == 'arrival':
                self.current_customers += 1

                if self.current_customers < self.num_customers:
                    # Schedule next customer arrival
                    self.schedule_new_event(event.time + interarrival_time, event.customer_id + 1, None, 'arrival')
                if scenario == 'uniform server selection':
                    choosen_server = self.select_server_uniformly()
                
                elif scenario == 'uniform server selection with power of d-choices':
                    choosen_server = self.select_server_uniformly_with_power_of_d_choices(d_choices)
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
            
            busy_servers = sum(server.is_busy for server in self.servers)
            self.queue_size.append(len(self.waiting_queue) / busy_servers) if busy_servers >= 1 else self.queue_size.append(0)


        avg_time_spent = (self.total_time_spent) / (self.current_customers)
        server_utilization = [server.total_load for server in self.servers]
        avg_queue_size = np.mean(self.queue_size)

        return avg_time_spent, self.max_time_spent, server_utilization, avg_queue_size