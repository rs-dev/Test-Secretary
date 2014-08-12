import itertools


class count(itertools.count):
    def __next__(self):
        return self.next()
