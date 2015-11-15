import sys

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


