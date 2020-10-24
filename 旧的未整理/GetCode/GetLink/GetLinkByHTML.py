#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

sensitive=['看片','快播','会所','性','色中色']
result=[]
def getnames(path):
	file=open(path)
	source=file.read()
	file.close()
	fanhao=[]
	fanhao=re.findall(r'^(magnet:\?xt=urn:btih:)[0-9a-fA-F]{40}.*$',source)
	for	index in range(len(fanhao)):
		print(fanhao[index])
		code=fanhao[index]
		result.append(code)
		
def SaveConfig(path,list):
	if not os.path.exists(path):
		file=open(path,"w",encoding='utf-8')
		for index in range(len(list)):
			file.write(list[index]+'\n')
		file.close()
	else:
		file=open(path,"a")
		for index in range(len(list)):
			file.write(list[index]+'\n')
		file.close()
		
def Main():
	rootdir="C:/Users/BugCreater/Desktop/Python/GetCode/GetLink"
	list=os.listdir(rootdir)
	for i in range(0,len(list)):
		path=os.path.join(rootdir,list[i])
		if os.path.isfile(path):
			if os.path.splitext(path)[1] == '.mhtml':
				print(os.path.basename(path))
				result.append(os.path.basename(path))
				getnames(path)
	SaveConfig(rootdir+"/result.txt",result)
	print("完成！")

if __name__=="__main__":
	Main()


