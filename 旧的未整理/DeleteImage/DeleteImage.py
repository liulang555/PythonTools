# coding: utf-8
import os  # 引入文件操作库
import time
import hashlib
import shutil
import tempfile
Delete_Type=[".png",".jpg",".gif",".pdf",".JPG",".py",".jpeg"]

def checkfile(path):
	basename=os.path.basename(path)
	#print(basename)
	file=os.path.splitext(basename)
	if os.path.getsize(path) == 0:
		os.remove(path)
		print("移除大小为0的文件：" + path)
	if file[1] in Delete_Type:
		os.remove(path)

def delete_dir(dir):
	if os.path.isdir(dir):
		for item in os.listdir(dir):
			delete_dir(os.path.join(dir, item))
		if not os.listdir(dir):
			os.rmdir(dir)
			print("移除空目录：" + dir)
	else:
		checkfile(dir)



if __name__=="__main__":
	delete_dir("D:/迅雷下载/已下载/180401/")


