from CalcuDoku import CalcuDoku
from Block import Block

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
