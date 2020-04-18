import cv2
import numpy as np

olemiss_original = cv2.imread('olemiss.jpg',0)
#cv2.imshow('olemiss.jpg',olemiss)

ret, olemiss = cv2.threshold(olemiss_original, 120, 255, cv2.THRESH_BINARY)

def minkowski_subtraction(img):
    for i in range(1, len(img)-1):
        for j in range(1, len(img[i])-1):
            
            if (img[i-1][j-1] == 255 and img[i-1][j] == 255 and img[i-1][j+1]  == 255 and 
                img[i][j-1] == 255 and img[i][j] == 255 and img[i][j+1] == 255 and 
                img[i+1][j-1] == 255 and img[i+1][j] == img[i+1][j+1] == 255):
                print(i, j)
                img[i][j] = 255
                
            else:
                img[i][j] = 0
    return img



def erosion(img, kernel, n):
    #erosion using opencv inbuilt function cv2.erode()
    erosion = cv2.erode(img, kernel, iterations = n)
    return erosion
    
def dialation(img, kernel, n):
    dialation = cv2.dilate(img, kernel, iterations = n)
    return dialation
    
def opening(img, kernel):
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening

def closing(img, kernel):
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing

def border1(img, kernel):
    erode = erosion(img, kernel, 1)
    
    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
            if(img[i][j] != erode[i][j]):
                erode[i][j] = 255
            else:
                erode[i][j] = 0
                
    return erode


def border2(img, kernel):
    dilate = dialation(img, kernel, 1)
    
    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
            if(img[i][j] != dilate[i][j]):
                dilate[i][j] = 255
            else:
                dilate[i][j] = 0
                
    return dilate
   
def border3(img, kernel):
    dilate = dialation(img, kernel, 2)
    erode = erosion(img, kernel, 1)
    
    temp = np.zeros((327, 452), dtype = np.uint8)
    
    for i in range(0, len(dilate)):
        for j in range(0, len(dilate[i])):
           if(dilate[i][j] != erode[i][j]):
               temp[i][j] = 255
           else:
               temp[i][j] = 0
               
    new_erode = erosion(temp, kernel, 1)
    
    return new_erode

'''
cv2.imshow('original',olemiss)
erode = minkowski_subtraction(olemiss)
cv2.imshow('erosion', erode)
'''
#set up a 3x3 structuring element
kernel = np.ones((3,3), np.uint8)

erode = erosion(olemiss, kernel, 2)
#cv2.imshow('Eroded', erode)
cv2.imwrite('eroded.jpg', erode)

dilate = dialation(olemiss, kernel, 2)
#cv2.imshow('Dilated', dilate)
cv2.imwrite('dilated.jpg', dilate)

opened = opening(olemiss, kernel)
#cv2.imshow('Opened', opened)
cv2.imwrite('opened.jpg', opened)

closed = closing(olemiss, kernel)
#cv2.imshow('Closed', closed)
cv2.imwrite('closed.jpg', closed)

#border detection
border_image1 = border1(olemiss, kernel)
#cv2.imshow('Border Image1', border_image1)
cv2.imwrite('Border Image1.jpg', border_image1)

border_image2 = border2(olemiss, kernel)
#cv2.imshow('Border Image 2', border_image2)
cv2.imwrite('Border Image2.jpg', border_image2)

border_image3 = border3(olemiss, kernel)
#cv2.imshow('Border Image 3', border_image3)
cv2.imwrite('Border Image3.jpg', border_image3)


cv2.waitKey(0)
cv2.destroyAllWindows()






















