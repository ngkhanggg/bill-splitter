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
This function checks if interval1 is greater than interval2
"""
def _compare_intervals(interval1, interval2):
    if interval1[0] < interval2[0]:
        return -1
    elif interval1[0] > interval2[0]:
        return 1
    else:
        if interval1[1] < interval2[1]:
            return -1
        elif interval1[1] > interval2[1]:
            return 1
        else:
            return 0


"""
This function checks if interval1 is within interval2
"""
def is_within_interval(interval, player_interval):
    start, end = interval
    player_start, player_end = player_interval
    
    # start_is_within_interval = start <= player_start < end
    # end_is_within_interval = start < player_end =< end
    
    start_is_within_interval = (_compare_intervals(player_start, start) in (0, 1)) and (_compare_intervals(end, player_start) == 1)
    end_is_within_interval = (_compare_intervals(player_end, start) == 1) and (_compare_intervals(end, player_end) in (0, 1))
    
    return start_is_within_interval or end_is_within_interval


def calculate_elapsed_time(time1, time2):
    h1, m1 = time1
    h2,m2 = time2
    h3, m3 = (h2 - h1, m2 - m1) if m2 >= m1 else (h2 - h1 - 1, m2 + 60 - m1)
    return round((h3 * 60 + m3) / 60, 3)


def main(cost_per_hour, file_name):
    log = get_log(file_name)
    new_log = transform_log(log)
    
    sorted_start_times, sorted_end_times = sort_times(new_log)
    
    unique_start_times = get_unique_times(sorted_start_times, 0)
    unique_end_times = get_unique_times(sorted_end_times, 1)
    
    merged_list = merge(unique_start_times, unique_end_times)
    
    combinations = create_combinations(merged_list)
    
    list_players = {player: 0.0 for player in log}
    
    for combination in combinations:
        active_players = [player for player, interval in new_log.items() if is_within_interval(combination, interval) or is_within_interval(interval, combination)]

        if active_players:
            elapsed_time = calculate_elapsed_time(combination[0], combination[1])
            split_time = elapsed_time * cost_per_hour / len(active_players)

            for player in active_players:
                list_players[player] = int(list_players[player] + split_time)
    
    print(list_players)


if __name__ == '__main__':
    cost_per_hour = 108_000
    file_name = 'log.txt'
    
    main(cost_per_hour, file_name)

