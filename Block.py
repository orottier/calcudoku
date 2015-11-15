def minus(values):
    return 2*max(values) - sum(values)

def plus(values):
    return sum(values)

def times(values):
    total = 1
    for v in values:
        total = v*total
    return total

class Block:
    def __init__(self, operation, result):
        if(operation == "*"):
                self.op = times
        if(operation == "-"):
                self.op = minus
        if(operation == "+"):
                self.op = plus

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


