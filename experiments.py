from simulation import Simulation
import os
import json
import random


def save_experiment_to_file(data, filename):
    folder_path = f'./experiments/{service_rate}_{num_customers}_{max_num_servers}'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def save_experiments_to_files(data):
    folder_path = f'./experiments/{service_rate}_{num_customers}_{max_num_servers}'
    os.makedirs(folder_path, exist_ok=True)
    for key, value in data.items():
        filename = f"{key}.json"
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as file:
            json.dump(value, file)

def run_experiment(params):
    data = {}
    
    for arrival_rate in [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999]:
        print(arrival_rate)
        data[arrival_rate] = {'avg_time_spent': [], 'max_time_spent': [], 'server_utilization': [], 'avg_queue_size': [], 'num_servers': []}
        for num_servers in range(1, params['max_num_servers'] + 1):
            simulation = Simulation(arrival_rate, params['service_rate'], num_servers, params['num_customers'], params['servers_speed'])
            avg_time_spent, max_time_spent, server_utilization, avg_queue_size = simulation.run(params['scenario'], params['d_choices'])
            data[arrival_rate]['avg_time_spent'].append(avg_time_spent)
            data[arrival_rate]['max_time_spent'].append(max_time_spent)
            data[arrival_rate]['server_utilization'].append(server_utilization)
            data[arrival_rate]['avg_queue_size'].append(avg_queue_size)
            data[arrival_rate]['num_servers'].append(num_servers)    
    print()
    return data


results = {}
s1_uss, s1_uss_d2, s1_uss_d3, s1_uss_d5 = {}, {}, {}, {}
s2_uss, s2_uss_d2, s2_uss_d3, s2_uss_d5, s2_nuss_d2, s2_nuss_d3, s2_nuss_d5 = {}, {}, {}, {}, {}, {}, {}

service_rate = 1.0
num_customers = 10000
max_num_servers = 1000

print('-------------------------- SCENARIO_1 --------------------------')
print('1: s1_uss')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'same',
    'scenario': 'uniform server selection', 
    'd_choices': 0,
    'max_num_servers': max_num_servers,
    }), 's1_uss')
    
print('2: s1_uss_d2')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'same',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 2,
    'max_num_servers': max_num_servers,
    }), 's1_uss_d2')

print('3: s1_uss_d3')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'same',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 3,
    'max_num_servers': max_num_servers,
    }), 's1_uss_d3')

print('4: s1_uss_d5')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'same',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 5,
    'max_num_servers': max_num_servers,
    }), 's1_uss_d5')

print('-------------------------- SCENARIO_2 --------------------------')
print('5: s2_uss_different_1')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_1',
    'scenario': 'uniform server selection', 
    'd_choices': 0,
    'max_num_servers': max_num_servers,
    }), 's2_uss_different_1')
print('6: s2_uss_different_2')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_2',
    'scenario': 'uniform server selection', 
    'd_choices': 0, 
    'max_num_servers': max_num_servers,
    }), 's2_uss_different_2')
print('7: s2_uss_different_3')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_3',
    'scenario': 'uniform server selection', 
    'd_choices': 0, 
    'max_num_servers': max_num_servers,
    }), 's2_uss_different_3')

print('8: s2_uss_d2_different_1')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_1',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 2, 
    'max_num_servers': max_num_servers,
    }), 's2_uss_d2_different_1')
print('9: s2_uss_d2_different_2')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_2',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 2,
    'max_num_servers': max_num_servers,
    }), 's2_uss_d2_different_2')
print('10: s2_uss_d2_different_3')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_3',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 2, 
    'max_num_servers': max_num_servers,
    }), 's2_uss_d2_different_3')

print('11: s2_uss_d3_different_1')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_1',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 3, 
    'max_num_servers': max_num_servers,
    }), 's2_uss_d3_different_1')
print('12: s2_uss_d3_different_2')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_2',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 3, 
    'max_num_servers': max_num_servers,
    }), 's2_uss_d3_different_2')
print('13: s2_uss_d3_different_3')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_3',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 3,
    'max_num_servers': max_num_servers,
    }), 's2_uss_d3_different_3') 

print('14: s2_uss_d5_different_1')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_1',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 5,
    'max_num_servers': max_num_servers,
    }), 's2_uss_d5_different_1')
print('15: s2_uss_d5_different_2')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_2',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 5,
    'max_num_servers': max_num_servers,
    }), 's2_uss_d5_different_2')
print('16: s2_uss_d5_different_3')
save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': 'different_3',
    'scenario': 'uniform server selection with power of d-choices', 
    'd_choices': 5,
    'max_num_servers': max_num_servers,
    }), 's2_uss_d5_different_3')