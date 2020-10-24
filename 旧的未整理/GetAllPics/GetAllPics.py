#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import random
import urllib.request
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
header = { 
'Accept':'text/css,*/*;q=0.1',
'Accept-Encoding':'gzip',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'User-Agent' : user_agent ,
}
SavePaht="E:/MyProject/PythonDown/"
#下载一个图片
def DownLoadOneImage(imgPath,savepath):
	try:
		#if not os.path.exists(savepath):
		f = open(savepath, 'wb')
		f.write((urllib.request.urlopen(imgPath)).read())
		f.close()
		#print("DownLoadOneImage finish:   "+imgPath)
	#else:
		#print("DownLoadOneImage IsAlreadyExists:   "+imgPath)
	except Exception as e:
		print("DownLoadOneImage error："+imgPath+"   Exception:   ",e)
	time.sleep(random.choice(range(2,5)))


#获取网页内容		
def GetHtmlText(url):
	#print(url)
	timeout=random.choice(range(80,120))
	while True:
		try:
			response=requests.get(url,headers=header,timeout=timeout)
			response.encoding='gb2312'
			break
		except socket.timeout as e:
			print('GetHtmlText failur 3:',e)
			time.sleep(random.choice(range(8,15)))

		except socket.error as e:
			print('GetHtmlText failur 4:',e)
			time.sleep(random.choice(range(20,60)))

		except http.client.BadStatusLine as e:
			print('GetHtmlText failur 5:',e)
			time.sleep(random.choice(range(30,80)))

		except http.client.IncompleteRead as e:
			print('GetHtmlText failur 6:',e)
			time.sleep(random.choice(range(5,15)))
	#print(response.text)
	return response.text
#获取所有图片链接
def GetAllImageUrl(html,imglist,imglastname):
	for link,t in set(re.findall(r'([http|https]:[^\s]*?(jpg|png|gif))', html)):
		if link.startswith('s'):
			link='http'+link
		else:
			link='htt'+link
		#print(link)
		if link not in imglist:
			imglist.append(link)
			imglastname.append('.'+t)
#获取标题
def GetAllTitleName(html):
	soup = BeautifulSoup(html,'html.parser')
	folder_name = soup.select('h4')[0].text
	#folder_name.replace("","")
	folder_name.replace(':', '@').replace('/', '_')
	return folder_name
	
#读取并下载所有图片
def GetAllImage(url):
	html = GetHtmlText(url)
	folder_name=GetAllTitleName(html)
	imglist=[]
	imglastname=[]
	GetAllImageUrl(html,imglist,imglastname)
	print(folder_name+"    "+str(len(imglist)))
	folderpath=SavePaht+folder_name
	if not os.path.exists(folderpath):
		os.makedirs(folderpath)
	for index in range(len(imglist)):
		DownLoadOneImage(imglist[index],folderpath+"/"+folder_name+str(index)+imglastname[index])
		time.sleep(random.choice(range(2,5)))
	
#读取配置文件	
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
def Main():
	Urllist=ReadConfig("C:/Users/BugCreater/Desktop/Python/GetAllPics/links.txt")
	p = Pool(len(Urllist))
	for index in range(len(Urllist)):
		p.apply_async(GetAllImage, args=(Urllist[index],))
		#GetAllImage(Urllist[index])
	p.close()
	p.join()
	
	print("完成！")

if __name__=="__main__":
	Main()


