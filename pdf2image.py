# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 17:25:06 2019

@author: v-yisun
"""

from PIL import Image
import os
import pytesseract

path = "D:/Documents/work/pdfwork/input" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称

################切割大图片成小图片并命名#######################
num = 0
for file in files:

    img = Image.open('D:/Documents/work/pdfwork/input/'+file)
    length = img.size[0]/5
    width = img.size[1]/2
    for i in range(5):
        cropped = img.crop(( i*length, 0, (i+1)*length,width))# (left, upper, right, lower)
        cropped.save('D:/Documents/work/pdfwork/output1/'+str(num)+'.jpg')
        num = num+1
        cropped = img.crop((i*length, width, (i+1)*length,2*width))# (left, upper, right, lower        
        cropped.save('D:/Documents/work/pdfwork/output1/'+str(num)+'.jpg')
        num = num+1
        
############文字识别######################################
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
path = 'D:/Documents/work/pdfwork/output1/'
files= os.listdir(path)

for file in files:
    text = pytesseract.image_to_string(Image.open(path+file),lang='jpn')
    token = text.split('\n')       
    f = open('D:/Documents/work/pdfwork/output2/'+file+'.txt','w')
    for to in token:        
        if len(to.strip()):
            f.write(to+'\n')
    f.close()