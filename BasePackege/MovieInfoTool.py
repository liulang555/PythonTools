
# 修改INFO

import xml.etree.ElementTree as ET
import LogTool
import sys

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
		self.tree.write(self.path,"utf-8")
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
