import numpy as np


def parse(file_path):
    file = open(file_path, 'r')
    data = file.read()
    coordinates, folds = data.split('\n\n')
    parsed_coordinates = [[int(xy) for xy in coordinate.split(',')] for coordinate in coordinates.split('\n')]
    parsed_folds = [[fold.split('=')[0][-1], int(fold.split('=')[1])] for fold in folds.split('\n')]
    return parsed_coordinates, parsed_folds


def init(coordinates):
    width = max(xy[0] for xy in coordinates)
    length = max(xy[1] for xy in coordinates)
    array = np.full((width + 1, length + 1), False)
    for x, y in coordinates:
        array[x, y] = True
    return array


def apply_transform(array, axis, index):
    print(f'folding on {axis}={index}')
    if axis == 'x':
        top_array = array[:index]
        bottom_array = np.flip(array[(index+1):], axis=0)
        return top_array | bottom_array
    elif axis == 'y':
        left_array = array[:, :index]
        right_array = np.flip(array[:, (index+1):], axis=1)
        return left_array | right_array
    else:
        print(axis)
        return None


def format_array(array):
    res: str = ''
    for y in range(array.shape[1]):
        for x in range(array.shape[0]):
            res += '#' if array[x, y] else '.'
        res += '\n'
    return res


def q1(path):
    coords, folds = parse(path)
    array = init(coords)
    array = apply_transform(array, *folds[0])
    return array.sum()


def q2(path):
    coords, folds = parse(path)
    array = init(coords)
    for fold in folds:
        array = apply_transform(array, *fold)
    return format_array(array)


if __name__ == '__main__':
    # test
    test_coords, test_folds = parse('resources/2021/13/test.txt')
    print(test_coords, test_folds)
    test_array = init(test_coords)
    print(format_array(test_array))
    for fold in test_folds:
        test_array = apply_transform(test_array, *fold)
        print(format_array(test_array))

    assert q1('resources/2021/13/test.txt') == 17
    print('answer for q1: ', q1('resources/2021/13/data.txt'))
    print('answer for q2:', q2('resources/2021/13/data.txt'), sep='\n')
