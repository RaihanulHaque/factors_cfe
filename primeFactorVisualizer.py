import math
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

IMG_STORAGE = "./images"
IMG_PREFIX = "factors_of_"
COLOR_BLUE = (22, 132, 170)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_ELEPHANT = (15, 60, 76)
LINE_THICKNESS = 4
FONT_SIZE = 2
FONT_PIX_W = 42
FONT_PIX_H = int(FONT_PIX_W * 3)
FONT = cv2.FONT_HERSHEY_DUPLEX


class Box:
    # __x1 = 0
    # __y1 = 0
    # __x2 = 0
    # __y2 = 0
    # __textX = 0
    # __textY = 0

    def __init__(self, n: int, x1: int, y1: int):
        self.n = n
        self.text = f" {n} "
        self.width = len(self.text) * FONT_PIX_W
        self.x1 = x1    # Top left x
        self.y1 = y1    # Top  left y
        self.x2 = self.x1+self.width    # bottom right x
        self.y2 = self.y1 + int(FONT_PIX_H)  # bottom right y
        self.textX = self.x1
        self.textY = self.y2 - int(FONT_PIX_H/3)

    def draw(self, img):
        cv2.rectangle(img, pt1=(self.x1, self.y1), pt2=(
            self.x2, self.y2), color=COLOR_BLUE, thickness=-1)
        cv2.rectangle(img, pt1=(self.x1, self.y1), pt2=(
            self.x2, self.y2), color=COLOR_BLACK, thickness=2)
        cv2.putText(img, text=self.text,
                    org=(self.textX, self.textY),
                    fontFace=FONT, fontScale=FONT_SIZE,
                    color=COLOR_WHITE, thickness=2)

    def draw_backgroundless(self, img):
        cv2.putText(img, text=self.text,
                    org=(self.textX, self.textY),
                    fontFace=FONT, fontScale=FONT_SIZE,
                    color=COLOR_BLUE, thickness=2)

    @staticmethod
    def checkWidth(n):
        text = f" {n} "
        width = len(text) * FONT_PIX_W
        return width

    @staticmethod
    def drawArrow(arrowTip: tuple, order, img):
        # Arrow Tip
        cv2.line(img, pt1=arrowTip, pt2=(
            arrowTip[0]+10, arrowTip[1] - 20), color=COLOR_BLACK, thickness=LINE_THICKNESS)
        cv2.line(img, pt1=arrowTip, pt2=(
            arrowTip[0]-10, arrowTip[1] - 20), color=COLOR_BLACK, thickness=LINE_THICKNESS)

        # Arrow Connector
        arrowBase = (arrowTip[0], arrowTip[1] - 35 * order)
        cv2.line(img, pt1=arrowTip, pt2=arrowBase,
                 color=COLOR_BLACK, thickness=LINE_THICKNESS)

        return arrowBase

    def joinCompanions(self, img):
        arrowTip1 = (int((self.x1+self.x2)/2), self.y1)
        arrowBase1 = self.drawArrow(arrowTip1, self.order, img)
        arrowTip2 = (int((self.companion.x1+self.companion.x2)/2),
                     self.companion.y1)
        arrowBase2 = self.drawArrow(arrowTip2, self.order, img)
        cv2.line(img, arrowBase1, arrowBase2, COLOR_BLACK, LINE_THICKNESS)

    def addCompanion(self, box, order: int):
        self.companion = box
        box.companion = self
        self.order = order
        box.order = order

    def addNext(self, n, x2=None, y1=None):
        if (x2 == None and y1 == None):
            self.next = Box(n, self.x2, self.y1)
        else:
            self.next = Box(n, x2, y1)

    def addPrevious(self, n):
        self.previous = Box(n, self.x1 - self.checkWidth(n), self.y1)

    def __repr__(self) -> str:
        return f"Box: {self.n}"


def factors(n):
    """Creates a dictionary object and a list containing factors of n"""
    factorsDict = {}
    f1 = []
    f2 = []
    for i in range(1, int(math.sqrt(n))+1, 1):
        if (n % i == 0):
            factorsDict[i] = int(n/i)
            f1.append(i)
            f2.append(int(n/i))
    factorsList = f1 + f2[::-1]
    factorsListUnique = list(set(factorsList))
    factorsListUnique.sort()
    return factorsDict, factorsList, factorsListUnique


def loadLogo(factor=0.25):
    global logoImg
    logoImg = cv2.imread('assets/logo.jpg')
    logoImg = cv2.cvtColor(logoImg, cv2.COLOR_BGR2RGB)
    return logoImg


loaded = False  # whether logo is loaded or not


