import sys
from MatrixGenerator import MatrixGenerator
from Block import Block
from ImageReader import ImageReader

path = sys.argv[1]
size = int(sys.argv[2])

m = MatrixGenerator(size)
reader = ImageReader(False, path, size)
calcuDoku = reader.getCalcuDoku()

print "Need to solve:"
calcuDoku.printMatrix()

print "Solving..."
for matrix in m.possibleMatrices():
    if calcuDoku.check(matrix):
        print "Solution:"
        calcuDoku.printMatrix(matrix)
        reader.writeSolution(matrix)
        break
