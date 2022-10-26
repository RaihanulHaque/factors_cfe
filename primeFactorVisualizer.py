from pickletools import optimize
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

IMG_STORAGE = "./images"
IMG_PREFIX = "prime_factorization"


def primeFactors(n):
    factors = {}
    c = 2
    while (n > 1):

        if (n % c == 0):
            factors[int(n)] = c
            n = n / c
        else:
            c = c + 1
    return factors


class CircleObject:
    def __init__(self, center, radius, value):
        self.center = center
        self.radius = int(radius)
        self.value = value
        self.left = None
        self.right = None

    def addLeft(self, value):
        self.leftCenter = (
            int(self.center[0] - self.radius * 2),
            int(self.center[1] + self.radius * 4)
        )
        self.left = CircleObject(center=self.leftCenter,
                                 radius=self.radius, value=value)

    def addRight(self, value):
        self.rightCenter = (
            int(self.center[0] + self.radius * 2),
            int(self.center[1] + self.radius * 4)
        )
        self.right = CircleObject(center=self.rightCenter,
                                  radius=self.radius, value=value)


def drawCircleElement(circle: CircleObject, lines=True):
    global npImg
    fontAdjustment1 = 10
    fontAdjustment2 = 10
    color1 = (37, 150, 190)
    color2 = (255, 166, 77)
    fontAdjustmentFactor = len(str(circle.value)) - 1
    fontAdjustment2 = fontAdjustment2 * fontAdjustmentFactor

    font = cv2.FONT_HERSHEY_SIMPLEX
    if lines:
        if (circle.left != None):
            cv2.line(npImg, pt1=circle.center,
                     pt2=circle.leftCenter, color=color1, thickness=5)
        if (circle.right != None):
            cv2.line(npImg, pt1=circle.center,
                     pt2=circle.rightCenter, color=color1, thickness=5)
    if (circle.left == None):
        cv2.circle(npImg, center=circle.center, radius=circle.radius,
                   color=color2, thickness=-1)
    else:
        cv2.circle(npImg, center=circle.center, radius=circle.radius,
                   color=color1, thickness=-1)
    cv2.putText(npImg, text=str(circle.value), org=(circle.center[0] - (fontAdjustment1 + fontAdjustment2), circle.center[1] + fontAdjustment1), fontFace=font,
                fontScale=1, color=(255, 255, 255), thickness=2)


count = 1


def show(circle: CircleObject, n: int):
    rad = 60
    scale = int(rad * 1.6) - rad
    global npImg
    global count
    if circle:

        # time.sleep(10)
        drawCircleElement(circle, lines=False)
        coeff = int((count-1)/2)
        if (count != 1 and (count+1) % 2 == 0):
            # print(f"{count} {int((count -1)/2) }")
            # plt.imshow(npImg)
            # plt.show()
            height = int(circle.center[1]) + rad + 20
            saveImg(npImg[:height, :],
                    n, type="tree", step=str(coeff))
        count = count + 1
        drawCircleElement(circle)

        show(circle.left, n)
        show(circle.right, n)
        # count = 0


def createTreeStructure(n: int):
    global count
    global logoImg
    count = 1
    global npImg
    global fileNames
    fileNames = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    items = primeFactors(n)
    radius = 60
    height = int(radius * 4 * (len(items)))
    width = int((len(items) + 2) * 2 * radius)
    if width < (radius*10):
        width = radius*10
    centerX = (radius * 3) + radius
    # centerX = radius*4
    centerY = int((3/2)*radius)
    center = (centerX, centerY)
    root = CircleObject(center=center, value=n, radius=radius)
    branch = root
    for key in items:
        branch.value = key

        if (key != items[key]):
            branch.addLeft(items[key])
            branch.addRight(1)
            branch = branch.right

    npImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    npImg[:, :, :] = 255
    logoImg = loadLogo(0.4)
    show(root, n)
    # endText = generateEndText(n, items=items)
    # pixValue = len(endText)*20
    # org = (int((width/2) - (pixValue/2)), height - 50)
    # cv2.putText(npImg, text=endText,
    #             org=org, fontFace=font,
    #             fontScale=1.2, color=(0, 0, 0), thickness=2)
    saveImg(npImg, n=n, type="tree", step=str(len(items)-1))
    # plt.imshow(npImg)
    # plt.show()
    return fileNames


