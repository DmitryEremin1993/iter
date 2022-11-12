from itertools import chain


class FlatIterator:


    def __init__(self, nested_list: list):
        self.nested_list = nested_list

    def __iter__(self):
        self.cursor = 0
        self.inner_cursor = -1
        return self

    def __next__(self):
        self.inner_cursor += 1
        if self.inner_cursor >= len(self.nested_list[self.cursor]):
            self.cursor += 1
            self.inner_cursor = 0
        if self.cursor >= len(self.nested_list):
            raise StopIteration
        return self.nested_list[self.cursor][self.inner_cursor]


def flat_generator(nested_list: list):

    outer_index = 0
    inner_index = 0
    while True:
        yield nested_list[outer_index][inner_index]
        inner_index += 1
        if inner_index >= len(nested_list[outer_index]):
            outer_index += 1
            inner_index = 0
        if outer_index >= len(nested_list):
            break


def flatter(nested_list: list) -> list:

    present = False
    for element in nested_list:
        if isinstance(element, list):
            present = True
            break
    if not present:
        return nested_list
    else:
        new_list = list(chain.from_iterable(nested_list))
        return flatter(new_list)


class SuperFlatIterator:

    def __init__(self, nested_list: list):

        self.nested_list = nested_list
        self.flatted_list = flatter(nested_list)

    def __iter__(self):

        self.cursor = 0
        return self

    def __next__(self):

        if self.cursor >= len(self.flatted_list):
            raise StopIteration
        self.cursor += 1
        return self.flatted_list[self.cursor - 1]


def super_flat_generator(very_nested_list: list):

    for inner in very_nested_list:
        if isinstance(inner, list):
            yield from super_flat_generator(inner)
        else:
            yield inner


if __name__ == '__main__':

    print('\nЗадание 1, итератор списка списков\n')

    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]

    for item in FlatIterator(nested_list):
        print(item)

    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)

    print('\nЗадание 2, генератор списка списков\n')

    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f'],
        [1, 2, None]
    ]

    for item in flat_generator(nested_list):
        print(item)

    super_nested_list = [
                         'a', ['b', 'c'],
                         ['d', [['e']], 'f', ['g', ['h', ['i']]]],
                         [['j'], 'k'], 'l',
                         ['m', ['n', ['o', ['p'], 'q'], 'r'], 's'],
                         [['t', 'u'], [['v'], 'w']],
                         ['x', [['y']]],
                         [[['z']]]
                         ]

    print('\nЗадание 3, итератор списка с любым уровнем вложенности\n')

    for element in SuperFlatIterator(super_nested_list):
        print(element)

    print('\nЗадание 4, генератор списка с любым уровнем вложенности\n')

    for element in super_flat_generator(super_nested_list):
        print(element)