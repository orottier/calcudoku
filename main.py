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
    def __init__(self, op, result):
        if(op == "*"):
                self.op = times
        if(op == "-"):
                self.op = minus
        if(op == "+"):
                self.op = plus

        self.result = result
        self.locations = []

    def addLocation(self, tuple):
        self.locations.append(tuple)

    def check(self, matrix):
        # only associative ops now
        values = []
        for (x,y) in self.locations:
            values.append(matrix[x][y])

        return self.op(values) == self.result

def blockGenerator(rows = []):
    return [
            [[1,2,3,4],[3,3,4,1],[3,4,1,2],[4,1,2,3]]
           ]

# main:
blocks = []

b = Block("*", 6)
b.addLocation((0,0))
b.addLocation((0,1))
b.addLocation((1,0))
blocks.append(b)

for test in blockGenerator():
    skip = False
    for b in blocks:
        if not b.check(test):
            skip = true
            break
    if not skip:
        print test
