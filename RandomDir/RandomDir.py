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
import random
import subprocess

deleteFolderConfigName = r"DirList.txt"
dopusrtPath = r"C:\\Program Files\\GPSoftware\\Directory Opus\\dopusrt.exe"
#参考页面
# http://127.0.0.1:36787/v12.12/index.html#!Documents/DOpusRT_Reference.htm
#需要删除的文件夹路径
Deletelist_Folder = []

if __name__=="__main__":
	Deletelist_Folder = ConfigTool.ReadConfig(sys.path[0]+ '\\' + deleteFolderConfigName)
	randomFileList = []
	#开始
	for root in Deletelist_Folder:
		L =	DirTool.get_allfile_name(root)
		for file in L:
			if file.endswith('.nfo'):
				randomFileList.append(os.path.dirname(file))
	openFile = random.sample(randomFileList, 1)
	# Debug.Log("随机路径：" + openFile[0])
	process = subprocess.Popen(
            [dopusrtPath, '/acmd','Go', openFile[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	# print(stdout)
	# print(stderr)

