#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs= True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()


result=[]
def getnames(path):
	file=open(path)
	source=file.read()
	file.close()
	stripsource=strip_tags(source)
	fanhao=[]
	fanhao=re.findall(r'[A-Za-z]+-[0-9]+',stripsource)
	for	index in range(len(fanhao)):
		#print(fanhao[index])
		code=fanhao[index]
		if not code=='utf-8':
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

pattern1 = re.compile('[A-Za-z]+-[0-9]+')# 普通番号的正则
pattern2 = re.compile('[A-Za-z0-9]+')
def Main():
	rootdir="C:/Users/BugCreater/Desktop/Python/GetCode"
	list=os.listdir(rootdir)
	for i in range(0,len(list)):
		path=os.path.join(rootdir,list[i])
		if os.path.isfile(path):
			if os.path.splitext(path)[1] == ".mhtml":
				print(os.path.basename(path))
				result.append(os.path.basename(path))
				getnames(path)
	SaveConfig("C:/Users/BugCreater/Desktop/Python/GetCode/link.txt",result)
	print("完成！")

if __name__=="__main__":
	Main()


