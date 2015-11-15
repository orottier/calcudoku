import sys
import os
import subprocess
import numpy
import cv2

""" based on https://github.com/KoffeinFlummi/SudokuSolver """
debug = True

def showImage(img, name):
    if debug:
        cv2.namedWindow(name)
        cv2.imshow(name, img)
        cv2.waitKey()

def cutOut(img):
    # Grayscale image for easier processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 200)

    showImage(canny, "edge")

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
    showImage(imgcontours, "squares")

    # Arrange the border points of the contour we found so that they match pointsNew.
    pointsOriginal = sorted(squares[0], key=lambda x: x[0])
    pointsOriginal[0:2] = sorted(pointsOriginal[0:2], key=lambda x: x[1])
    pointsOriginal[2:4] = sorted(pointsOriginal[2:4], key=lambda x: x[1])
    pointsOriginal = numpy.float32(pointsOriginal)
    pointsNew = numpy.float32([[0,0],[0,450],[450,0],[450,450]])

    # Warp the image to be a square.
    persTrans = cv2.getPerspectiveTransform(pointsOriginal, pointsNew)
    fixedImage = cv2.warpPerspective(img, persTrans, (450,450))

    showImage(fixedImage, "perspectivefix")

    return fixedImage

def extractSudoku(img, size):
    """ Extracts the actual numbers from the image using tesseract. """
    sudoku = []
    right = []
    below = []

    border = 5 # how much to cut off the edges to eliminate any of the lines between the cells
    piece = 450 / size
    for i in range(size):
        sudoku_temp = []
        right_temp = []
        below_temp = []
        for j in range(size):
            value = findNumber(img, i, j, piece, border)
            sudoku_temp.append(value.strip())

            edge = findEdge(img, i, j, piece, border, "right")
            right_temp.append(edge)
            edge = findEdge(img, i, j, piece, border, "below")
            below_temp.append(edge)

        sudoku.append(sudoku_temp)
        right.append(right_temp)
        below.append(below_temp)

    return (sudoku, right, below)

def findEdge(img, i, j, piece, border, direction):
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

def findNumber(img, i, j, piece, border):
    subimg = img[i*piece+border:(i+1)*piece-border, j*piece+border:(j+1)*piece-border]
    subimg = cv2.cvtColor(subimg, cv2.COLOR_BGR2RGB)
    ret,thresh = cv2.threshold(subimg,127,255,cv2.THRESH_BINARY) # black-and-white for most contrast

    tesinput = "temp.jpg"
    tesoutput = "temp.txt"
    cv2.imwrite(tesinput, thresh)

    try:
        subprocess.check_output("tesseract "+tesinput+" "+tesoutput[:-4]+" -psm 8", shell=True)
        digit = (open(tesoutput, "r").read())
    except:
        pass
    print digit

    os.remove(tesinput)
    os.remove(tesoutput)

    sys.stdout.write("\r"+"Extracting data ... "+str(int((i*9+j+1)/81*100)).rjust(3)+"%")
    sys.stdout.flush()
    return digit


if len(sys.argv) < 3:
    print "Please supply a path to an image file and a size as arguments."
    sys.exit(1)

try:
    img = cv2.imread(sys.argv[1], 1)
    assert(img != None)
except:
    print "Could not open image. Please make sure that the file you specified exists and is a valid image file."
    sys.exit(1)

# size max 800
if img.shape[0] > img.shape[1]:
    sizecoef = 800. / img.shape[0]
else:
    sizecoef = 800. / img.shape[1]
if sizecoef < 1:
    img = cv2.resize(img, (0,0), fx=sizecoef, fy=sizecoef)

showImage(img, "image")

img = cutOut(img)

(sudoku, right, below) = extractSudoku(img, int(sys.argv[2]))
print sudoku
print right
print below

