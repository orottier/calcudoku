# CalcuDoku
Python solver for calcudokus

![showcase](https://github.com/orottier/calcudoku/raw/master/showcase.gif "How it works")

## Requirements
Python:
 - [cv2](http://opencv.org/)
 - [numpy](http://www.numpy.org/)

[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Usage:
`python main.py path/to/image.jpg size`

Size is an integer denoting the width/height of the square calcudoku.

## Todo
 - Automatic size detection
 - Train Tesseract for better number/operator detection
