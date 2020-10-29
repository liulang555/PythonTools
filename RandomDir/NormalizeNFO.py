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

deleteFolderConfigName = r"D:\\SourceTreeFloder\\PythonTools\\RandomDir\\DirList.txt"

#需要删除的文件夹路径
Deletelist_Folder = []

if __name__=="__main__":
	# Deletelist_Folder = ConfigTool.ReadConfig(sys.path[0]+ '\\' + deleteFolderConfigName)
	Deletelist_Folder = ConfigTool.ReadConfig( deleteFolderConfigName)
	dirList = []
	#开始
	num = 0
	for root in Deletelist_Folder:
		L =	DirTool.get_allfile_name(root)
		for file in L:
			num = num + 1
			Debug.Log("个数: " + str(num) + " 路径：" + file)
			# dirList.append(file)
	os.system("pause")


