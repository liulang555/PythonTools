# coding: utf-8
import os  # 引入文件操作库
import time
import hashlib
import shutil
import tempfile
Deletelist_Type=[".chm",".html",".htm",".mht",".torrent",".apk",".lnk",".CHM",".sit",".db",".swf"]
KeepFile=".nomedia"
RepeatPath=["D:/自同步","D:/MyProject/MyFile","D:/ChromeDownLoad/ImageGroup"]
NotDeletePath="D:/自同步/阅后即焚";
IsSaveDeltePath=True#False  #True  #是不是删除图片  或者保存需要删除的图片的路径 

class MD5Info:
	keySize=""
	firstPath=""
	firstMD5=""
	def __init__(self,p):
		self.firstPath = p
		self.keySize = os.path.getsize(p)
		self.firstMD5 = getmd5(self.firstPath)
		

def getmd5(file):
	if not os.path.isfile(file):  
		return  
	fd = open(file,'rb')
	md5 = hashlib.md5()
	md5.update(fd.read())
	fd.close()
	return md5.hexdigest() 

def SaveConfig(list):
	savepath="C:/Users/BugCreater/Desktop/Python/CLeanEmptyDir/NeedDeletePath.txt"
	index=0
	file=open(path,"w",encoding='utf-8')
	for values,key in list.values(),list.keys():
		file.write(index+".要删除的文件：  "+key+'\n')
		for pathstr in values:
			file.write(pathstr+'\n')
	file.close()



def DeleteRepeat(uipath):
	start = time.time()
	total_file= 0
	total_delete=0
	all_size={}
	allfile = []
	start = time.time()
	
	deletefiledic={}
	
	for curpath in uipath:
		for path,dir,filelist in os.walk(curpath ):
			for filename in filelist:
				allfile.append(os.path.join(path,filename))
	
	for cur_path in allfile:
		total_file += 1
		real_path=os.path.normpath(cur_path)
		if os.path.isfile(real_path)==True:
			md5info=MD5Info(real_path)
			if not md5info.keySize in all_size.keys():#不存在这个大小的图片
				all_size[md5info.keySize]=[]
				all_size[md5info.keySize].append(md5info)	
			else:#存在相同的size的图片  
				list=all_size[md5info.keySize]
				currepeatmd5=-1
				for index in range(len(list)):#遍历整个数组  对比md5  相同md5就判断为图片相同
					if list[index].firstMD5==md5info.firstMD5:
						currepeatmd5=index#记录相同的序号
				if currepeatmd5==-1:#不存在相同的size的图片 就存入数组
					all_size[md5info.keySize].append(md5info)
				else:
					#删除图片
					deletepath=md5info.firstPath
					if md5info.firstPath.index(NotDeletePath)>-1:#如果是优先不删除的文件夹
						deletepath=list[currepeatmd5].firstPath
						all_size[md5info.keySize][currepeatmd5]=md5info
					#记录删除的图片
					if IsSaveDeltePath:
						if not  md5info.firstMD5 in deletefiledic.keys():
							deletefiledic[md5info.firstMD5]=[]
						deletefiledic[md5info.firstMD5].append(deletepath)
					else:
						print(deletepath)
						#删除图片
						try:
							os.remove(deletepath)
						except Exception as ie:
							print ('无法删除文件-'+deletepath+"    "+str(ie))
							os.system("rd/q  "+deletepath)#调用windows的强制删除命令才搞定
						total_delete+=1
	end = time.time()
	last = end - start
	print("time: " + str(last) +"s")
	print('文件个数：'+ str(total_file))
	print('删除个数：'+ str(total_delete))
	if IsSaveDeltePath:
		SaveConfig(deletefiledic)


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
	delete_dir("D:/自同步")
	#os.remove("D:/MyProject/MyFile\\其他\\FHDのWanimal 王動官版VIP套圖 法拉利女孩＆戶外雜拍超有情調的燈條纏身啪啪 311p 1\\HiHBT#WDA001.jpg")
	#delete_dir("D:/WeGame")