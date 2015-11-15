import sys

def minus(values):
    return 2*max(values) - sum(values)

def plus(values):
    return sum(values)

def times(values):
    total = 1
    for v in values:
        total = v*total
    return total

class CalcuDoku:
    def __init__(self, size):
        self.size = size
        self.blocks = []

    def addBlock(self, block):
        self.blocks.append(block)

    def printMatrix(self, matrix = None):
        print
        print '/' + '-'*(4*self.size-1) + '\\'
        for i in range(0, self.size):
            sys.stdout.write('|')
            for j in range(0, self.size):
                if matrix:
                    sys.stdout.write(' ')
                    sys.stdout.write(str(matrix[i][j]))
                    sys.stdout.write(' ')
                else:
                    b = self.findBlock(i,j)
                    if not b.printedYet:
                        sys.stdout.write((str(b.result) + b.operation).ljust(3))
                        b.printedYet = True
                    else:
                        sys.stdout.write('   ')
                if self.connected(i, j, 'right'):
                    sys.stdout.write(' ')
                else:
                    sys.stdout.write('|')
            sys.stdout.write("\n")
            if i+1 != self.size:
                sys.stdout.write('|')
                for j in range(0, self.size):
                    if self.connected(i, j, 'down'):
                        sys.stdout.write('   ')
                    else:
                        sys.stdout.write('---')
                    if j+1 != self.size:
                        sys.stdout.write('+')
                sys.stdout.write("|\n")
        print '\\' + '-'*(4*self.size-1) + '/'
        print

    def connected(self, i, j, direction):
        if direction == 'right':
            if j+1 == self.size:
                return False
            b = self.findBlock(i,j)
            if not b:
                return False
            return (i, j+1) in b.locations

        if direction == 'down':
            if i+1 == self.size:
                return False
            b = self.findBlock(i,j)
            if not b:
                return False
            return (i+1, j) in b.locations

    def findBlock(self, i, j):
        for b in self.blocks:
            for loc in b.locations:
                if loc == (i,j):
                    return b

    def check(self, matrix):
        success = True
        for b in self.blocks:
            if not b.check(matrix):
                success = False
                break
        return success


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

def blockGenerator(rows = []):
    return [
            [[1,2,3,4],[3,3,4,1],[3,4,1,2],[4,1,2,3]]
           ]

# main:
calcuDoku = CalcuDoku(4)

b = Block("*", 6)
b.addLocation(1,1)
b.addLocation(1,2)
b.addLocation(2,1)
calcuDoku.addBlock(b)

b = Block("*", 24)
b.addLocation(1,3)
b.addLocation(1,4)
b.addLocation(2,3)
calcuDoku.addBlock(b)

b = Block("+", 11)
b.addLocation(2,2)
b.addLocation(3,1)
b.addLocation(3,2)
b.addLocation(4,1)
calcuDoku.addBlock(b)

b = Block("*", 2)
b.addLocation(2,4)
b.addLocation(3,4)
calcuDoku.addBlock(b)

b = Block("+", 11)
b.addLocation(3,3)
b.addLocation(4,2)
b.addLocation(4,3)
b.addLocation(4,4)
calcuDoku.addBlock(b)

print "Need to solve:"
calcuDoku.printMatrix()

print "Solution:"
for matrix in blockGenerator():
    if calcuDoku.check(matrix):
        calcuDoku.printMatrix(matrix)
        break
