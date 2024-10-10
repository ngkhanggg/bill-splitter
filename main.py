import time


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1_000
        print(f"The function {func.__name__} took {execution_time_ms:.6f} ms to execute.")
        
        return result
    return wrapper


def get_log(filename):
    log = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '':
                continue
            player_name, start_time, end_time = line.split(',')
            log.update({player_name: (start_time, end_time)})
    return log


def transform_log(log):
    new_log = {}
    for k, v in log.items():
        start_time_h, start_time_m = map(int, v[0].split(':'))
        end_time_h, end_time_m = map(int, v[1].split(':'))
        end_time_h += (24 if end_time_h < start_time_h else 0)
        new_log.update({k: [(start_time_h, start_time_m), (end_time_h, end_time_m)]})
    return new_log


def sort_times(log):
    sorted_start_times = dict(sorted(log.items(), key=lambda x: x[1][0]))
    sorted_end_times = dict(sorted(log.items(), key=lambda x: x[1][1]))
    return sorted_start_times, sorted_end_times


def get_unique_times(times, index):
    unique_times = []
    for v in times.values():
        if v[index] not in unique_times:
            unique_times.append(v[index])
    return unique_times


def main(cost_per_hour, file_name):
    log = get_log(file_name)
    new_log = transform_log(log)
    
    sorted_start_times, sorted_end_times = sort_times(new_log)
    print(f"sorted_start_times\n{sorted_start_times}")
    print(f"sorted_end_times\n{sorted_end_times}")
    
    unique_start_times, unique_end_times = get_unique_times(sorted_start_times, 0), get_unique_times(sorted_end_times, 1)
    print(f"unique_start_times\n{unique_start_times}")
    print(f"unique_end_times\n{unique_end_times}")


if __name__ == '__main__':
    cost_per_hour = 108_000
    file_name = 'log.txt'
    
    main(cost_per_hour, file_name)

