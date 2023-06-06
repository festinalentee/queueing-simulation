import random
import os
import json
from server import Server
from simulation import Simulation


def get_interarrival_time(arrival_rate):
    return random.expovariate(arrival_rate)

def get_service_time(service_rate):
    return random.expovariate(1.0 / service_rate)

def initialize_servers(service_time, num_servers):
    return [Server(i, service_time[i], False, None, 0, 0) for i in range(num_servers)]

def run_experiment(params):
    data = {'avg_time_spent': [], 'max_time_spent': [], 'server_utilization': [], 'avg_queue_size': [], 'server_speed_to_load': [], 'interarrival_time': []}
    
    for i in range(0, params['num_experiments']):
        servers = initialize_servers(params['service_times'][i], params['num_servers'])
        simulation = Simulation(params['interarrival_times'][i], servers, params['num_servers'], params['num_customers'])
        avg_time_spent, max_time_spent, server_utilization, avg_queue_size = simulation.run(params['scenario'], params['d_choices'], params['servers_speed'])
        data['avg_time_spent'].append(avg_time_spent)
        data['max_time_spent'].append(max_time_spent)
        data['server_utilization'].append(server_utilization)
        data['avg_queue_size'].append(avg_queue_size)
        data['server_speed_to_load'].extend(list(zip([s.service_time for s in servers], server_utilization)))
        data['interarrival_time'].append(params['interarrival_times'][i])
    
    data['server_speed_to_load'].sort(key=lambda x: x[0])
    
    return data

def save_experiment_to_file(data, filename):
    folder_path = './experiments/'
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def save_experiments_to_files(data):
    folder_path = f'./experiments/{service_rate}_{num_servers}_{num_customers}_{num_experiments}'
    os.makedirs(folder_path, exist_ok=True)
    for key, value in data.items():
        filename = f"{key}.json"
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as file:
            json.dump(value, file)


results = {}
s1_uss, s1_uss_d2, s1_uss_d3, s1_uss_d5 = {}, {}, {}, {}
s2_uss, s2_uss_d2, s2_uss_d3, s2_uss_d5, s2_nuss_d2, s2_nuss_d3, s2_nuss_d5 = {}, {}, {}, {}, {}, {}, {}

service_rate = 1.0
num_servers = 100
num_customers = 10000
num_experiments = 100

for arrival_rate in [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999]:
    print(f'\n{arrival_rate}')
    random.seed(0)
    interarrival_times = []
    same_service_times = []
    different_service_times = []
    service_time = get_service_time(service_rate)
    for _ in range(0, num_experiments):
        interarrival_times.append(get_interarrival_time(arrival_rate))
        same_service_times.append([service_time for _ in range(num_servers)])
        different_service_times.append([get_service_time(service_rate) for _ in range(num_servers)])

    interarrival_times.sort()

    print('SCENARIO_1')
    print('1: s1_uss')
    results.setdefault('s1_uss', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': same_service_times,
        'scenario': 'uniform server selection', 
        'd_choices': 0, 
        'servers_speed': 'same'})    
    
    print('2: s1_uss_d2')
    results.setdefault('s1_uss_d2', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': same_service_times,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': 2, 
        'servers_speed': 'same'})

    print('3: s1_uss_d3')
    results.setdefault('s1_uss_d3', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': same_service_times,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': 3, 
        'servers_speed': 'same'})

    print('4: s1_uss_d5')
    results.setdefault('s1_uss_d5', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': same_service_times,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': 5, 
        'servers_speed': 'same'})
    
    print('SCENARIO_2')
    print('5: s2_uss')
    results.setdefault('s2_uss', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': different_service_times,
        'scenario': 'uniform server selection', 
        'd_choices': 0, 
        'servers_speed': 'different'})
    
    print('6: s2_uss_d2')
    results.setdefault('s2_uss_d2', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': different_service_times,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': 2, 
        'servers_speed': 'different'})

    print('7: s2_uss_d3')
    results.setdefault('s2_uss_d3', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': different_service_times,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': 3, 
        'servers_speed': 'different'})

    print('8: s2_uss_d5')
    results.setdefault('s2_uss_d5', {})[arrival_rate] = run_experiment(
        {'num_servers': num_servers, 
        'num_customers': num_customers,
        'num_experiments': num_experiments,
        'interarrival_times': interarrival_times, 
        'service_times': different_service_times,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': 5, 
        'servers_speed': 'different'})    

save_experiments_to_files(results)