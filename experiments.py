from simulation import Simulation
import os
import json
import numpy as np

def save_experiment_to_file(data, filename, path):
    folder_path = f'./experiments/{service_rate}_{num_customers}_{max_num_servers}_{num_experiments}/{path}'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def save_experiments_to_files(data, path):
    folder_path = f'./experiments/{service_rate}_{num_customers}_{max_num_servers}_{num_experiments}/{path}'
    os.makedirs(folder_path, exist_ok=True)
    for key, value in data.items():
        filename = f"{key}.json"
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as file:
            json.dump(value, file)

def run_plot_experiment(params):
    data = {}
    for arrival_rate in [0.5, 0.8, 0.999]:
        data[arrival_rate] = {'avg_time_spent': [], 'max_time_spent': [], 'server_utilization': {}, 'avg_queue_size': [], 'num_servers': []}
        for num_servers in range(5, params['max_num_servers'] + 1):
            avg_times, max_times, avg_queue_sizes, servers_utilizations = [], [], [], []
            for experiment in range(params['num_experiments']):
                print(f"{params['filename']}, arrival_rate: {arrival_rate}, num_servers: {num_servers}, experiment: {experiment}")
                simulation = Simulation(arrival_rate, params['service_rate'], num_servers, params['num_customers'], params['servers_speed'])
                avg_time_spent, max_time_spent, server_utilization, avg_queue_size = simulation.run(params['scenario'], params['d_choices'])
                servers_utilizations.append(server_utilization)
                avg_times.append(avg_time_spent)
                max_times.append(max_time_spent)
                avg_queue_sizes.append(avg_queue_size)
            data[arrival_rate]['avg_time_spent'].append(np.mean(avg_times))
            data[arrival_rate]['max_time_spent'].append(np.mean(max_times))
            
            data[arrival_rate]['server_utilization'][num_servers] = [
                 np.mean([servers_utilizations[row][column] for row in range(params['num_experiments'])])
                 for column in range(num_servers)
            ]
            data[arrival_rate]['avg_queue_size'].append(np.mean(avg_queue_sizes))
            data[arrival_rate]['num_servers'].append(num_servers)    
    return data

def run_experiment(params):
    data = {}
    for arrival_rate in [0.5, 0.8, 0.999]:
        data[arrival_rate] = {'avg_time_spent': [], 'max_time_spent': [], 'server_utilization': [], 'avg_queue_size': [], 'num_servers': []}
        servers_utilizations = []
        for experiment in range(params['num_experiments']):
            print(f"{params['filename']}, arrival_rate: {arrival_rate}, num_servers: {params['max_num_servers']}, experiment: {experiment}")
            simulation = Simulation(arrival_rate, params['service_rate'], params['max_num_servers'], params['num_customers'], params['servers_speed'])
            avg_time_spent, max_time_spent, server_utilization, avg_queue_size = simulation.run(params['scenario'], params['d_choices'])
            servers_utilizations.append(server_utilization)
            data[arrival_rate]['avg_time_spent'].append(np.mean(avg_time_spent))
            data[arrival_rate]['max_time_spent'].append(np.mean(max_time_spent))
            data[arrival_rate]['avg_queue_size'].append(np.mean(avg_queue_size)) 
        data[arrival_rate]['server_utilization'] = [
                np.mean([servers_utilizations[row][column] for row in range(params['num_experiments'])])
                for column in range(params['max_num_servers'])
            ]
    return data


results = {}
s1_uss, s1_uss_d2, s1_uss_d3, s1_uss_d5 = {}, {}, {}, {}
s2_uss, s2_uss_d2, s2_uss_d3, s2_uss_d5, s2_nuss_d2, s2_nuss_d3, s2_nuss_d5 = {}, {}, {}, {}, {}, {}, {}

service_rate = 1.0
num_customers = 10000
max_num_servers = 100
num_experiments = 10


# ---------------------------------------------------------------------------------------------- #
# -------------------------------------------- PLOTS ------------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

# print('-------------------------- S1_USS & S2_USS_different_1_2_3 --------------------------')

