
# 修改INFO

import xml.etree.ElementTree as ET
import LogToLocal
import sys

tagRemoveName = "tag"
tagEditorName = "genre"

Debug = LogToLocal.Debug()
Debug.InitLogger(sys.path[0])

class EditorInfo:
	def ReadInfoFile(self,path):
		if not path.endswith('.nfo') :
			Debug.Log("ReadInfoFile path is not aviliable:" + path)
			return 0
		self.tree = ET.parse(path)
		self.path = path
		self.root = self.tree.getroot()  # 使用getroot()获取根节点，得到的是一个Element对象
		self.DeleteRemoveTag()

	def AddTag(self,title):
		# 增加
		e = ET.Element(tagEditorName)
		e.text = title
		self.root.insert(2, e)
		self.tree.write(self.path,"utf-8")

	def DelteTag(self,title):
		self.DeleteRemoveTag()
		for element in self.root.findall(tagEditorName):
			if element.text == title :
				self.root.remove(element)
				Debug.Log("DelteTag success " + title)

	def DeleteRemoveTag(self):
		for element in self.root.findall(tagRemoveName):
			Debug.Log("DeleteRemoveTag remove tag:" + element.text)
			self.root.remove(element)
	def GetAllTags(self):
		list = []
		for element in self.root.findall(tagEditorName):
			list.append(element.text)
		return list
