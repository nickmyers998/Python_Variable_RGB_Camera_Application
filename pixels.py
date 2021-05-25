import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time
from PIL import Image


def func():

    # This function finds high density color areas of a color-parsed image provided in camapp.py and focuses a gray box around the area of average density

    img = cv.imread("           REPLACE WITH DESIRED FILE PATH FOR color_screenshot.png", 1)   # Opens cv image

    count_all = int(img.size/3)                                 # Gets total pixels in image
    count_blk = int(np.sum(img < 255)/3)                        # Counts all black pixels
    count_wht = int(np.sum(img==255)/3)                         # Counts all white pixels
    print("Total pixels: " + str(count_all))                    
    print("Total white pixels: " + str(count_wht))
    print("Total black pixels: " + str(count_blk))
    blk_dist = round(100*count_blk / count_all, 4)              # Gets black pixel percentage
    wht_dist = round(100*count_wht / count_all, 4)              # Gets white pixel percentage

    print("Black pixel percentage: " + str(blk_dist) + "%")
    print("White pixel percentage: " + str(wht_dist) + "%")

    x = img.shape
    imwidth, imlength = x[0], x[1]                              # Gets image width and length
    print("Width: " + str(imwidth) + " pixels")
    print("Length: " + str(imlength) + " pixels")
    numwidth = 0
    numlength = 0
    wlist = [0]*imwidth                                         # Initialize list of width rows
    llist = [0]*imlength                                        # Initialize list of length columns
    num = 0
    for i in range(imwidth):                                    # Loops find white pixel occurances in each row and column of image
        for x in range(imlength):

            if img[i][x][0] == 255:
                wlist[i] += 1
                llist[x] += 1


    for i in range(imwidth):                                    # Multiplies number of white pixel occurances in each row by the row number
        wlist[i] *= i                                           # Multiplies number of white pixel occurances in each column by the column number
    for i in range(imlength):
        llist[i] *= i
        
        
    print("Weighted sum width = " + str(sum(wlist)))
    print("Weighted sum length = " + str(sum(llist)))
    numwidth = int(sum(wlist)/count_wht)                        # Gets the weighted average density row
    numlength = int(sum(llist)/count_wht)                       # Gets the weighted average density column

    print("Average Width Column: %d" % numwidth)
    print("Average Length Column: %d" % numlength)

    scaler = int(wht_dist*imwidth*.01)                          # Scales identifier box to total white pixel count
    if scaler < 8:
        scaler = 20
    print("Box scaler: " + str(scaler))

    w_high = numwidth + scaler
    w_low = numwidth - scaler
    l_high = numlength + scaler
    l_low = numlength - scaler

    w2_high = w_high - 8
    w2_low = w_low + 8
    l2_high = l_high - 8
    l2_low = l_low + 8

    newim = Image.open("            REPLACE WITH DESIRED FILE PATH FOR color_screenshot.png")       # Saves image and creates a new image for box generation
    newim.save("                    REPALCE WITH DESIRED FILE PATH FOR imtest.png")
    altim = Image.open("            REPLACE WITH DESIRED FILE PATH FOR imtest.png")
    pixels = altim.load()


    for i in range(altim.size[1]):                                                  # Draws solid box around high density image area
        for x in range(altim.size[0]):

            if (i < w_high) and (i > w_low) and (x < l_high) and (x > l_low):
                altim.putpixel((x, i), (100))

    for i in range(altim.size[1]):                                                  # "Hollows out" box and replaces pixels within
        for x in range(altim.size[0]):

            if (i < w2_high) and (i > w2_low) and (x < l2_high) and (x > l2_low):
                h = newim.getpixel((x, i))
                altim.putpixel((x, i), (h))

    altim.show()                                                                    # Opens box image using Windows photo app


def timer():        

    # This function is used to test the performance of the pixel analysis function

    totalt = 0

    for i in range(20):
        start_time = time.time()
        func()
        timelapsed = (time.time() - start_time)
        totalt += timelapsed
        

    print("\n\n\n------%s seconds average ------" % (totalt/20))

func()  # Call main
