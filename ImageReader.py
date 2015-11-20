import sys
import os
import subprocess
import numpy
import cv2
from Block import Block
from CalcuDoku import CalcuDoku

class ImageReader:
    """ based on https://github.com/KoffeinFlummi/SudokuSolver """

    def __init__(self, debug, path, size):
        self.debug = debug
        self.size = size

        try:
            img = cv2.imread(path, 1)
            assert(img != None)
        except:
            print "Could not open image. Please make sure that the file you specified exists and is a valid image file.", path
            sys.exit(1)

        # size max 800
        if img.shape[0] > img.shape[1]:
            sizecoef = 800. / img.shape[0]
        else:
            sizecoef = 800. / img.shape[1]
        if sizecoef < 1:
            img = cv2.resize(img, (0,0), fx=sizecoef, fy=sizecoef)

        self.showImage(img, "image")
        self.img = img


    def showImage(self, img, name):
        if self.debug:
            cv2.namedWindow(name)
            cv2.imshow(name, img)
            cv2.waitKey()

    def cutOut(self, img):
        # Grayscale image for easier processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 50, 200)

        self.showImage(canny, "edge")

        # Detect contours
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours for things that might be squares
        squares = []
        for contour in contours:
            contour = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(contour) == 4 and cv2.isContourConvex(contour):
                squares.append(contour)

        # Find the biggest one.
        squares = [sorted(squares, key=lambda x: cv2.contourArea(x))[-1]]
        squares[0] = squares[0].reshape(-1, 2)

        imgcontours = img
        cv2.drawContours(imgcontours, squares, -1, (0,0,255))
        self.showImage(imgcontours, "squares")

        # Arrange the border points of the contour we found so that they match pointsNew.
        pointsOriginal = sorted(squares[0], key=lambda x: x[0])
        pointsOriginal[0:2] = sorted(pointsOriginal[0:2], key=lambda x: x[1])
        pointsOriginal[2:4] = sorted(pointsOriginal[2:4], key=lambda x: x[1])
        pointsOriginal = numpy.float32(pointsOriginal)
        pointsNew = numpy.float32([[0,0],[0,450],[450,0],[450,450]])

        # Warp the image to be a square.
        persTrans = cv2.getPerspectiveTransform(pointsOriginal, pointsNew)
        fixedImage = cv2.warpPerspective(img, persTrans, (450,450))

        self.showImage(fixedImage, "perspectivefix")

        return fixedImage

    def extractSudoku(self, img, size):
        """ Extracts the actual numbers from the image using tesseract. """
        self.sudoku = []
        self.right = []
        self.below = []

        border = 5 # how much to cut off the edges to eliminate any of the lines between the cells
        piece = 450 / size
        for i in range(size):
            sudoku_temp = []
            right_temp = []
            below_temp = []
            for j in range(size):
                value = self.findNumber(img, i, j, piece, border)
                sudoku_temp.append(value.strip())

                edge = self.findEdge(img, i, j, piece, border, "right")
                right_temp.append(edge)
                edge = self.findEdge(img, i, j, piece, border, "below")
                below_temp.append(edge)

            self.sudoku.append(sudoku_temp)
            self.right.append(right_temp)
            self.below.append(below_temp)

    def findEdge(self, img, i, j, piece, border, direction):
        if direction == "below":
            subimg = img[
                    max(0, (i+1)*piece-border):(i+1)*piece+border,
                    j*piece+border:(j+1)*piece-border
            ]
        else:
            subimg = img[
                    i*piece+border:(i+1)*piece-border,
                    max(0, (j+1)*piece-border):(j+1)*piece+border
            ]

        subimg = cv2.cvtColor(subimg, cv2.COLOR_BGR2RGB)
        ret,thresh = cv2.threshold(subimg,127,255,cv2.THRESH_BINARY) # black-and-white for most contrast
        (occur, bins) = numpy.histogram(thresh, 2)
        (black, white) = occur
        return black*3 > white

    def findNumber(self, img, i, j, piece, border):
        subimg = img[i*piece+border:(i+1)*piece-border, j*piece+border:(j+1)*piece-border]
        subimg = cv2.cvtColor(subimg, cv2.COLOR_BGR2RGB)
        ret,thresh = cv2.threshold(subimg,127,255,cv2.THRESH_BINARY) # black-and-white for most contrast

        cv2.imwrite("tesseract/input.png", thresh)

        try:
            subprocess.check_output("tesseract tesseract/input.png tesseract/output -psm 8 digits-chars", shell=True)
            digit = (open("tesseract/output.txt", "r").read())
        except:
            digit = ""
            pass

        print "digit", digit.strip()
        return digit

    def discover(self, i, j):
        print "checking ", i, j
        for (vertical, lateral) in [(0,1), (0,-1), (1,0), (-1,0)]:
            print "v", vertical, "l", lateral
            ii = i+vertical
            ilat = i + (vertical-1)/2
            jj = j+lateral
            jlat = j + (lateral-1)/2
            if ii in range(self.size) and jj in range(self.size):
                if not self.sectors[ii][jj]:
                    if lateral and not self.right[i][jlat] or vertical and not self.below[ilat][j]:
                        block = self.sectors[i][j]
                        print "connecting", ii, jj, block.operation, block.result
                        self.sectors[ii][jj] = block
                        block.addLocation(ii+1, jj+1)
                        self.calcuDoku.printMatrix()
                        self.discover(ii, jj)
                    else:
                        print "not connected"
                else:
                    print "already discovered"
            else:
                print "outside"

    def getCalcuDoku(self):

        img = self.cutOut(self.img)

        self.calcuDoku = CalcuDoku(self.size)
        self.extractSudoku(img, self.size)
        print self.sudoku
        print self.right
        print self.below

        self.sectors = [[None for i in range(self.size)] for j in range(self.size)]
        for i in range(0, self.size):
            for j in range(0, self.size):
                if not self.sectors[i][j]:
                    if self.sudoku[i][j]:
                        ops = self.sudoku[i][j]
                        b = Block(ops)
                        self.calcuDoku.addBlock(b)
                        b.addLocation(i+1, j+1)
                        self.sectors[i][j] = b
                        self.discover(i, j)
                    else:
                        print "huh"
                        sys.exit(1)

        return self.calcuDoku
