
# 修改INFO

import xml.etree.ElementTree as ET
import LogTool
import sys
import os

tagElement_tag = "tag"
tagElement_genre = "genre"

class MovieInfoTool:
	def ReadInfoFile(self,path,debug):
		self.Debug = debug
		if not path.endswith('.nfo') :
			self.Debug.Log("ReadInfoFile path is not aviliable:" + path)
			return 0
		self.tree = ET.parse(path)
		self.path = path
		self.root = self.tree.getroot()  # 使用getroot()获取根节点，得到的是一个Element对象
		self.DeleteRemoveAllTag(tagElement_tag)

	def SaveAllTag(self,list):
		self.DeleteRemoveAllTag(tagElement_tag)
		self.DeleteRemoveAllTag(tagElement_genre)
		for tag in list:
			self.AddTag(tag)
		self.SaveNFO()
	def AddTag(self,title):
		# 增加
		e = ET.Element(tagElement_genre)
		e.text = title
		self.root.insert(2, e)

	def DelteTag(self,title):
		self.DeleteRemoveAllTag(tagElement_tag)
		for element in self.root.findall(tagElement_genre):
			if element.text == title :
				self.root.remove(element)
				self.Debug.Log("DelteTag success " + title)

	def DeleteRemoveAllTag(self,removeName):
		for element in self.root.findall(removeName):
			self.Debug.Log("DeleteRemoveAllTag remove tag:" + element.text)
			self.root.remove(element)
	def GetAllTags(self):
		list = []
		for element in self.root.findall(tagElement_genre):
			list.append(element.text)
		return list
	def SaveNFO(self):
		#保存修改   因为权限的问题  直接先删除，再保存
		os.remove(self.path)
		self.tree.write(self.path,"utf-8")
	#编辑标签
	#删除不要的
	#修改不合适的名字
	def NormalizeNFO(self,DeleteConfig,ChangeConfigDic):
		for element in self.root.findall(tagElement_genre):
			text = element.text   # 访问Element文本
			# print("读取 " + text)
			if text in DeleteConfig:
				# print("删除： "+text)
				self.root.remove(element)
			if text in ChangeConfigDic:
				# print("改名： "+text)
				element.text = ChangeConfigDic[text]
		self.SaveNFO()