def createDivisionStructure(n):
    global logoImg
    global fileNames
    fileNames = []
    global npImg
    font = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 2
    color1 = (37, 150, 190)
    items = primeFactors(n)
    height = int((len(items) + 2) * 90) + 200
    logoPadding = 250
    width = int(len(items)*40) + logoPadding
    if width < 800:
        width = 800
    npImg = np.zeros(shape=(height, width, 3), dtype=np.uint16)
    logoImg = loadLogo()
    npImg[:, :, :] = 255
    textX = 200
    textY = 200

    i = 0
    increaseFactor = 90
    for key in items:
        fontAdjustment2 = 30
        fontAdjustmentFactor = len(str(items[key])) - 1
        # print(fontAdjustmentFactor) # Baka
        fontAdjustment2 = fontAdjustment2 * fontAdjustmentFactor

        # putting divident numbers on screen
        cv2.putText(npImg, text=f"{key}",
                    org=(textX + 150, textY + i * increaseFactor), fontFace=font,
                    fontScale=fontScale, color=color1, thickness=3)
        # putting the vertical line
        cv2.line(npImg,
                 pt1=(textX + 100, textY - 50),
                 pt2=(textX + 100, textY + i * increaseFactor),
                 color=(0, 0, 0),
                 thickness=3
                 )
        if (i != 0):    # for avoiding saving the first image
            saveImg(img=npImg[:textY + i * increaseFactor + 100],
                    n=n, type="division", step=str(i))
        # Putting the divisor text
        cv2.putText(npImg, text=f"{items[key]}",
                    org=(textX - fontAdjustment2, textY + i * increaseFactor), fontFace=font,
                    fontScale=fontScale, color=(255, 102, 0), thickness=3)
        cv2.line(npImg,
                 pt1=(int(textX/2), int(textY + 20 + i*increaseFactor)),
                 pt2=(int(width-textX/2),
                      int(textY + 20 + i*increaseFactor)),
                 color=(0, 0, 0), thickness=3
                 )
        i += 1

    cv2.putText(npImg, text=f"1",
                org=(textX+150, textY + i * increaseFactor), fontFace=font,
                fontScale=fontScale, color=color1, thickness=3)
    cv2.line(npImg,
             pt1=(textX + 100, textY - 50),
             pt2=(textX + 100, textY + i * increaseFactor),
             color=(0, 0, 0),
             thickness=3
             )

    # answers = [str(items[key]) for key in items]
    # answers.append(str(1))
    # answers = ', '.join(answers)
    # endText = f"We got the prime factors of {n} as {answers}"
    endText = generateEndText(n, items=items)
    pixValue = len(endText)*12
    org = (int((width/2) - (pixValue/2)), height - 50)
    cv2.putText(npImg, text=endText,
                org=org, fontFace=font,
                fontScale=0.7, color=(0, 0, 0), thickness=2)
    # plt.imshow(npImg)
    # plt.show()
    saveImg(npImg, n=n, type="division", step=f"{i}")
    return fileNames


def generateEndText(n, items):
    answers = [str(items[key]) for key in items]
    answers = set(answers)
    x = []
    for a in answers:
        x.append(a)
    xStr = ', '.join(x)
    endText = f"We got the prime factors of {n} as {xStr}"
    return endText


