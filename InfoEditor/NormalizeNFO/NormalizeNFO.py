# coding: utf-8
import os  # 引入文件操作库
import sys
import time
import hashlib
import shutil
import tempfile
import xml.etree.ElementTree as ET
import ConfigTool
import DirTool
import LogTool
import MovieInfoTool

current_dir = os.path.dirname(os.path.abspath(__file__))
Debug = LogTool.Debug()
Debug.InitLogger(current_dir)


deleteFolderConfigName = r"规范标签--文件夹.txt"
deleteTagConfigName = r"规范标签--删除.txt"
changeTagConfigName = r"规范标签---替换.txt"

#需要删除的文件夹路径
Deletelist_Folder=[]
#需要删除的标签 数组
DeleteConfig = []
#需要改名的标签 字典
ChangeConfigDic = {}

if __name__=="__main__":
	Deletelist_Folder = ConfigTool.ReadConfigByTxtName(deleteFolderConfigName)
	DeleteConfig = ConfigTool.ReadConfigByTxtName(deleteTagConfigName)
	ChangeConfig = ConfigTool.ReadConfigByTxtName(changeTagConfigName)
	for linestr in ChangeConfig:
		splitlist = linestr.split("——", 1)
		# Debug.Log(splitlist[0])
		# Debug.Log(splitlist[1])
		ChangeConfigDic[splitlist[0]] = splitlist[1]
	for key in ChangeConfigDic:
		if key in DeleteConfig:
			DeleteConfig.remove(key)
	#打印
	for key in ChangeConfigDic:
		Debug.Log("改名: " + key + "  到：" + ChangeConfigDic[key])
	for	linestr in DeleteConfig:
		Debug.Log("删除: "+ linestr)
	#开始
	num = 0
	for root in Deletelist_Folder:
		L =	DirTool.get_allfile_name(root)
		for file in L:
			num = num + 1
			Debug.Log("个数: " + str(num) + " 路径：" + file)
			item = MovieInfoTool.MovieInfoTool()
			item.ReadInfoFile(file,Debug)
			item.NormalizeNFO(DeleteConfig,ChangeConfigDic)
	os.system("pause")


