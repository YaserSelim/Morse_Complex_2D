def create_morse_function(im, i, j, rows, columns):
    if isinstance(im[i][j],str):
        return im[i][j]
    rows = rows -1 # to not get an error when we want to get i,j from the value
    if (.5 * ((i + j * rows) / (2 * rows * columns))) > .99:
        raise Exception("create morse function : the value can not be more than 1")
    perturbed_value = str(format(im[i][j] + (.5 * ((i + j * rows) / (2 * rows * columns))), ".15f"))
    place_of_dot = perturbed_value.find('.')
    if place_of_dot == 1:
        return '00' + perturbed_value
    elif place_of_dot == 2:
        return '0' + perturbed_value
    else:
        return perturbed_value


def create_lower_star_list(pic, i, j, rows, columns):
    lower_star = {'zero': [], "one": [], 'two': []}
    value = create_morse_function(pic, i, j, rows, columns)
    lower_star['zero'].append(value)
    if i != 0:
        val1 = create_morse_function(pic, i - 1, j, rows, columns)
        if value > val1:
            lower_star['one'].append(value + val1)
            if j < columns - 1:
                val2 = create_morse_function(pic, i, j + 1, rows, columns)
                if value > val2:
                    val3 = create_morse_function(pic, i - 1, j, rows, columns)
                    if value > val3:
                        s = [value, val1, val2, val3]
                        s.sort(reverse=True)
                        val = ''.join(s)
                        lower_star['two'].append(val)
            if j != 0:
                val2 = create_morse_function(pic, i, j - 1, rows, columns)
                if value > val2:
                    val3 = create_morse_function(pic, i - 1, j - 1, rows, columns)
                    if value > val3:
                        s = [value, val1, val2, val3]
                        s.sort(reverse=True)
                        val = ''.join(s)
                        lower_star['two'].append(val)
    if i != rows - 1:
        val1 = create_morse_function(pic, i + 1, j, rows, columns)
        if value > val1:
            lower_star["one"].append(value + val1)
            if j < columns - 1:
                val2 = create_morse_function(pic, i, j + 1, rows, columns)
                if value > val2:
                    val3 = create_morse_function(pic, i + 1, j + 1, rows, columns)
                    if value > val3:
                        s = [value, val1, val2, val3]
                        s.sort(reverse=True)
                        val = ''.join(s)
                        lower_star['two'].append(val)
            if j != 0:
                val2 = create_morse_function(pic, i, j - 1, rows, columns)
                if value > val2:
                    val3 = create_morse_function(pic, i + 1, j - 1, rows, columns)
                    if value > val3:
                        s = [value, val1, val2, val3]
                        s.sort(reverse=True)
                        val = ''.join(s)
                        lower_star['two'].append(val)
    if j != 0:
        val1 = create_morse_function(pic, i, j - 1, rows, columns)
        if value > val1:
            val = value + val1
            lower_star['one'].append(val)

    if j != columns - 1:
        val1 = create_morse_function(pic, i, j + 1, rows, columns)
        if value > val1:
            val = value + val1
            lower_star['one'].append(val)
    return lower_star


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
