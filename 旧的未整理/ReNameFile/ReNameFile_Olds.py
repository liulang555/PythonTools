#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil
import time
#reload(sys)
#sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(10000)  # set the maximum depth as 10000

Deletelist_Type=[".chm",".html",".htm",".mht",".torrent",".apk",".lnk",".CHM"]
Deletelist_Folder=["論壇文宣","宣傳文件","／宣傳文檔"]
ReNamelist_Folder=["第一會所新片","Tokyo-Hot","@","第一會所新片@SIS001@","@草榴社區@","@第一会所@","【片片勃士】【sex8.cc】","【娼井空】【sex8.cc】"]
Deletelist_File=[]
re_words=re.compile(u"[\u4e00-\u9fa5]+")
#获取修改后的名字
def modificationname(basename,suffixname):
	print("basename:    "+basename)
	newname=basename
	for index in range(len(ReNamelist_Folder)):
		if ReNamelist_Folder[index] in basename:
			newname=newname.replace(ReNamelist_Folder[index],'')
	if len(newname)>28:
		str=re_words.findall(newname)
		fanhao=re.findall(r'[A-Za-z]+-[0-9]+',newname)
		if "".join(fanhao)!='' and "".join(str)!='':
			return basename+suffixname
		if "".join(fanhao)!='':
			newname='_'.join(str)+"("+'_'.join(fanhao)+")"+suffixname
		else:
			newname='_'.join(str)+suffixname
		print(newname)
		return newname
	return newname

#修改文件夹名字  递归
def CheckDirName(path):
	basename=os.path.basename(path)
	newname=basename
	if os.path.isdir(path):
		newname= modificationname(basename,'')
	if os.path.isfile(path):
		file=os.path.splitext(basename)
		newname=modificationname(basename,file[1])
	if newname!=basename:
			newpath=os.path.dirname(path)+"/"+newname
			if not os.path.exists(newpath):
				os.rename(path,newpath)
			if os.path.isdir(path):
				checkname(newpath)
	else:
		checkname(path)

	#删除需要删除的文件夹 递归
def checkdir(path):
	basename=os.path.basename(path)
	if basename in Deletelist_Folder:
		shutil.rmtree(path)
	else:
		renameall(path)

	#是不是只有一个文件
def IsOneFile(path):
	dirbasename=os.path.basename(path)
	dirname=os.path.dirname(path)
	list=os.listdir(path)
	if len(list)==1:
		filepath=os.path.join(path,list[0])
		if os.path.isfile(filepath):
			filebasename=os.path.basename(filepath)
			file=os.path.splitext(filebasename)
			if file[0]==dirbasename:
				shutil.move(filepath,dirname+"/"+filebasename)
				#print("filepath:   "+dirname+"/"+filebasename)
	
def checkfile(path):
	basename=os.path.basename(path)
	#print(basename+"   "+str(basename in Deletelist_File))
	if basename in Deletelist_File:
		#print("  checkfile  Deletelist_File"+path)
		os.remove(path)
	file=os.path.splitext(basename)
	if file[1] in Deletelist_Type:
		os.remove(path)
		
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
		
def renameall(rootdir):
	list=os.listdir(rootdir)
	for i in range(0,len(list)):
		path=os.path.join(rootdir,list[i])
		if os.path.isfile(path):
			checkfile(path)
		if os.path.isdir(path):
			checkdir(path)
			
	
def checkname(rootdir):
	list=os.listdir(rootdir)
	for i in range(0,len(list)):
		path=os.path.join(rootdir,list[i])	
		if os.path.isdir(path):
			CheckDirName(path)

def checkonefile(rootdir):
	list=os.listdir(rootdir)
	for i in range(0,len(list)):
		path=os.path.join(rootdir,list[i])	
		if os.path.isdir(path):
			IsOneFile(path)
def cleandir(rootdir):
	list=os.listdir(rootdir)
	for i in range(0,len(list)):
		path=os.path.join(rootdir,list[i])
		if os.path.isdir(path):
			if not os.listdir(path):
				os.rmdir(path)
			else:
				cleandir(path)
			
if __name__=="__main__":
	IsTest=1
	if IsTest==1:
		rootdir="C:/Users/BugCreater/Desktop/Python/ReNameFile/新建文件夹"
	else:
		rootdir="D:/迅雷下载/已下载"
	Deletelist_File=ReadConfig("C:/Users/BugCreater/Desktop/Python/ReNameFile/Config.txt")
	renameall(rootdir)
	checkname(rootdir)
	checkonefile(rootdir)
	cleandir(rootdir)
	print("所有 完成")
	if IsTest==1:
		os.system("pause");


