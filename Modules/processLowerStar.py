import createLowerStarList as ls
import datetime
import numpy as np


def split_to_vertices(cell):
    count = cell.count('.')
    x = []
    if count == 1:
        x.append(cell)
    elif count == 2:
        x = [cell[:19], cell[19:]]
    elif count == 4:
        x = [cell[:19], cell[19:38], cell[38:57], cell[57:]]
    else:
        print(count)
        print(cell)
        raise Exception('number of dot can not be other')
    return x


def is_face(face, coface):
    count1 = face.count('.')
    count2 = coface.count('.')
    if count1 == 2 and count2 == 4:
        x = split_to_vertices(face)
        for item in x:
            if coface.find(item) == -1:
                return False
    elif count1 == 1 and count2 == 2:
        if coface.find(face) == -1:
            return False
    else:
        return False
    return True


def num_unpaired(cell, critical_vector_field, lower_star):
    count = cell.count('.')
    counter = 0
    x = []
    pair = ''
    if count == 4:
        x = lower_star['one']
    elif count == 2:
        y = cell[19:]
        if y.find('.') == 3:
            return 1, y
        else:
            raise Exception("Error")

    else:
        raise Exception("number of dot must be 4 or 2")

    for item in x:
        if is_face(item, cell):
            if item not in critical_vector_field:
                counter += 1
                pair += item
    if counter == 2:
        raise Exception('counter can not be 2. Either 0 or 1')
    return counter, pair


def process_lower_star(img):
    beginTime = datetime.datetime.now()
    print(beginTime)
    # sort the unique values of image in descending order to be the filtration value
    rows, columns = img.shape
    img = np.ndarray.tolist(img)
    print(rows)
    print(columns)

    # define the variables needed for the algorithm
    PQOne = []
    PQZero = []
    indexI = 0
    indexJ = 0
    critical_cells = []
    discrete_vector_field = {}

    # define the morse complex inductivly to equal the image at the end
    c =0

    for row in range(rows):
        for column in range(columns):
            # find the index of filteration value in image of string value
            # the index is saved in 2d array (array contains 2 arraies)
            c+=1
            print(c)

            try:
                lower_star = ls.create_lower_star_list(img, row, column, rows, columns)
                filtration_value = lower_star['zero'][0]
                if len(lower_star['zero']) == 1 and len(lower_star['one']) == 0 and len(lower_star['two']) == 0:
                    # the 0-cell can not paired with others cells so it is critical
                    critical_cells.append(filtration_value)

                else:

                    beta = lower_star['one'] + lower_star['two'] + lower_star['zero']
                    delta = min(lower_star['one'])
                    discrete_vector_field[filtration_value] = delta
                    list_critical_vector_field = [filtration_value, delta]
                    PQZero = lower_star['one']
                    PQZero.remove(delta)
                    for item in lower_star['two']:
                        if is_face(delta, item):
                            if num_unpaired(item, list_critical_vector_field, lower_star)[0] == 1:
                                PQOne.append(item)
                    while len(PQOne) != 0 or len(PQZero) != 0:
                        while len(PQOne) != 0:
                            PQOne.sort()
                            alpha = PQOne.pop(0)
                            num_unpaired_cells, pair_alpha = num_unpaired(alpha, list_critical_vector_field,
                                                                          lower_star, )
                            if num_unpaired_cells == 0:
                                PQZero.append(alpha)
                            else:
                                discrete_vector_field[pair_alpha] = alpha
                                PQZero.remove(pair_alpha)

                                for item in beta:
                                    if is_face(alpha, item) or is_face(pair_alpha, item):
                                        if num_unpaired(item, list_critical_vector_field, lower_star)[0] == 1:
                                            PQOne.append(item)
                        while len(PQZero) != 0:
                            PQZero.sort()
                            gamma = PQZero.pop(0)
                            critical_cells.append(gamma)
                            list_critical_vector_field.append(gamma)
                            for item in beta:
                                if item != gamma:
                                    if is_face(gamma, item):
                                        if num_unpaired(item, list_critical_vector_field, lower_star) == 1:
                                            PQOne.append(item)
            except:
                print("i: ,j: ".format(row,column))
    print(beginTime)
    print(datetime.datetime.now())
    print('critical cells: {}'.format(len(critical_cells)))
    print("discrete vector field: {}".format(len(discrete_vector_field)))
    return critical_cells, discrete_vector_field
