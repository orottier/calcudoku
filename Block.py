import operator

def minus(values):
    return 2*max(values) - sum(values)

def times(values):
    return reduce(operator.mul, values, 1)

def divide(values):
    m = max(values)
    return reduce(operator.div, [v for v in values if v != m], m)


class Block:
    def __init__(self, operation, result):
        ops = {
                "x": times,
                ":": divide,
                "+": sum, #builtin
                "-": minus
        }

        self.op = ops[operation]
        self.operation = operation
        self.result = result
        self.locations = []
        self.printedYet = False

    def addLocation(self, x, y):
        self.locations.append((x-1, y-1))

    def check(self, matrix):
        # only associative ops now
        values = []
        for (x,y) in self.locations:
            values.append(matrix[x][y])

        return self.op(values) == self.result
