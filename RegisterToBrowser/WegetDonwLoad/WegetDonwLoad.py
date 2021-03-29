#!/usr/bin/python
# -*- coding: utf-8 -*-
import os  
import sys  
import subprocess
import chardet
import re
from urllib import parse

ConstPathStr = '?path='
ConstOutPathStr = '&out='
DownLoadPath = "D:\\MyDownLoad\\WeGetDownLoad\\"

# IDM下载方式
IDMPath = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"

# weget 版本使用方式  下载太慢废弃
# WeGetPath = "D:\\GreenSoftWare\\SoftWare\\wget-1.20.3-win64\\wget.exe"
# UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63"
# cookieTxt = "D:\\SourceTreeFloder\\PythonTools\\RegisterToBrowser\\WegetDonwLoad\\pornhub.com_cookies.txt"
# proxyStr = '-e https_proxy=http://127.0.0.1:10809'

# process = subprocess.Popen(
# 		# [WeGetPath,'-d','-Q500m','-c','-b','-nc','-O' + FinalOutPath, FinalDownLoadPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 		# [WeGetPath,'-d','-Q500m','-c','-nc','--load-cookies='+cookieTxt,'-O' + FinalOutPath,'-U'+ UserAgent , FinalDownLoadPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 		# [WeGetPath,'-d','-Q500m','-c','--load-cookies='+cookieTxt,'-e http_proxy=http://127.0.0.1:10809','-O' + FinalOutPath,'-U'+ UserAgent , FinalDownLoadPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 		[WeGetPath,'-d','-Q500m','-c','-nc','--load-cookies='+cookieTxt,proxyStr,'-O' + FinalOutPath,'-U'+ UserAgent , FinalDownLoadPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 	stdout, stderr = process.communicate()
# 	print(stdout)
# 	print(stderr)

if __name__=="__main__":
	paramString = sys.argv[1]
	
	pathStartIndex = paramString.find(ConstPathStr)
	outStartIndex = paramString.find(ConstOutPathStr)

	FinalDownLoadPath = paramString[pathStartIndex + len(ConstPathStr) :outStartIndex]
	OutPathStr = paramString[outStartIndex + len(ConstOutPathStr):]
	path = parse.unquote(OutPathStr)
	fileName = re.sub('[\/:*?"<>|]','-',path)#去掉非法字符
	FinalOutPath = DownLoadPath +  fileName
	print(FinalOutPath)
	if os.path.exists(FinalOutPath):
		if os.path.getsize(FinalOutPath) <= 0:
			os.remove(FinalOutPath)

	process = subprocess.Popen(
		[IDMPath,'/d',FinalDownLoadPath,'/p',DownLoadPath,'/f', fileName,'/q', '/n'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	print(stdout)
	print(stderr)
	
