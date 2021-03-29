# coding: utf-8
import os  # 引入文件操作库
import sys
import time
import ConfigTool
import DirTool
import LogTool
import MovieInfoTool
import random
import DirectoryOpusTool

deleteFolderConfigName = r"随机的文件夹路径.txt"
HaveRandomFolderConfigName = r"已随机路径.txt"

#需要删除的文件夹路径
Deletelist_Folder = []
HaveRandomlist_Folder = []

def IsHaveRandom(str):
	if str == '':
		return True
	if str in HaveRandomlist_Folder:
		return True
	return False

if __name__=="__main__":
	Deletelist_Folder = ConfigTool.ReadConfigByTxtName(deleteFolderConfigName)
	HaveRandomlist_Folder = ConfigTool.ReadConfigByTxtName(HaveRandomFolderConfigName)
	randomFileList = []
	#开始
	for root in Deletelist_Folder:
		L =	DirTool.get_allfile_name(root)
		for file in L:
			if file.endswith('.nfo'):
				if file not in randomFileList:
					randomFileList.append(os.path.dirname(file))
	openFile = ''			
	while (IsHaveRandom(openFile)):
		openFile = random.sample(randomFileList, 1)
	#Debug.Log("随机路径：" + openFile[0])
	ConfigTool.SaveConfigToEnd(HaveRandomFolderConfigName,openFile[0])
	DirectoryOpusTool.OpenDirByOpenWindow(openFile[0])

