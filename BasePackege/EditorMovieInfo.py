
# 修改INFO

import xml.etree.ElementTree as ET

def AddTag(path,title):
	# 打开xml文档
	tree = ET.parse(path)
	root = tree.getroot()  # 使用getroot()获取根节点，得到的是一个Element对象
	# 增加
	e = ET.Element('genre')
	e.text = title
	root.insert(2, e)
	tree.write(path,"utf-8")