def loadLogo(factor=0.25):
    logoImg = cv2.imread('assets/logo.jpg')
    logoImg = cv2.cvtColor(logoImg, cv2.COLOR_BGR2RGB)
    newRatio = (int(logoImg.shape[1]*factor), int(logoImg.shape[0]*factor))
    logoImg = cv2.resize(
        logoImg, newRatio
    )
    return logoImg


def addLogo(img):
    global logoImg
    logoImgWidth = int(img.shape[1]/3)
    logoImgHeight = int((logoImgWidth / logoImg.shape[1]) * logoImg.shape[0])
    logoImg = cv2.resize(logoImg, (logoImgWidth, logoImgHeight))
    y_offset = 30
    y_end = y_offset + logoImg.shape[0]
    x_offset = img.shape[1] - logoImg.shape[1] - 30
    x_end = img.shape[1] - 30
    img[y_offset:y_end, x_offset:x_end] = logoImg
    return img


def saveImg(img, n: int, type: str, step=''):
    global fileNames
    img = addLogo(img)
    imgWidth = 1024
    imgHeight = int((imgWidth / img.shape[1]) * img.shape[0])
    imgResized = cv2.resize(img, (imgWidth, imgHeight))
    saveImg = cv2.cvtColor(imgResized, cv2.COLOR_RGB2BGR)
    fileName = f"{IMG_STORAGE}/{IMG_PREFIX}_{n}_{type}_{step}.webp"
    fileNames.append(fileName)
    cv2.imwrite(fileName, saveImg, [int(cv2.IMWRITE_WEBP_QUALITY), 80])


def drawOnBanner(img, text, font, pos, color="#0e4fa1"):
    imgDraw = ImageDraw.Draw(im=img)
    imgDraw.text(xy=pos, text=text,
                 font=font, fill=color)


def createBanner(n: int):
    whiteBanner = Image.open("assets/whiteBanner.jpg")
    bannerSimple = Image.open("assets/banner_simple.jpg")
    bannerComplex = Image.open("assets/banner_complex.jpg")
    robotoFont = ImageFont.truetype(
        font='assets/roboto/Roboto-Black.ttf', size=90)
    omegaFont1 = ImageFont.truetype(font='assets/omega/omega.ttf', size=150)
    omegaFont2 = ImageFont.truetype(font='assets/omega/omega.ttf', size=120)
    drawOnBanner(whiteBanner, f"OF {n}", robotoFont, (55, 290))
    drawOnBanner(bannerSimple, f"{n}", omegaFont1, (370, 560), "white")
    drawOnBanner(bannerComplex, f"{n}", omegaFont2, (372, 562), "black")
    drawOnBanner(bannerComplex, f"{n}", omegaFont2, (370, 560), "white")
    ext = "jpg"
    imgQuality = 50
    arr = [f"./images/{IMG_PREFIX}_{n}_banner_white.{ext}",
           f"./images/{IMG_PREFIX}_{n}_banner_simple.{ext}",
           f"./images/{IMG_PREFIX}_{n}_banner_complex.{ext}"]
    whiteBanner.save(arr[0], optimize=True, quality=imgQuality)
    bannerSimple.save(arr[1], optimize=True, quality=imgQuality)
    bannerComplex.save(arr[2], optimize=True, quality=imgQuality)
    return arr


def generateImages(n: int):
    arr = {}

    arr["TreeFiles"] = [i for i in createTreeStructure(n)]
    if (len(arr["TreeFiles"]) > 1):
        arr["TreeFiles"].pop()
    arr["DivisionFiles"] = [i for i in createDivisionStructure(n)]
    arr["Banners"] = [i for i in createBanner(n)]
    # arr.__repr__()
    return arr


fileNames = []

if __name__ == "__main__":
    n = 20
    time1 = time.perf_counter()
    # createTreeStructure(n)
    # createDivisionStructure(n)
    # print(primeFactors(n))
    print(generateImages(n))
    time2 = time.perf_counter()
    print(time2 - time1)
    # print(fileNames)