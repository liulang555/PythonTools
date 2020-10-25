# 图片加水印
#参考
# https://github.com/moyy996/AVDC
# https://github.com/moyy996/AVDC/blob/master/AVDC_Main.py
# AVDC_Main.py   1304行  add_mark函数

from PIL import Image
from enum import Enum
import os

#水印的位置（和MarkType(Enum)一一对应）
class MarkPos(Enum):
    LeftTop = 0
    RightTop = 1
    RightBottom = 2
    LeftBottom = 3

# 水印的类型 （增加需要一并增加图片（MarkIconName）和路径（MarkIconPath））
class MarkType(Enum):
    uncensored = 0 #无码
    cn_sub = 1 #字幕

#需要修改的图片列表  直接加就可以
MarkImgEndList = ['-thumb.jpg','-poster.jpg','-fanart.jpg']

MarkTagName = [r"无码",r"字幕"]  #和 MarkType(Enum) 对应
MarkIconName = [r"/UNCENSORED.png",r"/SUB.png"]  #和 MarkType(Enum) 对应
MarkIconPath = [] #和 MarkType(Enum) 对应
current_dir = os.path.dirname(os.path.abspath(__file__))
MarkIconPath.append(current_dir + MarkIconName[MarkType.uncensored.value]) #和 MarkType(Enum) 对应
MarkIconPath.append(current_dir + MarkIconName[MarkType.cn_sub.value]) #和 MarkType(Enum) 对应

horizontalSlider_mark_size = 5  #水印大小

#通过marktype 获取中文标签名字
def GetMarkTagNameByMarkType(markTypeValue):
    return MarkTagName[markTypeValue]

#通过标签列表添加水印
def AddMarkBytagList(filePath,tagList):
    sortlist = []
    for tag in tagList:
        for index in range(len(MarkTagName)):
            if MarkTagName[index] == tag:
                sortlist.append(index)
    AddMark(filePath,sortlist)

def AddMark(filePath,sortlist):
    if len(sortlist) <= 0:
        return 0
    sortlist.sort()
    filenames = os.listdir(filePath)
    for filename in filenames:
        for iconEnd in MarkImgEndList:
            if filename.endswith(iconEnd): #每个图片都是一个逻辑
                curFilePath = os.path.join(filePath,filename)
                judgeTypeToPic(curFilePath,sortlist)

def judgeTypeToPic(curFilePath,sortlist):
    # 从 MarkType 类型最小值开始循环，第一个就是左上角，第二个就是右上角
    for index in range(len(sortlist)):
        AddMarkToOnePic(curFilePath,MarkPos(index),MarkIconPath[sortlist[index]])

def AddMarkToOnePic(picSourcePath, markPos, mark_pic_path):
	#需要加水印的图片
	img_pic = Image.open(picSourcePath)
	# 水印大小的值
	size = 14 - horizontalSlider_mark_size  

	img_subt = Image.open(mark_pic_path)
	scroll_high = int(img_pic.height / size)
	scroll_wide = int(scroll_high * img_subt.width / img_subt.height)
	img_subt = img_subt.resize((scroll_wide, scroll_high), Image.ANTIALIAS)
	r, g, b, a = img_subt.split()  # 获取颜色通道，保持png的透明性
	# 封面四个角的位置
	pos = [
		{'x': 0, 'y': 0},
		{'x': img_pic.width - scroll_wide, 'y': 0},
		{'x': img_pic.width - scroll_wide, 'y': img_pic.height - scroll_high},
		{'x': 0, 'y': img_pic.height - scroll_high},
	]
	img_pic.paste(img_subt, (pos[markPos.value]['x'], pos[markPos.value]['y']), mask=a)
	img_pic.save(picSourcePath, quality = 95)
	img_pic.close()





























# ========================================================================加水印

def add_mark_thread(pic_path, cn_sub, uncensored):
  size = 14 - horizontalSlider_mark_size  # 获取自定义大小的值
  img_pic = Image.open(pic_path)
  count = 0  # 获取自定义位置，取余配合pos达到顺时针添加的效果
  if uncensored == 1:
      add_to_pic(pic_path, img_pic, size, count, 3)
      count = (count + 1) % 4
  if cn_sub == 1:
      add_to_pic(pic_path, img_pic, size, count, 1)  # 添加
  img_pic.close()

def add_to_pic(pic_path, img_pic, size, count, mode):
  mark_pic_path = ''
  if mode == 1:
      mark_pic_path = RootDir + SUB
  elif mode == 2:
      mark_pic_path = RootDir + LEAK
  elif mode == 3:
      mark_pic_path = RootDir + UNCENSORED
      
  img_subt = Image.open(mark_pic_path)
  scroll_high = int(img_pic.height / size)
  scroll_wide = int(scroll_high * img_subt.width / img_subt.height)
  img_subt = img_subt.resize((scroll_wide, scroll_high), Image.ANTIALIAS)
  r, g, b, a = img_subt.split()  # 获取颜色通道，保持png的透明性
  # 封面四个角的位置
  pos = [
      {'x': 0, 'y': 0},
      {'x': img_pic.width - scroll_wide, 'y': 0},
      {'x': img_pic.width - scroll_wide, 'y': img_pic.height - scroll_high},
      {'x': 0, 'y': img_pic.height - scroll_high},
  ]
  img_pic.paste(img_subt, (pos[count]['x'], pos[count]['y']), mask=a)
  img_pic.save(pic_path, quality = 95)

# ========================================================================获取分集序号
