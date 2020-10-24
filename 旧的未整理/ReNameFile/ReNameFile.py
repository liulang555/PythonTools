#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil
import time
import urllib.request
import requests
import urllib.parse
import json
import random
import hashlib
import langid
#reload(sys)
#sys.setdefaultencoding('utf-8')
from googletrans import Translator
sys.setrecursionlimit(10000)  # set the maximum depth as 10000

Deletelist_Type=[".chm",".html",".htm",".mht",".torrent",".apk",".lnk",".CHM"]
Deletelist_Folder=["論壇文宣","宣傳文件","／宣傳文檔"]
ReNamelist_Folder=[]
Deletelist_File=[]
re_words=re.compile(u"[\u4e00-\u9fa5]+")

def ReadConfig(path):
	list=[]
	try:
		file=open(path,"rb")#选用rb  防止读取文件出错
		#filereader=file.decode("utf-8")
	except IOError:
		print ("open file fail:  "+path)
	else:
		for index in file:
			line=index.decode("utf-8").strip()
			if line!="":
				#print(line)
				list.append(line)
		file.close()
		return list;	
		



#获取修改后的名字
def modificationname(basename,suffixname):
	#print("modificationname--basename:    "+basename)
	newname=basename
	for index in range(len(ReNamelist_Folder)):
		if ReNamelist_Folder[index] in basename:
			newname=newname.replace(ReNamelist_Folder[index],'')
	return newname
		
def ChangeName(oldpath,newpath):
	if(oldpath!=newpath):
		try:
			if not os.path.exists(newpath):
				os.rename(oldpath,newpath)
			else:
				print("已经存在了这个文件或者文件夹："+newpath+"        源文件： "+oldpath)
		except IOError:
			print ("open file fail:  "+oldpath)
	#else:
		#print ("ChangeName:  "+oldpath)
def checkDeltefile(path):
	basename=os.path.basename(path)
	if basename in Deletelist_File:
		os.remove(path)
		return True
	file=os.path.splitext(basename)
	if file[1] in Deletelist_Type:
		os.remove(path)
		return True
	return False
	
def FindAllPath(rootdir):
	for Root,dirs,files in os.walk(rootdir):
		for file in files:
			if not checkDeltefile(os.path.join(Root,file)):
				suffixname=os.path.splitext(file)
				newname=modificationname(file,suffixname[1])
				#print("filepath:  "+file+"-----newname:  "+newname)
				ChangeName(os.path.join(Root,file),os.path.join(Root,newname))
		for dir in dirs:
			newname=modificationname(dir,'')
			#print("dirpath:  "+dir+"-----newname:  "+newname)
			ChangeName(os.path.join(Root,dir),os.path.join(Root,newname))


if __name__=="__main__":
	IsTest=1
	if IsTest==1:
		rootdir="C:/Users/BugCreater/Desktop/Python/ReNameFile/新建文件夹"
	else:
		rootdir="D:/迅雷下载/已下载"
	Deletelist_File=ReadConfig("C:/Users/BugCreater/Desktop/Python/ReNameFile/Config.txt")
	ReNamelist_Folder=ReadConfig("C:/Users/BugCreater/Desktop/Python/ReNameFile/ReplaceName.txt")
	FindAllPath(rootdir)
	FindAllPath("E:/ThunderDownLoad/((已完成下载))")
	print("所有 完成")
	if IsTest==1:
		os.system("pause");