servers_speeds = ['same', 'different_1', 'different_2', 'different_3']
scenarios = ['s1_uss', 's2_uss_different_1', 's2_uss_different_2', 's2_uss_different_3']
for server_speed, scenario in zip(servers_speeds, scenarios):
    save_experiment_to_file(run_plot_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': server_speed,
    'scenario': 'uniform server selection', 
    'd_choices': 0, 
    'max_num_servers': max_num_servers,
    'num_experiments': num_experiments, 
    'filename': scenario,
    }), scenario, 'plot')


# print('--------------------------------- S1_USS_d_2_3_5 ------------------------------------')

scenarios = ['s1_uss_d2', 's1_uss_d3', 's1_uss_d5']
d_choices = [2, 3, 5]
for scenario, d in zip(scenarios, d_choices):
        print(scenario)
        save_experiment_to_file(run_plot_experiment(
        {'service_rate': service_rate,
        'num_customers': num_customers,
        'servers_speed': 'same',
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': d,
        'max_num_servers': max_num_servers,
        'num_experiments': num_experiments,
        'filename': scenario,
        }), scenario, 'plot')


print('--------------------------- S2_USS_d_2_3_5_different_1_2_3 --------------------------')

servers_speeds = ['different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3']
scenarios = ['s2_uss_d2_different_1', 's2_uss_d2_different_2', 's2_uss_d2_different_3',
             's2_uss_d3_different_1', 's2_uss_d3_different_2', 's2_uss_d3_different_3',
             's2_uss_d5_different_1', 's2_uss_d5_different_2', 's2_uss_d5_different_3']
d_choices = [2, 2, 2, 3, 3, 3, 5, 5, 5]

for server_speed, scenario, d in zip(servers_speeds, scenarios, d_choices):
        print(scenario)
        save_experiment_to_file(run_plot_experiment(
        {'service_rate': service_rate,
        'num_customers': num_customers,
        'servers_speed': server_speed,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': d,
        'max_num_servers': max_num_servers,
        'num_experiments': num_experiments,
        'filename': scenario,
        }), scenario, 'plot')


# ---------------------------------------------------------------------------------------------- #
# -------------------------------------------- TABLES ------------------------------------------ #
# ---------------------------------------------------------------------------------------------- #

print('-------------------------- S1_USS & S2_USS_different_1_2_3 --------------------------')

servers_speeds = ['same', 'different_1', 'different_2', 'different_3']
scenarios = ['s1_uss', 's2_uss_different_1', 's2_uss_different_2', 's2_uss_different_3']
for server_speed, scenario in zip(servers_speeds, scenarios):
    save_experiment_to_file(run_experiment(
    {'service_rate': service_rate,
    'num_customers': num_customers,
    'servers_speed': server_speed,
    'scenario': 'uniform server selection', 
    'd_choices': 0, 
    'max_num_servers': max_num_servers,
    'num_experiments': num_experiments, 
    'filename': scenario,
    }), scenario, 'table')


print('--------------------------------- S1_USS_d_2_3_5 ------------------------------------')

scenarios = ['s1_uss_d2', 's1_uss_d3', 's1_uss_d5']
d_choices = [2, 3, 5]

for scenario, d in zip(scenarios, d_choices):
        print(scenario)
        save_experiment_to_file(run_experiment(
        {'service_rate': service_rate,
        'num_customers': num_customers,
        'servers_speed': 'same',
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': d,
        'max_num_servers': max_num_servers,
        'num_experiments': num_experiments,
        'filename': scenario,
        }), scenario, 'table')


print('--------------------------- S2_USS_d_2_3_5_different_1_2_3 --------------------------')

servers_speeds = ['different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3']
scenarios = ['s2_uss_d2_different_1', 's2_uss_d2_different_2', 's2_uss_d2_different_3',
             's2_uss_d3_different_1', 's2_uss_d3_different_2', 's2_uss_d3_different_3',
             's2_uss_d5_different_1', 's2_uss_d5_different_2', 's2_uss_d5_different_3']
d_choices = [2, 2, 2, 3, 3, 3, 5, 5, 5]

for server_speed, scenario, d in zip(servers_speeds, scenarios, d_choices):
        print(scenario)
        save_experiment_to_file(run_experiment(
        {'service_rate': service_rate,
        'num_customers': num_customers,
        'servers_speed': server_speed,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': d,
        'max_num_servers': max_num_servers,
        'num_experiments': num_experiments,
        'filename': scenario,
        }), scenario, 'table')