#-*-coding: utf-8 -*-
import cv2
import numpy as np
import math
img = cv2.imread('img.png') #อ่านรูปภาพ
Blur_img = cv2.GaussianBlur(img,(3,3),0) #GaussianBlur เพื่อทำให้ภาพบางจุดที่ขาดมาต่อเนื่องกัน
img_grey = cv2.cvtColor(Blur_img,cv2.COLOR_BGR2GRAY) #แปลงภาพเป็นขาวดำ เพื่อทำให้สามาถหาเส้นขอบของภาพได้
thresh = cv2.bitwise_not(cv2.threshold(img_grey, 127, 255, 0)[1]) #invert ภาพจากขาวเป็นดำ เพื่อทำให้สามาถหา conเส้นขอบของภาพได้
color_define = {'red':[0,0,255],'yellow':[0,255,255],'blue':[255,0,0],'white':[255,255,255],'pink':[180,105,255]} #ตัวแปรเก็บค่าสี BGR
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #หาเส้นขอบของรูปภาพ
cv2.drawContours(img,contours,-1,(0,255,0),2) #วาดเส้นขอบของรูปภาพ
color = list() #ตัวแปรกำหนดค่าสีของจุดต่างๆ
text = "" #ตัวแปรกำหนดชื่อของรูปแบบทรงต่างๆ
font = cv2.FONT_HERSHEY_SIMPLEX #เลือกใช้ font ชื่อ HERSHEY_SIMPLEX
type_number = {'Triangle':0,'Square':0,'Rectangle':0,'Circle':0} #ตัวแปรนับจำนวนของรูปทรงต่างๆ
for cnt in contours: # ลูปเส้นขอบของแต่ละรูปทรง
    approx = cv2.approxPolyDP(cnt,0.04*cv2.arcLength(cnt,True),True) #หาตำแหน่งมุมจากเส้นขอบของรูปทรงนั้นๆ
    list_cen_x = [i[0][0] for i in approx] #ตัวแปรเก็บตำแหน่งมุมของพิกเซล x
    list_cen_y = [i[0][1] for i in approx] #ตัวแปรเก็ยตำแหน่งมุมจองพิกเซล y
    cen_x = sum(list_cen_x)/len(approx) #หาจุดศูนย์กลางของพิกเซล x
    cen_y = sum(list_cen_y)/len(approx) #หาจุดศูนย์กลางของพิกเซล y
    if len(approx) == 3: #ตรวจสอบจำนวนจุดของมุมที่ได้
        color = color_define['red'] #กำหนดสีเป็นสีแดง
        text = 'Triangle' #กำหนดชื่อเป็น Triangle
        type_number[text]+=1 #เพิ่มจำนวนค่าของ ตัวแปรนับรูปทรง Triangle
    elif len(approx) == 4: #ตรวจสอบจำนวนจุดของมุมที่ได้
        distance = list() #ตัวแปรเก็บความกว้างยาวของสี่เหลี่ยม
        for x in range(0,2): #ลูปนับด้านของสี่เหลี่ยม
            a = math.fabs(list_cen_y[x]-list_cen_y[x+1]) #หาความยาวด้าน a
            b = math.fabs(list_cen_x[x]-list_cen_x[x+1]) #หาความยาวด้าน b
            distance.append(int(math.sqrt(math.pow(a,2)+math.pow(b,2)))) #หาความกว้างยาวของสี่เหลี่ยมจากพีทากรอรัส c^2 = a^2 + b^2
        if (distance[0] >= distance[1]-1) and (distance[0] <= distance[1]+1): #ตรวจสอบว่าแต่ละด้านเท่ากันหรือไม่ โดยกำหนดความคลาดเคลื่อน +-1
            text = 'Square' #กำหนดชื่อเป็น Square
            color = color_define['yellow'] #กำหนดสีเป็นสีเหลือง
            type_number[text]+=1 #เพิ่มจำนวนค่าของ ตัวแปรนับรูปทรง Square
        else :
            color = color_define['white'] #กำหนดสีเป็นสีขาว
            text = 'Rectangle' #กำหนดชื่อเป็น Rectangle
            type_number[text]+=1 #เพิ่มจำนวนค่าของ ตัวแปรนับรูปทรง Rectangle
    else :
        color = color_define['blue'] #กำหนดสีเป็นสีฟ้า
        text = 'Circle' #กำหนดชื่อเป็น Circle
        type_number[text]+=1 #เพิ่มจำนวนค่าของ ตัวแปรนับรูปทรง Circle
    for x in range(0,len(approx)): #ลูปนับจำนวนมุมของรูปทรง
        cv2.circle(img,(list_cen_x[x],list_cen_y[x]),4,color,-1) #วาดวงกลมไปยังมุมของรูปทรง
    cv2.circle(img,(cen_x,cen_y),4,color,-1) #วางวงกลมไปยังจุดศูนย์กลางของรูปทรง
    cv2.putText(img,text+' ('+str(cen_x)+','+str(cen_y)+') ',(min(list_cen_x),max(list_cen_y)+12), font, 0.35,color_define['pink'],1) #วาดตัวอักษรบอกชื่อและตำแหน่งจุดศูนย์กลางของรูปทรง

cv2.putText(img,'Triangle : '+str(type_number['Triangle']),(0,10), font, 0.35,color_define['pink'],1)      #|
cv2.putText(img,'Square : '+str(type_number['Square']),(0,30), font, 0.35,color_define['pink'],1)          # } วาดตัวอักษรบอกจำนวนของรูปทรงที่นับได้
cv2.putText(img,'Rectangle : '+str(type_number['Rectangle']),(0,50), font, 0.35,color_define['pink'],1)    #|
cv2.putText(img,'Circle : '+str(type_number['Circle']),(0,70), font, 0.35,color_define['pink'],1)          #|
cv2.imshow('image',img) #แสดงรูปภาพที่หาทุกอย่างเรียบร้อยแล้ว
cv2.waitKey(0) #รอ key เพื่อจบโปรแกรม
