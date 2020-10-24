#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

xunlei="magnet:?xt=urn:btih:"

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
headers = { 
'Accept':'text/css,*/*;q=0.1',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'User-Agent' : user_agent ,
}
def getlink(code):
	linklist=[]
	try:
		print(code)
		url = 'https://btso.pw/search/' + code
		#print(url)
		r = requests.get(url,headers=headers,timeout=30)
		html = r.text
		#print(html)
		soup = BeautifulSoup(html,'html.parser')
		for tag in soup.find_all('div',class_='row'):
			#for gg in tag.find_all(class_='col-sm-2 col-lg-1 hidden-xs text-right size'):
				#print ("file size:  "+gg.string)
			#for aa in tag.find_all(class_='col-sm-2 col-lg-2 hidden-xs text-right date'):
				#print ("file time:  "+aa.string)
			for xx in tag.find_all(href=re.compile("https://btso.pw/magnet/detail/hash")):
				#print ("html url:  "+xx.attrs['href'])
				r1 = requests.get(xx.attrs['href'],headers=headers,timeout=30)
				html1 = r1.text
				#print (html1)
				soup1 = BeautifulSoup(html1,'html.parser')
				for tag1 in soup1.find_all('textarea',id='magnetLink'):
					#print ("get last link:  "+tag1.string)
					return tag1.string
	except Exception as e:
		print("解析失败："+e)
		return ''
					
					
def ReadConfig(path):
	list=[]
	try:
		file=open(path,"r")
	except IOError:
		print ("open file:  "+path)
	else:
		for index in file:
			line=index.strip()
			if line!="":
				list.append(line)
		file.close()
		return list;
		
def SaveConfig(path,list):
	if not os.path.exists(path):
		file=open(path,"w")
		for index in range(len(list)):
			if  list[index]!=None:
				file.write(list[index]+'\n')
		file.close()
	else:
		file=open(path,"a")
		for index in range(len(list)):
			file.write(list[index]+'\n')
		file.close()
		
def Main():
	Linkdata=ReadConfig("C:/Users/BugCreater/Desktop/Python/GetLinks/link.txt")
	HaveReadData=ReadConfig("C:/Users/BugCreater/Desktop/Python/GetLinks/SpecielCode.txt")
	ReadFailDate=[]
	ResultData=[]
	for index in range(len(Linkdata)):
		code= Linkdata[index]
		if code in HaveReadData:
			print ("it is have read already:   "+code)
		else:
			result=getlink(Linkdata[index])
			if result=='':
				ReadFailDate.append(result)
			else:
				HaveReadData.append(code)
				ResultData.append(result)
	if len(ReadFailDate)>0:
		SaveConfig("C:/Users/BugCreater/Desktop/Python/GetLinks/ReadFailDate.txt",ReadFailDate)
	SaveConfig("C:/Users/BugCreater/Desktop/Python/GetLinks/ResultData.txt",ResultData)
	SaveConfig("C:/Users/BugCreater/Desktop/Python/GetLinks/SpecielCode.txt",HaveReadData)
	print("完成！")

if __name__=="__main__":
	Main()


