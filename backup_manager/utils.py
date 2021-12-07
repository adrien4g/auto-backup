import datetime

def get_root_paths(paths):
    split_paths = []
    for current_path in paths:
        split_paths.append(current_path.split('/')[1:])
    intersections = []
    if not len(split_paths) > 1:
        root_path = '/' + '/'.join(split_paths[0][:-1])
        intersections.append(root_path)
    else:
        for current_path in split_paths:
            for next_path in split_paths:
                if current_path == next_path: continue
                path = []
                for index in range(0, len(current_path)):
                    try:
                        if current_path[index] == next_path[index]:
                            path.append(current_path[index])
                        elif index == 0:
                            for i in current_path[:-1]:
                                path.append(i)
                    except:
                        continue
                path = '/' + '/'.join(path)
                if not path in intersections:
                    intersections.append(path)

    intersections_copy = intersections.copy()
    for current_path in intersections:
        for next_path in intersections:
            if current_path == next_path: continue
            if current_path in next_path:
                if next_path in intersections_copy:
                    intersections_copy.remove(next_path)
    intersections = intersections_copy
    return intersections

def write_log(data):
    if data == True:
        with open('../dacleara.log', 'a') as logfile:
            logfile.write('\n')
        return
    time = datetime.datetime.now()
    date = datetime.date.today()
    current_time = f'{time.hour}:{time.minute}:{time.second}'
    current_date = f'{date.year}/{date.month}/{date.day}'
    with open('../data.log', 'a') as logfile:
        logfile.write(f'{current_date} {current_time} {data}\n')
        