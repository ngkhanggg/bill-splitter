def get_log(filename):
    log = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '':
                continue
            player_name, start_time, end_time = line.split(',')
            log[player_name] = (start_time, end_time)
    return log


def transform_log(log):
    new_log = {}
    for k, v in log.items():
        start_time_h, start_time_m = map(int, v[0].split(':'))
        end_time_h, end_time_m = map(int, v[1].split(':'))
        if end_time_h < start_time_h:
            end_time_h += 24  # Handle overnight cases
        new_log[k] = [(start_time_h, start_time_m), (end_time_h, end_time_m)]
    return new_log


def sort_times(log):
    sorted_start_times = dict(sorted(log.items(), key=lambda x: x[1][0]))  # Sort by start time
    sorted_end_times = dict(sorted(log.items(), key=lambda x: x[1][1]))  # Sort by end time
    return sorted_start_times, sorted_end_times


def get_unique_times(times, index):
    return sorted(set(v[index] for v in times.values()))


def merge(list1, list2):
    return sorted(set(list1 + list2), key=lambda x: (x[0], x[1]))


def create_combinations(times):
    return [[times[i], times[i + 1]] for i in range(len(times) - 1) if times[i] != times[i + 1]]


"""
@param interval1
@param interval2
This function checks if interval1 is within interval2
"""
def is_within_interval(interval, player_interval):
    start, end = interval
    player_start, player_end = player_interval
    
    start_is_within_interval = start <= player_start <= end
    end_is_within_interval = start <= player_end <= end
    
    return start_is_within_interval or end_is_within_interval


def calculate_elapsed_time(time1, time2):
    h1, m1 = time1
    h2,m2 = time2
    h3, m3 = (h2 - h1, m2 - m1) if m2 >= m1 else (h2 - h1 - 1, m2 + 60 - m1)
    return round((h3 * 60 + m3) / 60, 3)


def main(cost_per_hour, file_name):
    log = get_log(file_name)
    print(f"log\n{log}")
    
    new_log = transform_log(log)
    print(f"new_log\n{new_log}")
    
    list_players = {key: 0.0 for key in log.keys()}
    print(f"list_players\n{list_players}")
    
    sorted_start_times, sorted_end_times = sort_times(new_log)
    print(f"sorted_start_times\n{sorted_start_times}")
    print(f"sorted_end_times\n{sorted_end_times}")
    
    unique_start_times, unique_end_times = get_unique_times(sorted_start_times, 0), get_unique_times(sorted_end_times, 1)
    print(f"unique_start_times\n{unique_start_times}")
    print(f"unique_end_times\n{unique_end_times}")
    
    merged_list = merge(unique_start_times, unique_end_times)
    print(f"merged_list\n{merged_list}")
    
    combinations = create_combinations(merged_list)
    print(f"combinations\n{combinations}")
    
    divisions = []
    for combination in combinations:
        tmp = []
        for k, v in new_log.items():
            if is_within_interval(combination, v):
                tmp.append(k)
        divisions.append({'interval': combination, 'player(s)': tmp})
    print(f"divisions\n{divisions}")
    
    new_divisions = []
    for division in divisions:
        elapsed_time = calculate_elapsed_time(division['interval'][0], division['interval'][1])
        new_divisions.append({elapsed_time: division['player(s)']})
    print(f"new_divisions\n{new_divisions}")
    
    for player, fees in list_players.items():
        print(f"player {player} fees {fees}")
        for division in new_divisions:
            print(f"division {division}")
            for k, v in division.items():
                print(f"k {k} v {v}")
                if player in v:
                    list_players[player] += (k / len(v))
    print(list_players)
    
    for player, fees in list_players.items():
        list_players[player] = fees * cost_per_hour
    
    print(list_players)


if __name__ == '__main__':
    cost_per_hour = 108_000
    file_name = 'log.txt'
    
    main(cost_per_hour, file_name)

