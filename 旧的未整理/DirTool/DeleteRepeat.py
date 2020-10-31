# coding: utf-8
import os  # 引入文件操作库
import time
import hashlib
import shutil
import tempfile
Deletelist_Type=[".chm",".html",".htm",".mht",".torrent",".apk",".lnk",".CHM",".sit",".db",".swf"]
KeepFile=".nomedia"
RepeatPath=["D:/ZiSyncBackup","D:/MyProject/MyFile","D:/ChromeDownLoad/ImageGroup"]
NotDeletePath="D:/ZiSyncBackup";

def getmd5(file):
	if not os.path.isfile(file):  
		return  
	fd = open(file,'rb')
	md5 = hashlib.md5()
	md5.update(fd.read())
	fd.close()
	return md5.hexdigest() 

def DeleteRepeat(uipath):
	start = time.time()
	total_file= 0
	total_delete=0
	all_size={}
	allfile = []
	start = time.time()
	
	for curpath in uipath:
		for path,dir,filelist in os.walk(curpath ):
			for filename in filelist:
				allfile.append(os.path.join(path,filename))
	
	for cur_path in allfile:
		total_file += 1
		real_path=os.path.normpath(cur_path)
		#real_path = os.path.join(path,file)
		if os.path.isfile(real_path)==True:
			size = os.path.getsize(real_path)
			name_and_md5 = [real_path,'']
			if size in all_size.keys():
				new_md5 = getmd5(real_path)
				if all_size[size][1]=='':
					all_size[size][1]=getmd5(all_size[size][0])
				if new_md5 in all_size[size]:
					deletepath=real_path
					if not real_path.strip() and real_path.index(NotDeletePath)>-1:#如果是优先不删除的文件夹
						deletepath=all_size[size][0]
						all_size[size][0]=real_path
						all_size[size][1]=new_md5
					try:
						os.remove(deletepath)
					except Exception as ie:
						print ('无法删除文件-'+deletepath+"    "+str(ie))
						os.system("rd/q  "+deletepath)#调用windows的强制删除命令才搞定
					print('删除:'+deletepath)
					#CopyFileTo(deletepath,new_md5)
					#CopyFileTo(all_size[size][0],new_md5)
					total_delete+=1
				else:
					all_size[size].append(new_md5)
			else:
				all_size[size] = name_and_md5
	end = time.time()
	last = end - start
	print("time: " + str(last) +"s")
	print('文件个数：'+ str(total_file))
	print('删除个数：'+ str(total_delete))


def CopyFileTo(real_path,new_md5):
	houzui=os.path.splitext(real_path)[1]
	dirs="D:/自同步/测试删除重复/"+new_md5
	if not os.path.exists(dirs):
		os.makedirs(dirs)
	shutil.copyfile(real_path,dirs+"/"+os.path.basename(tempfile.NamedTemporaryFile().name)+houzui)

def checkfile(path):
	basename=os.path.basename(path)
	#print(basename)
	file=os.path.splitext(basename)
	if os.path.getsize(path) == 0 and basename!=KeepFile:
		os.remove(path)
		print("移除大小为0的文件：" + path)
	if file[1] in Deletelist_Type:
		os.remove(path)
		print("移除文件：" + path)
		
		
def delete_dir(dir):
	if os.path.isdir(dir):
		for item in os.listdir(dir):
			if item!='System Volume Information':#windows下没权限删除的目录：可在此添加更多不判断的目录
				delete_dir(os.path.join(dir, item))
		if not os.listdir(dir):
			os.rmdir(dir)
			print("移除空目录：" + dir)
	else:
		checkfile(dir)
		

if __name__ == "__main__":  # 执行本文件则执行下述代码
	DeleteRepeat(RepeatPath)
	delete_dir("D:/ZiSyncBackup")
	#os.remove("D:/MyProject/MyFile\\其他\\FHDのWanimal 王動官版VIP套圖 法拉利女孩＆戶外雜拍超有情調的燈條纏身啪啪 311p 1\\HiHBT#WDA001.jpg")
	#delete_dir("D:/WeGame")