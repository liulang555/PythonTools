#coding=utf-8
import sys
from tkinter import *
import os
import urllib.request
import requests
import urllib.parse
import json
import random
import hashlib
import langid

OldPath=''
ReNamelist_Folder=[]

appid = '20181125000239086'
secretKey = 'MkzYCpbC2yPu6tVHWjVs'
url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
translatestart="$"

# In Python3, use str.maketrans instead
table = {ord(f):ord(t) for f,t in zip(
	u'，。！？【】（）％＃＠＆１２３４５６７８９０',
	u',.!?[]()%#@&1234567890')}


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

#获取修改后的名字
def modificationname(basename):
	#print("modificationname--basename:    "+basename)
	newname=basename
	for index in range(len(ReNamelist_Folder)):
		if ReNamelist_Folder[index] in basename:
			newname=newname.replace(ReNamelist_Folder[index],'')
	return translateBaidu(newname)

def translateBaidu(text, f='ja', t='zh'):
	lineTuple = langid.classify(text)           #调用langid来对该行进行语言检测
	#print(lineTuple[0]+"-------"+text)
	if lineTuple[0] != "ja":
		return text
	if(text.startswith(translatestart)):
		return text
	try:
		#print ("translateBaidu:  "+text)
		salt = random.randint(32768, 65536)
		sign = appid + text + str(salt) + secretKey
		sign = hashlib.md5(sign.encode()).hexdigest()
		url = url_baidu + '?appid=' + appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
			'&salt=' + str(salt) + '&sign=' + sign
		response = urllib.request.urlopen(url)
		content = response.read().decode('utf-8')
		data = json.loads(content)
		result = str(data['trans_result'][0]['dst'])
		return translatestart+result.translate(table)
	except a:
		print("translateBaidu eorr: "+text)
	else: 
		return text
		
def ChangeName(oldpath,newpath):
	if(oldpath!=newpath):
		try:
			if not os.path.exists(newpath):
				os.rename(oldpath,newpath)
			else:
				print("已经存在了这个文件或者文件夹："+newpath+"        源文件： "+oldpath)
		except IOError as Error:
			print ("open file fail:  "+str(Error))

def Confirm():
	#print("Confirm:  "+t2.get('1.0',END))
	dir=os.path.dirname(OldPath)
	newpath=dir+"/"+t2.get('1.0',END)
	ChangeName(OldPath.strip(),newpath.strip())
	root.destroy()
	
			
if __name__=="__main__":
	OldPath = sys.argv[1]
	#print("printpath:  "+OldPath)
	#ReplaceNamePath=os.path.join(os.path.abspath('..'),"ReNameFile\ReplaceName.txt")
	#print(os.path.abspath('..'))
	#print("print ReplaceNamePath:  "+ReplaceNamePath)
	
	#print(os.getcwd()) #获取当前工作目录路径
	#print(os.path.abspath('.')) #获取当前工作目录路径
	#print(os.path.abspath('test.txt')) #获取当前目录文件下的工作目录路径
	#print(os.path.abspath('..')) #获取当前工作的父目录 ！注意是父目录路径
	#print(os.path.abspath(os.curdir)) #获取当前工作目录路径
	#env_dist = os.environ # environ是在os.py中定义的一个dict environ = {}
	#print(env_dist.get('PYTHONPATH')) # os.getenv('PYTHONPATH')
	
	ReplaceNamePath = r"D:\QQCloudSync\Python\ReNameFile\ReplaceName.txt"
	#ReplaceNamePath = r"C:\Users\BugCreater\Desktop\ReplaceName.txt"
	ReNamelist_Folder=ReadConfig(ReplaceNamePath)
	basename=os.path.basename(OldPath)
	suffixname=os.path.splitext(basename)
	newname=modificationname(suffixname[0])+suffixname[1]
	#newname=translatestart+basename
	if newname!=basename:
		root = Tk()
		root.title("翻译")
		screenwidth = root.winfo_screenwidth()  
		screenheight = root.winfo_screenheight()  
		curwidth=1200
		curheight=200
		size = '%dx%d+%d+%d' % (curwidth, curheight, (screenwidth - curwidth)/2, (screenheight - curheight)/2)  
		#print(size)  
		root.geometry(size) 
		
		t = Text(root,width=300, height=2)
		t.insert(END, basename)
		t.pack()
		
		t2 = Text(root,width=300, height=2)
		t2.insert(END, newname)
		t2.pack()
		#var = StringVar()
		#e = Entry(root,bd =10, textvariable = var)
		#var.set(basename)
		#e.pack()
	
		Button(root, text="确定", command = Confirm).pack()
		root.mainloop()
	
	
	
	


