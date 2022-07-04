import cv2
import math
import os
# CHANGE THESE VALUES TO YOUR LIKING

saveCropped = ord('f')
cancelCropped = ord('a')
goToNextImage = ord('d')
rotate = ord('r')

# Shows image in this size
# (still uses original image size when cropping, this just makes larger images easier to crop)
height = 900

countStart = 68


#========================================#

def getRotationAmount(degrees):
    if currentRotation == 90:
        return cv2.cv2.ROTATE_90_CLOCKWISE
    elif currentRotation == 180:
        return cv2.cv2.ROTATE_180
    elif currentRotation == 270:
        return cv2.cv2.ROTATE_90_COUNTERCLOCKWISE
    else:
        return -1


def ResizeWithAspectRatio(_image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = _image.shape[:2]

    if width is None and height is None:
        return _image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def shape_selection(event, x, y, flags, param):
    # making coordinates global
    global coordinates
    global scaledImage
    global image
    global currentCroppedImage
    global currentImageName
    global currentRotation

    # Storing the (x1,y1) coordinates when left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates = [(x, y)]

    # Storing the (x2,y2) coordinates when the left mouse button is released and make a rectangle on the selected region
    elif event == cv2.EVENT_LBUTTONUP:
        coordinates.append((x, y))

        ycoord1 = min(coordinates[0][0], coordinates[1][0])
        ycoord2 = max(coordinates[0][0], coordinates[1][0])
        xcoord1 = min(coordinates[0][1], coordinates[1][1])
        xcoord2 = max(coordinates[0][1], coordinates[1][1])
        xmax = scaledImage.shape[0]
        ymax = scaledImage.shape[1]
        if xcoord1 < 0:
            xcoord1 = 0
        if ycoord1 < 0:
            ycoord1 = 0
        if xcoord2 > xmax:
            xcoord2 = xmax
        if ycoord2 > ymax:
            ycoord2 = ymax

        if xcoord2 == xcoord1 or ycoord1 == ycoord2:
            return
        currentName = currentImageName + '_' + str(currentCroppedImage - 1) + '.jpg'
        if countStart != -1:
            currentName = str(countStart) + '_' + str(currentCroppedImage - 1) + '.jpg'

        cv2.imshow(currentName, scaledImage[xcoord1:xcoord2, ycoord1:ycoord2])
        while (1):
            k = cv2.waitKey(33)
            if k == cancelCropped:  # a key
                cv2.destroyWindow(currentName)
                break
            elif k == saveCropped: # f key
                ycoord1 = round(min(coordinates[0][0], coordinates[1][0]) * scaledAmount)
                ycoord2 = round(max(coordinates[0][0], coordinates[1][0]) * scaledAmount)
                xcoord1 = round(min(coordinates[0][1], coordinates[1][1]) * scaledAmount)
                xcoord2 = round(max(coordinates[0][1], coordinates[1][1]) * scaledAmount)
                xmax = image.shape[0]
                ymax = image.shape[1]
                if xcoord1 < 0:
                    xcoord1 = 0
                if ycoord1 < 0:
                    ycoord1 = 0
                if xcoord2 > xmax:
                    xcoord2 = xmax
                if ycoord2 > ymax:
                    ycoord2 = ymax

                rotatedImage = image[xcoord1:xcoord2, ycoord1:ycoord2]
                rotationAmount = getRotationAmount(currentRotation)
                if rotationAmount != -1:
                    rotatedImage = cv2.rotate(rotatedImage, rotationAmount)

                saveName = currentName
                if countStart != -1:
                    currentImageName = currentImageName.split('.jpg')[0]
                    saveName = str(countStart) + '(' + currentImageName + ')' + '_' + str(currentCroppedImage - 1) + '.jpg'
                cv2.imwrite('./cropped/' + saveName, rotatedImage)
                currentCroppedImage += 1
                cv2.destroyWindow(currentName)
                currentRotation = 0
                break
            elif k == rotate:
                currentRotation = (currentRotation + 90) % 360
                rotateAmount = getRotationAmount(currentRotation)

                rotatedImage = scaledImage[xcoord1:xcoord2, ycoord1:ycoord2]
                if rotateAmount != -1:
                    rotatedImage = cv2.rotate(rotatedImage, rotateAmount)
                cv2.destroyWindow(currentName)
                cv2.imshow(currentName, rotatedImage)
            elif k == -1:
                continue
            else:
                print("cancel:", cancelCropped)
                print("accept:", saveCropped)
                print('rotate:', rotate)
                print("key pressed 2:", k)
        coordinates = []
        scaledImage = ResizeWithAspectRatio(image, height=height)


coordinates = []
currentRotation = 0

listOfImageNames = os.listdir('./images')

image = ''
for imageName in listOfImageNames :
    image = cv2.imread('images/' + imageName)
    scaledImage = ResizeWithAspectRatio(image, height=height)

    scaledAmount = image.shape[0]/height
    cv2.imshow(imageName, scaledImage)

    currentImageName = imageName
    currentCroppedImage = 1
    while(1):
        cv2.setMouseCallback(imageName, shape_selection)
        while (1):
            k = cv2.waitKey(33)
            if k == goToNextImage:  # d key
                if countStart != -1:
                    countStart += 1
                break
            elif k == -1:
                continue
            else:
                print("go to next:", goToNextImage)
                print("key pressed 1:", k)
        cv2.destroyWindow(imageName)
        break
