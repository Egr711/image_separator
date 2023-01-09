from tkinter import Toplevel
import cv2
import math
import os
import numpy as np
import imutils
# CHANGE THESE VALUES TO YOUR LIKING

saveCropped = ord('f')
cancelCropped = ord('a')
goToNextImage = ord('d')
rotateR = ord('r')
rotateL = ord('e')
lineCropMode = ord('t')

# Shows image in this size
# (still uses original image size when cropping, this just makes larger images easier to crop)
height = 900

countStart = 68

print('Controlls:')
print("save: f")
print("cancel: a")
print("next image: d")
print("rotate: r")
print("rotate: e")
print("rotate by one degree: t")
print('change mode: t')


#========================================#

def rotateVector( a, deg ) :
    if deg % 90 != 0 :
        print("Error: rotation must be a multiple of 90 degrees")
        return a
    deg = deg % 360
    if deg == 0 :
        return a
    elif deg == 90 :
        return np.array( [ -a[1], a[0] ] )
    elif deg == 180 :
        return np.array( [ -a[0], -a[1] ] )
    elif deg == 270 :
        return np.array( [ a[1], -a[0] ] )

def getRotationAmount(degrees):
    if currentRotation == 90:
        return cv2.ROTATE_90_CLOCKWISE
    elif currentRotation == 180:
        return cv2.ROTATE_180
    elif currentRotation == 270:
        return cv2.ROTATE_90_COUNTERCLOCKWISE
    else:
        return -1

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

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

def getRotatedPoint(pt, radians, origin, offset):
    x, y = pt
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    return round(qx+offset[0]), round(qy+offset[1])

def shape_selection(event, x, y, flags, param):
    # making coordinates global
    global coordinates
    global scaledImage
    global image
    global currentCroppedImage
    global currentImageName
    global currentRotation
    global currentMode

    # Storing the (x1,y1) coordinates when left mouse button is pressed
    if currentMode == _REGULAR_: 
        if event == cv2.EVENT_LBUTTONDOWN:
            if currentMode == _REGULAR_: 
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
                elif k == rotateR or k == rotateL:
                    if k == rotateL:
                        currentRotation = (currentRotation + 270) % 360
                    else:
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
                    print('rotate:', rotateR)
                    print("key pressed 2:", k)
            coordinates = []
            scaledImage = ResizeWithAspectRatio(image, height=height)
    else: 
        if event == cv2.EVENT_LBUTTONUP:
            coordinates.append((x, y))
            # coordinates = [(111, 186), (254, 186), (109, 383)]
            if len(coordinates) == 3:

                print(coordinates)
                topLeft = coordinates[0]
                topRight = coordinates[1]
                bottomLeft = coordinates[2]

                yDiff = bottomLeft[1] - topLeft[1]

                topLine = (topRight[0] - topLeft[0], (topRight[1] - topLeft[1]) * -1)
                rotatedVectorNorm = unit_vector(rotateVector(topLine, 270))
                angle1 = angle_between(rotatedVectorNorm, (0, -1))
                hypLength = yDiff / math.cos(math.radians(angle1))

                bottomLeft = (round(rotatedVectorNorm[0] * hypLength) + topLeft[0], round(rotatedVectorNorm[1] * hypLength * -1) + topLeft[1])
                bottomRight = (round(rotatedVectorNorm[0] * hypLength) + topRight[0], round(rotatedVectorNorm[1] * hypLength * -1) + topRight[1])

                multiplyBy = -1 if topRight[1] < topLeft[1] else 1


                angleToRotateImage = angle_between(topLine, (1, 0)) * multiplyBy

                print('angle to rotate image:', angleToRotateImage)

                originalImageRotated = imutils.rotate(image, angle=angleToRotateImage)
                resizedOriginalImageRotated = imutils.resize(originalImageRotated, height=900)

                h, w = scaledImage.shape[:2]
                origin = (w/2, h/2)
                h_new, w_new = resizedOriginalImageRotated.shape[:2]
                xoffset, yoffset = (w_new - w)/2, (h_new - h)/2

                newTopRight = getRotatedPoint(topRight, np.radians(angleToRotateImage), origin, (xoffset, yoffset))
                newTopLeft = getRotatedPoint(topLeft, np.radians(angleToRotateImage), origin, (xoffset, yoffset))
                newBottomLeft = getRotatedPoint(bottomLeft, np.radians(angleToRotateImage), origin, (xoffset, yoffset))
                newBottomRight = getRotatedPoint(bottomRight, np.radians(angleToRotateImage), origin, (xoffset, yoffset))

                newBottomLeft = (newTopLeft[0], newBottomLeft[1])
                newBottomRight = (newTopRight[0], newBottomRight[1])

                currentName = currentImageName + '_' + str(currentCroppedImage - 1) + '.jpg'
                if countStart != -1:
                    currentName = str(countStart) + '_' + str(currentCroppedImage - 1) + '.jpg'


                cv2.imshow(currentName, resizedOriginalImageRotated[newTopLeft[1]:newBottomLeft[1], newTopLeft[0]:newTopRight[0]])

                coordinates = [newTopLeft, newBottomRight]
                ycoord1 = min(coordinates[0][0], coordinates[1][0])
                ycoord2 = max(coordinates[0][0], coordinates[1][0])
                xcoord1 = min(coordinates[0][1], coordinates[1][1])
                xcoord2 = max(coordinates[0][1], coordinates[1][1])

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
                        xmax = originalImageRotated.shape[0]
                        ymax = originalImageRotated.shape[1]
                        if xcoord1 < 0:
                            xcoord1 = 0
                        if ycoord1 < 0:
                            ycoord1 = 0
                        if xcoord2 > xmax:
                            xcoord2 = xmax
                        if ycoord2 > ymax:
                            ycoord2 = ymax

                        rotatedImage = originalImageRotated[xcoord1:xcoord2, ycoord1:ycoord2]
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
                    elif k == rotateR:
                        currentRotation = (currentRotation + 90) % 360
                        rotateAmount = getRotationAmount(currentRotation)

                        rotatedImage = resizedOriginalImageRotated[xcoord1:xcoord2, ycoord1:ycoord2]
                        if rotateAmount != -1:
                            rotatedImage = cv2.rotate(rotatedImage, rotateAmount)
                        cv2.destroyWindow(currentName)
                        cv2.imshow(currentName, rotatedImage)
                    elif k == -1:
                        continue
                    else:
                        print("cancel:", cancelCropped)
                        print("accept:", saveCropped)
                        print('rotate:', rotateR)
                        print("key pressed 2:", k)
                coordinates = []
                scaledImage = ResizeWithAspectRatio(image, height=height)

                coordinates = []

print("Type in count start:")
countStart = input()
if not countStart.isdigit():
    print("Type in count start:")
    countStart = input()
countStart = int(countStart)


_REGULAR_ = 0
_LINE_ = 1
_QUAD_ = 2
coordinates = []
currentRotation = 0
currentMode = _REGULAR_

listOfImageNames = sorted(os.listdir('./images'), key=lambda x: int(x.split('.')[0]))

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
                coordinates = []
                break
            elif k == -1:
                continue
            elif k == lineCropMode:
                currentMode = (currentMode + 1) % 2
                text = ""
                if currentMode == _LINE_:
                    text = "Line"
                elif currentMode == _QUAD_:
                    text = "Quad"
                else:
                    text = "Regular"
                print('current mode:', text)
                coordinates = []
            else:
                print("go to next:", goToNextImage)
                print("key pressed 1:", k)
        cv2.destroyWindow(imageName)
        break
