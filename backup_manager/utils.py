def get_main_paths(array):
    # Spli paths to array
    split_path = []
    for path in array:
        # Remove first element (is a blank string)
        split_path.append(path.split('/')[1:])
    # Get main paths
    intersection = set()
    if len(split_path) > 1:
        for path1 in split_path:
            for path2 in split_path:
                if path1 == path2: continue
                path = ''
                for index in range(0, len(path1)):
                    try:
                        # Verify if has intersection in path
                        if path1[index] == path2[index]:
                            path += f'{path1[index]}/'

                        # Add the root of path1
                        elif index == 0:
                            intersection.add('/' + '/'.join(path1[:-1]))
                            break

                        # Add intersection path
                        elif path != '':
                            intersection.add('/' + path[:-1])
                            break

                    except:
                        if path != '': intersection.add('/' + path[:-1])
                        break
    # If container have only 1 volume
    else:
        intersection.add('/' + '/'.join(split_path[0][:-1]))
    # Remove duplicate paths
    duplicate_intersection = intersection.copy()
    for path1 in intersection:
        for path2 in intersection:
            if path1 == path2: continue
            if path1 in path2:
                print(f'path1 = {path1} | path2 = {path2}')
                duplicate_intersection.remove(path2)
    return duplicate_intersection
