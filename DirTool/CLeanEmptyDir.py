# coding: utf-8
import os  # 引入文件操作库
import time
import hashlib
import shutil
import tempfile
Deletelist_Type=[".chm",".html",".htm",".mht",".torrent",".apk",".lnk",".CHM",".sit",".db"]
ExceptFloder=["D:/ZiSyncBackup/","D:/ZiSyncBackup"]
NotMovelist_Type=[".png",".jpg",".gif",".pdf",".JPG",".py",".jpeg",".bat",".nomedia"]
KeepFile=".nomedia"
OthersDir="D:/ChromeDownLoad/视频文件/图片文件里面的视频/"


def MoveFile(path,basename):
	path1=path.lstrip().rstrip(',').replace("D:/ZiSyncBackup","")
	path2=path1.replace("/",'_')
	usename=path2.replace('\\','_')
	#print("MoveFile:  "+usename)
	os.rename(path, OthersDir+usename)
	
def checkfile(path):
	basename=os.path.basename(path)
	#print(basename)
	file=os.path.splitext(basename)
	if os.path.getsize(path) == 0 and basename!=KeepFile:
		os.remove(path)
		print("移除大小为0的文件：" + path)
	if file[1] in Deletelist_Type:
		os.remove(path)
	else:
		if not file[1] in NotMovelist_Type and basename!=KeepFile:
			#os.remove(path)
			MoveFile(path,basename)
			print("剪切文件：" + path)

def delete_dir(dir):
	if os.path.isdir(dir):
		for item in os.listdir(dir):
			if not dir in ExceptFloder:#windows下没权限删除的目录：可在此添加更多不判断的目录
				delete_dir(os.path.join(dir, item))
		if not os.listdir(dir):
			os.rmdir(dir)
			print("移除空目录：" + dir)
	else:
		checkfile(dir)

if __name__ == "__main__":  # 执行本文件则执行下述代码
	delete_dir("D:/ZiSyncBackup")