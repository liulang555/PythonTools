# coding: utf-8
import os  # 引入文件操作库
import time
import hashlib
import shutil
import tempfile
import xml.etree.ElementTree as ET

Deletelist_Folder=["D:\媒体库\输出目录","E:\媒体库\输出目录"]
# Deletelist_Folder=["D:\QQCloudSync\Python\EditorNFO"]
#需要删除的标签 数组
DeleteConfig = []
#需要改名的标签 字典
ChangeConfigDic = {}

def ReadConfig(path):
	list=[]
	try:
		file = open(path,"rb")#选用rb  防止读取文件出错
		#filereader=file.decode("utf-8")
	except IOError:
		print ("open file fail:  "+path)
	else:
		for index in file:
			linetemp = index.decode("utf-8").strip()
			#去掉字符串中的 \ufeff
			line = linetemp.encode('utf-8').decode('utf-8-sig')
			if line!="":
				#print(line)
				list.append(line)
		file.close()
		return list;	

#编辑标签
#删除不要的
#修改不合适的名字
def EidtorTag(path):
	# 打开xml文档
	tree = ET.parse(path)
	root = tree.getroot()  # 使用getroot()获取根节点，得到的是一个Element对象
	#读取
	for element in root.findall('genre'):
		text = element.text   # 访问Element文本
		# print("读取 " + text)
		if text in DeleteConfig:
			# print("删除： "+text)
			root.remove(element)
		if text in ChangeConfigDic:
			# print("改名： "+text)
			element.text = ChangeConfigDic[text]
	#所有tag标签默认都删除
	for element in root.findall('tag'):
		root.remove(element)
	#保存修改   因为权限的问题  直接先删除，再保存
	os.remove(path)
	tree.write(path,"utf-8")   

def get_allfile_name(file_dir):   
    L=[]   
    for dirpath, dirnames, filenames in os.walk(file_dir):  
        for file in filenames :  
            if os.path.splitext(file)[1] == '.nfo':  
                L.append(os.path.join(dirpath, file))  
    return L 



if __name__=="__main__":
	import sys
	DeleteConfig = ReadConfig("D:\QQCloudSync\Python\EditorNFO\DeleteConfig.txt")
	ChangeConfig = ReadConfig("D:\QQCloudSync\Python\EditorNFO\ChangeConfig.txt")
	for linestr in ChangeConfig:
		splitlist = linestr.split("——", 1)
		# print(splitlist[0])
		# print(splitlist[1])
		ChangeConfigDic[splitlist[0]] = splitlist[1]
	for key in ChangeConfigDic:
		if key in DeleteConfig:
			DeleteConfig.remove(key)
	#打印
	for key in ChangeConfigDic:
		print("改名: " + key + "  到：" + ChangeConfigDic[key])
	for	linestr in DeleteConfig:
		print("删除: "+ linestr)
	#开始
	num = 0
	for root in Deletelist_Folder:
		L =	get_allfile_name(root)
		for file in L:
			num = num + 1
			print("个数: " + str(num) + " 路径：" + file)
			EidtorTag(file)	
	os.system("pause")