def addLogo(img, n=10):
    global logoImg
    global loaded
    if (not loaded):
        loadLogo()
        loaded = 1
    logoImgWidth = int(img.shape[1]/3)
    logoImgHeight = int((logoImgWidth / logoImg.shape[1]) * logoImg.shape[0])
    logoImgTemp = cv2.resize(logoImg, (logoImgWidth, logoImgHeight))
    height = img.shape[0] + logoImgHeight
    width = img.shape[1]
    newImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    newImg[:, :, :] = 255
    newImg[logoImgHeight:, :] = img
    newImg[20:logoImgHeight+20, width-logoImgWidth-20:width-20] = logoImgTemp
    addText(newImg, f"Factors of {n}", (20, 20 + int(
        logoImgHeight*(3/4))), color=COLOR_BLACK, font_size=1.5 * logoImgHeight/FONT_PIX_H, thickness=4)

    # y_offset = 30
    # y_end = y_offset + logoImg.shape[0]
    # x_offset = img.shape[1] - logoImg.shape[1] - 30
    # x_end = img.shape[1] - 30
    # img[y_offset:y_end, x_offset:x_end] = logoImg
    return newImg


def addText(img, text, pos, color=COLOR_WHITE, font_size=FONT_SIZE, thickness=2):
    cv2.putText(img, text=text,
                org=(pos),
                fontFace=FONT, fontScale=font_size,
                color=color, thickness=thickness)


def createDetailedImage(n):
    factorsDict, factorsList, factorsListUnique = factors(n)
    width = 1920
    height = 1080
    npImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    npImg[:, :, :] = 255
    startingX = 50
    startingY = 100
    endingX = width - 50

    # Positive Integers
    addText(npImg, f"Factors of {n}:", (startingX, startingY),
            color=COLOR_BLACK, thickness=3)
    printText = ""
    startingY += int(FONT_PIX_H*0.7)
    for elem in factorsListUnique:
        printText += f"{elem}{', ' if elem != factorsListUnique[-1] else ''}"
        printLen = len(printText) * FONT_PIX_W
        if (elem == factorsList[-1]):
            addText(npImg, printText, pos=(
                startingX + 20, startingY), color=COLOR_ELEPHANT)
            startingY += int(FONT_PIX_H * 0.7)
            printText = ""
            break
        if (printLen >= endingX):
            addText(npImg, printText, (startingX+20,
                    startingY), color=COLOR_ELEPHANT)
            startingY += int(FONT_PIX_H*0.7)
            printText = ""

    # Negative Integers
    addText(npImg, f"Negative Factors of {n}:", (startingX, startingY),
            color=COLOR_BLACK, thickness=3)
    startingY += int(FONT_PIX_H*0.7)
    for elem in factorsListUnique:
        printText += f"-{elem}{', ' if elem != factorsListUnique[-1] else ''}"
        printLen = len(printText) * FONT_PIX_W
        if (elem == factorsList[-1]):
            addText(npImg, printText, pos=(
                startingX + 20, startingY), color=COLOR_ELEPHANT)
            break
        if (printLen >= endingX):
            addText(npImg, printText, (startingX+20,
                    startingY), color=COLOR_ELEPHANT)
            startingY += int(FONT_PIX_H*0.7)
            printText = ""

    saveImg(f"factors-of-{n}", npImg)
    if __name__ == "__main__":
        plt.imshow(npImg)
        plt.show()


