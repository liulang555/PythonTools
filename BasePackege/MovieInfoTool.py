# 修改INFO
import xml.etree.ElementTree as ET
import LogTool
import DirTool
import sys
import os
import TranslateTool

tagElement_tag = "tag"
tagElement_genre = "genre"
tagElement_title = "title"

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

	def SaveAllTag(self,List):
		self.DeleteRemoveAllTag(tagElement_tag)
		self.DeleteRemoveAllTag(tagElement_genre)
		for tag in List:
			self.AddTag(tag)
		self.SaveNFO()
	def AddTag(self,title):
		for element in self.root.findall(tagElement_genre):
			if element.text == title :
				return 0 #已经有了
		# 增加
		e = ET.Element(tagElement_genre)
		e.tail = "\n  "  #美化操作   增加换行和空格
		e.text = title
		self.root.insert(8, e)  #从第8个开始插入，和原先的放一起

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
		List = []
		for element in self.root.findall(tagElement_genre):
			List.append(element.text)
		return List
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
	def TranslateToChinese(self):
		for element in self.root.findall(tagElement_title):
			curstr = element.text
			# curstr = r"ウエディングドレスで初生挿入"
			self.Debug.Log("读取标题: "+curstr)
			translateStr = TranslateTool.baiduAPI_translate_main(curstr)
			if translateStr == None:
				self.Debug.Log("翻译失败: "+ curstr)
			else:
				self.Debug.Log("翻译成功: "+translateStr)
				element.text = translateStr
				self.SaveNFO()

# 读取一个文件夹中所有NFO文件
class MovieInfoToolList:
	def ReadInfoFile(self,path,debug):
		self.Debug = debug
		self.List = []
		InfoFileList = DirTool.GetAllMovieInfoFile(path,self.Debug)
		for file in InfoFileList:
			self.Debug.Log("InfoFileList: " + file)
			item = MovieInfoTool()
			item.ReadInfoFile(file,self.Debug)
			self.List.append(item)
	def GetAllTags(self):
		if len(self.List) >= 1:
			return self.List[0].GetAllTags()
		else:
			return []
	def SaveAllTag(self,curlist):
		for item in self.List:
			item.SaveAllTag(curlist)
	def AddTag(self,title):
		for item in self.List:
			item.AddTag(title)
	def SaveNFO(self):
		for item in self.List:
			item.SaveNFO()