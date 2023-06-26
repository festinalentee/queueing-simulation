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

def run_experiment(params):
    data = {}
    for arrival_rate in [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999]:
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

def run_plot_experiment(params):
    data = {}
    for arrival_rate in [0.5, 0.8, 0.9, 0.99]:
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

def run_histogram_experiment(params):
    data = {}
    for arrival_rate in [0.999]:
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


service_rate = 1.0
num_customers = 100
max_num_servers = 20
num_experiments = 2


# ---------------------------------------------------------------------------------------------- #
# -------------------------------------------- TABLES ------------------------------------------ #
# ---------------------------------------------------------------------------------------------- #


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


scenarios = ['s1_uss_d1', 's1_uss_d2', 's1_uss_d3', 's1_uss_d5']
d_choices = [1, 2, 3, 5]
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


servers_speeds = ['different_1', 'different_2', 'different_3',
                  'different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3']
scenarios = ['s2_uss_d1_different_1', 's2_uss_d1_different_2', 's2_uss_d1_different_3',
             's2_uss_d2_different_1', 's2_uss_d2_different_2', 's2_uss_d2_different_3',
             's2_uss_d3_different_1', 's2_uss_d3_different_2', 's2_uss_d3_different_3',
             's2_uss_d5_different_1', 's2_uss_d5_different_2', 's2_uss_d5_different_3']
d_choices = [1, 1, 1, 2, 2, 2, 3, 3, 3, 5, 5, 5]
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


# ---------------------------------------------------------------------------------------------- #
# -------------------------------------------- PLOTS ------------------------------------------- #
# ---------------------------------------------------------------------------------------------- #


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


scenarios = ['s1_uss_d1', 's1_uss_d2', 's1_uss_d3', 's1_uss_d5']
d_choices = [1, 2, 3, 5]
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


servers_speeds = ['different_1', 'different_2', 'different_3',
                  'different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3', 
                  'different_1', 'different_2', 'different_3']
scenarios = ['s2_uss_d1_different_1', 's2_uss_d1_different_2', 's2_uss_d1_different_3',
             's2_uss_d2_different_1', 's2_uss_d2_different_2', 's2_uss_d2_different_3',
             's2_uss_d3_different_1', 's2_uss_d3_different_2', 's2_uss_d3_different_3',
             's2_uss_d5_different_1', 's2_uss_d5_different_2', 's2_uss_d5_different_3']
d_choices = [1, 1, 1, 2, 2, 2, 3, 3, 3, 5, 5, 5]
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
# ------------------------------------------ HISTOGRAMS ---------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

servers_speeds = ['different_1', 'different_1', 'different_2', 'different_2', 'different_3', 'different_3']
scenarios = ['s2_uss_d1_different_1', 's2_uss_d2_different_1', 
             's2_uss_d1_different_2', 's2_uss_d2_different_2', 
             's2_uss_d1_different_3', 's2_uss_d2_different_3']
d_choices = [1, 2, 1, 2, 1, 2]
for server_speed, scenario, d in zip(servers_speeds, scenarios, d_choices):
        print(scenario)
        save_experiment_to_file(run_histogram_experiment(
        {'service_rate': service_rate,
        'num_customers': num_customers,
        'servers_speed': server_speed,
        'scenario': 'uniform server selection with power of d-choices', 
        'd_choices': d,
        'max_num_servers': max_num_servers,
        'num_experiments': num_experiments,
        'filename': scenario,
        }), scenario, 'histogram')