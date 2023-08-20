#imports
import numpy as np
import cv2
from matplotlib import pyplot as pt

#ignore table function
def ignoreTable (image):
    #transform color image to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #apply adaptive threshold to form binary of backgrond and foreground
    binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
    
    
    
    # Find contours of binary image
    cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 2:
        cnts = cnts[0]  
    else:
        cnts = cnts[1]
    
    #draw contour
    for c in cnts:
        cv2.drawContours(binary, [c], -1, (255,255,255), -1)
    
    
    # apply opening morphology to remove noise(text) from binary image with 9x9 kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    opened_binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=4)
    
    # find table
    cnts = cv2.findContours(opened_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 2:
        cnts = cnts[0]  
    else:
        cnts = cnts[1]
    
    # draw white rectangle on image to omit table
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,255), -1)
    
    return image

#detect columns function
def detectColumn(image):
    
    #convert image to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #apply adaptive threshold to form binary of backgrond and foreground
    binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,25,15)
    
    
    #apply closing morphology to make paragraphs blocks instead of texts with kernel size 21x131
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 131))
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    pt.imshow(closing, "gray")
    
    #find contours of image
    cnts = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 2:
        cnts = cnts[0]  
    else:
        cnts = cnts[1]
        
    counter = 0
    
    if(len(cnts) > 1):
        #crop image based on columns
        for cnt in cnts:
            convex = cv2.convexHull(cnt)
            x, y, w, h = cv2.boundingRect(convex)
            x = x-50
            y = y-50
            w = w+100
            h = h+100
            
            cropped = image[y:y + h, x:x + w]
            
            #merge columns to one column only
            if (len(cnts) - counter == len(cnts)):
                temp = cropped
            else:
                w_min = min(temp.shape[1],cropped.shape[1])
                ftemp = cv2.resize(temp, (w_min, int(temp.shape[0] * w_min / temp.shape[1])), cv2.INTER_CUBIC)
                fcrop = cv2.resize(cropped, (w_min, int(cropped.shape[0] * w_min / cropped.shape[1])),cv2.INTER_CUBIC)
                
                merge = np.concatenate((fcrop,ftemp),0)
                
                temp = merge
                
            counter += 1
            
    else:
        merge = image

    #return merged image
    return merge


#extract and sort paragraphs function
def extract(image, number):
    
    #convert image to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #apply adaptive threshold to form binary of backgrond and foreground
    binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,25,15)
    
    #apply closing morphology to make paragraphs blocks instead of texts with kernel size 31x31
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31))
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    #find contours of image
    cnts, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counter = 0
    
    #draw countours on image
    for cnt in cnts:
        
        name = len(cnts) - counter
        counter += 1
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = image[y:y + h, x:x + w]
        
        #add padding to extracted paragraph
        cropped = cv2.copyMakeBorder(cropped, 50, 50, 50, 50, cv2.BORDER_CONSTANT,value=[255,255,255])
        cv2.imwrite('output/Material00' + str(number) + '/Paragraph_' + str(name) + '.png', cropped)
        cv2.rectangle(image, (x, y), (x + w, y + h), (200, 0, 0), 2)


#read images
# image1 = cv2.imread("001.png")
# image2 = cv2.imread("002.png")
# image3 = cv2.imread("003.png")
# image4 = cv2.imread("004.png")
image5 = cv2.imread("005.png")
# image6 = cv2.imread("006.png")
# image7 = cv2.imread("007.png")
# image8 = cv2.imread("008.png")

#ignore tables for all images
# ignored1 = ignoreTable(image1)
# ignored2 = ignoreTable(image2)
# ignored3 = ignoreTable(image3)
# ignored4 = ignoreTable(image4)
ignored5 = ignoreTable(image5)
# ignored6 = ignoreTable(image6)
# ignored7 = ignoreTable(image7)
# ignored8 = ignoreTable(image8)

#detect column for all images
# detected1 = detectColumn(ignored1)
# detected2 = detectColumn(ignored2)
# detected3 = detectColumn(ignored3)
# detected4 = detectColumn(ignored4)
detected5 = detectColumn(ignored5)
# detected6 = detectColumn(ignored6)
# detected7 = detectColumn(ignored7)
# detected8 = detectColumn(ignored8)

#extract text for all images
# extract(detected1,1)
# extract(detected2,2)
# extract(detected3,3)
# extract(detected4,4)
# extract(detected5,5)
# extract(detected6,6)
# extract(detected7,7)
# extract(detected8,8)