def createBoxStructure(n):
    factorsDict, factorsList, factorsListUnique = factors(n)
    if (len(factorsListUnique) > 10):
        boxText = '  '.join([str(elem) for elem in factorsListUnique[-10:]])
        boxText += "  "
    else:
        boxText = '  '.join([str(elem) for elem in factorsListUnique])
        boxText += "  "
    # print(boxText)
    height = int(FONT_PIX_H * 1.5 * ((len(factorsListUnique)//10)+1)) + 100
    # print(len(factorsListUnique)//10)
    width = len(boxText) * FONT_PIX_W + 200
    if (width < 1024):
        width = 1024
    # Creating white background image
    npImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    npImg[:, :, :] = 255
    # boxes = []
    box = Box(factorsListUnique[0], 100, 100)
    box.draw(npImg)
    boxWidth = 0
    for i in range(1, len(factorsListUnique)):
        boxWidth += box.width
        if (i % 10 == 0):

            box.next = Box(
                factorsListUnique[i], 100, box.y1+int(FONT_PIX_H*1.5))
            centerElement(npImg, boxWidth+box.next.width,
                          width, box.y1, box.y2)
            boxWidth = 0
        else:
            box.addNext(factorsListUnique[i])
        box = box.next
        box.draw(npImg)

    centerElement(npImg, boxWidth+box.width*2,
                  width, box.y1, box.y2)
    npImg = addLogo(npImg, n)
    saveImg(f"factors-of-{n}-box", npImg)
    if __name__ == "__main__":
        plt.imshow(npImg)
        plt.show()


def centerElement(img, boxWidth, width, y1, y2):
    newImg = img[y1-5:y2+5, :boxWidth, :].copy()
    img[y1-5:y2+5, :boxWidth, :] = 255
    starting = (width-boxWidth) // 2
    img[y1-5: y2+5, starting:boxWidth+starting, :] = newImg
    pass


def createArrowStructure(n):
    factorsDict, factorsList, factorsListUnique = factors(n)
    pairsInOneLine = len(factorsList)//2
    if (len(factorsList) > 10):
        pairsInOneLine = 5
    if (len(factorsList) > (pairsInOneLine * 2)):
        boxText = '  '.join([str(elem)
                            for elem in factorsList[:pairsInOneLine]])
        boxText += '  '
        boxText += '  '.join([str(elem)
                             for elem in factorsList[-pairsInOneLine:]])
    else:
        boxText = '  '.join(str(elem) for elem in factorsList)

    # Separating left elements and right elements according to left x right
    factors_l = factorsList[:len(factorsList)//2]
    factors_r = factorsList[len(factorsList)//2:]

    # starting point
    startingX = 50
    startingY = 50 + (50 * pairsInOneLine)

    # Determining height and width of the image
    if (pairsInOneLine >= 5):
        height = (len(factors_l)//pairsInOneLine + 1) * \
            FONT_PIX_H + len(factors_l) * 50 + 200
    else:
        height = (len(factors_l)//pairsInOneLine + 1) * \
            FONT_PIX_H + len(factors_l) * 50
    width = len(boxText) * FONT_PIX_W + 200
    if (width < 1024):
        width = 1024

    npImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    npImg[:, :, :] = 255

    # Drawing elements without arrow
    lines = []
    line = []
    box = Box(factors_l[0], startingX, startingY)
    box.draw_backgroundless(npImg)
    line.append(box)
    ii = pairsInOneLine
    for i in range(1, len(factors_l)):
        if (i % pairsInOneLine == 0):
            # print(f"Triggered {i} => {i%pairsInOneLine}")

            # Draw the other elements
            for j in range(0, pairsInOneLine):
                box.addNext(factors_r[len(factors_r)-ii+j])
                box = box.next
                line.append(box)
                box.draw_backgroundless(npImg)
            lines.append(line)
            line = []
            ii += pairsInOneLine
            startingY += 50 + (50 * pairsInOneLine)
            box.addNext(factors_l[i], startingX, startingY)
        else:
            box.addNext(factors_l[i])
        box = box.next
        line.append(box)
        box.draw_backgroundless(npImg)

    # Rest of them
    for x in range(0, len(factors_r) - (ii-pairsInOneLine)):
        box.addNext(factors_r[x])
        box = box.next
        line.append(box)
        box.draw_backgroundless(npImg)
    lines.append(line)

    # Draw arrows
    for line in lines:
        boxWidth = 0
        for i in range(0, len(line)//2, 1):
            line[i].addCompanion(line[len(line)-i-1], order=(len(line)//2) - i)
            boxWidth += line[i].width + line[len(line) - i - 1].width
            line[i].joinCompanions(npImg)
        centerElement(npImg, boxWidth, width-50,
                      line[0].y1 - line[0].order*35, line[0].y2)
    npImg = addLogo(npImg, n)
    saveImg(f"factors-of-{n}-arrow", npImg)
    if __name__ == "__main__":
        plt.imshow(npImg)
        plt.show()


def createGeneralStructure(n):
    factorsDict, factorsList, factorsListUnique = factors(n)
    # Estimating width of element
    boxText = f"  {factorsList[0]}   x    {factorsList[-1]}  "

    # Height and Width determination
    if (len(factorsList) > 2):  # If number is not prime number
        height = int(len(factorsList)/4 * FONT_PIX_H) + 200
    else:  # If number is prime number
        height = int(2 * FONT_PIX_H) + 200

    width = len(boxText) * FONT_PIX_W * 2 + 200

    # Creating white background image
    npImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    npImg[:, :, :] = 255

    divided = 0
    if (len(factorsList) > 2):
        startingPoint = [(width//4) - (FONT_PIX_W*3), 100]
    else:
        startingPoint = [(width//2) - (FONT_PIX_W*3), 100]
    for i in range(0, len(factorsList)//2):
        if (i != 0 and i >= len(factorsList)//4 and divided == 0):
            startingPoint[0] = startingPoint[0] + int(len(boxText)*FONT_PIX_W)
            startingPoint[1] = 100
            divided = 1
        boxM = Box("x", startingPoint[0],
                   startingPoint[1])
        startingPoint[1] += FONT_PIX_H
        boxM.addPrevious(factorsList[i])
        boxM.addNext(factorsList[len(factorsList) - 1 - i])
        boxM.draw_backgroundless(npImg)
        boxM.previous.draw_backgroundless(npImg)
        boxM.next.draw_backgroundless(npImg)
        # if __name__ == "__main__":
        #     print(f"{boxM.previous.n} x {boxM.next.n}")
        #     plt.imshow(npImg)
        #     plt.show()
    npImg = addLogo(npImg, n)
    saveImg(f"factors-of-{n}-general", npImg)
    if __name__ == "__main__":
        plt.imshow(npImg)
        plt.show()


def saveImg(filename, img):
    imgBGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"images/{filename}.jpg", imgBGR)


if __name__ == "__main__":
    n = 4096
    # n = 20
    time1 = time.perf_counter()
    createDetailedImage(n)
    createBoxStructure(n)
    createArrowStructure(n)
    createGeneralStructure(n)
    # factors(n)
    time2 = time.perf_counter()
    print(time2 - time1)
    # print(fileNames)
