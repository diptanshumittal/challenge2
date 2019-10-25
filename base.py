import cv2 
import numpy as np
import sys

x = sys.argv[1]
img = cv2.imread(x)

#masking of red planes 
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([0,120,70])
upper_red = np.array([10,255,255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)
lower_red = np.array([170,120,70])
upper_red = np.array([180,255,255])
mask2 = cv2.inRange(hsv, lower_red, upper_red)
mask=mask1+mask2
mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
res = cv2.bitwise_and(img,img, mask= mask1)

#generating contours
cimg = cv2.cvtColor(res , cv2.COLOR_BGR2GRAY)
ret, thresh3 = cv2.threshold(cimg, 120, 255, cv2.THRESH_TRUNC)
alist = []
a, contoursGreen, hierarchy = cv2.findContours(thresh3,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
i=0
for contour in contoursGreen:
    i+=1
    x,y = cv2.minEnclosingCircle(contour)
    if cv2.contourArea(contour)<700  :
        continue    
    approx = cv2.approxPolyDP(contour , 0.01*cv2.arcLength(contour, True), True)
    peri = cv2.arcLength(contour, True)
    if(len(approx)>5):
        alist.append((x[0],x[1],y))        
    
temp = cv2.absdiff(img,res)
cimg1 = cv2.cvtColor(temp , cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(cimg1,(5,5),0)
ret, thresh1 = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
a, contoursRed, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
blist = []
max = 0
#cv2.imshow('res' , temp)
for contour in contoursRed:
    x,y = cv2.minEnclosingCircle(contour)
    a = int(x[0])
    b = int(x[1])
    x=(a,b)
    y=int(y)
    flag=0
    approx = cv2.approxPolyDP(contour , 0.01*cv2.arcLength(contour, True), True)
    for temp in alist:
        if (abs(temp[0]-x[0])<20 or abs(temp[0]-x[0])<20):
            #print(pow((abs(temp[0]-x[0])),2)+ pow((abs(temp[0]-x[0])),2), pow(temp[2],2))
            flag=1
    if(cv2.contourArea(contour)<700):
        continue
    elif(len(approx)<3):
        continue
    elif(flag==0):
        blist.append((x[0],x[1],y))
        if(y>max):
            max=y
for temp in blist:
    if(max==temp[2]):
        continue
    a = int(temp[0])
    b = int(temp[1])
    x=(a,b)
    y=int(temp[2])
    cv2.circle(img,x,y,(0,0,255),2)

ans = []
for temp in alist:
    a = int(temp[0])
    b = int(temp[1])
    x=(a,b)
    ans.append(x)
    y=int(temp[2])
    cv2.circle(img,x,y,(0,255,0),2)
print(ans)


cv2.imshow('frame',img)




  


    
