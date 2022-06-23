import cv2
import math
import os
# CHANGE THESE VALUES TO YOUR LIKING

# a = 97
# f = 102
# d = 100
saveCropped = ord('f')
cancelCropped = ord('a')
goToNextImage = ord('d')

# Shows image in this size
# (still uses original image size when cropping, this just makes larger images easier to crop)
height = 900


#========================================#

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

        # Drawing a rectangle around the region of interest (roi)
        cv2.imshow(currentImageName + '_' + str(currentCroppedImage) + '.jpg', scaledImage[xcoord1:xcoord2, ycoord1:ycoord2])
        while (1):
            k = cv2.waitKey(33)
            if k == cancelCropped:  # a key
                cv2.destroyWindow(currentImageName + '_' + str(currentCroppedImage) + '.jpg')
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
                cv2.imwrite('./cropped/' + currentImageName + '_' + str(currentCroppedImage) + '.jpg', image[xcoord1:xcoord2, ycoord1:ycoord2])
                currentCroppedImage += 1
                cv2.destroyWindow(currentImageName + '_' + str(currentCroppedImage - 1) + '.jpg')
                break
            elif k == -1:
                continue
            else:
                print("key pressed:", k)
        coordinates = []
        scaledImage = ResizeWithAspectRatio(image, height=height)

coordinates = []

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
                break
            elif k == -1:
                continue
            else:
                print("key pressed:", k)
        cv2.destroyWindow(imageName)
        break
