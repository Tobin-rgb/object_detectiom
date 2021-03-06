# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 14:11:04 2020

@author: Ping
"""

import os
import cv2

try:
  import xml.etree.cElementTree as ET #解析xml的c语言版的模块
except ImportError:
  import xml.etree.ElementTree as ET


##get object annotation bndbox loc start 
def GetAnnotBoxLoc(AnotPath):#AnotPath VOC标注文件路径
  tree = ET.ElementTree(file=AnotPath) #打开文件，解析成一棵树型结构
  root = tree.getroot()#获取树型结构的根
  ObjectSet=root.iter('object')#找到文件中所有含有object关键字的地方，这些地方含有标注目标
  ObjBndBoxSet={} #以目标类别为关键字，目标框为值组成的字典结构
  for Object in ObjectSet:
    ObjName=Object.find('name').text
    BndBox=Object.find('bndbox')
    x1 = int(BndBox.find('xmin').text)#-1 #-1是因为程序是按0作为起始位置的
    y1 = int(BndBox.find('ymin').text)#-1
    x2 = int(BndBox.find('xmax').text)#-1
    y2 = int(BndBox.find('ymax').text)#-1
    BndBoxLoc=[x1,y1,x2,y2]
    if ObjName in ObjBndBoxSet:
        ObjBndBoxSet[ObjName].append(BndBoxLoc)#如果字典结构中含有这个类别了，那么这个目标框要追加到其值的末尾
    else:
        ObjBndBoxSet[ObjName]=[BndBoxLoc]#如果字典结构中没有这个类别，那么这个目标框就直接赋值给其值吧
  return ObjBndBoxSet
##get object annotation bndbox loc end
 
def display(objBox,pic):
  img = cv2.imread(pic)
   
  for key in objBox.keys():
    for i in range(len(objBox[key])):
      cv2.rectangle(img, (objBox[key][i][0],objBox[key][i][1]), (objBox[key][i][2], objBox[key][i][3]), (0, 0, 255), 2)    
      cv2.putText(img, key, (objBox[key][i][0],objBox[key][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
  cv2.imshow('img',img)
  cv2.imwrite('display.jpg',img)
  cv2.waitKey(0)
 
 
if __name__== '__main__':
  pic = r"E:/data/VOCdevkit/VOC2007/JPEGImages/000282.jpg"
  ObjBndBoxSet=GetAnnotBoxLoc(r"E:/data/VOCdevkit/VOC2007/Annotations/000282.xml")
  print(ObjBndBoxSet)
  display(ObjBndBoxSet,pic)