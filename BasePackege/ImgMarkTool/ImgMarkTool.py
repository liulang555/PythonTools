# 图片加水印
#参考
# https://github.com/moyy996/AVDC
# https://github.com/moyy996/AVDC/blob/master/AVDC_Main.py
# AVDC_Main.py   1304行  add_mark函数

from PIL import Image
from enum import Enum
import os

#水印的位置
class MarkPos(Enum):
    LeftTop = 0
    RightTop = 1
    RightBottom = 2
    LeftBottom = 3

# 水印的类型
class MarkType(Enum):
    noneMark = 0 #没有标签
    uncensored = 1 #无码
    cn_sub = 2 #字幕


horizontalSlider_mark_size = 5  #水印大小
thumb_end =  '-thumb.jpg'
poster_end = '-poster.jpg'
fanart_end = '-fanart.jpg'

uncensoredName = r"/UNCENSORED.png"   #无码
subName = r"/SUB.png"   #字幕
current_dir = os.path.dirname(os.path.abspath(__file__))
uncensoredPath = current_dir + uncensoredName
subPath = current_dir + subName

def AddMark(filePath,sortlist):
    sortlist.sort()
    filenames = os.listdir(filePath)
    for filename in filenames:
        if filename.endswith(thumb_end):
            curFilePath = os.path.join(filePath,filename)
            judgeTypeToPic(curFilePath,sortlist)
        if filename.endswith(poster_end):
            curFilePath = os.path.join(filePath,filename)
            judgeTypeToPic(curFilePath,sortlist)

def judgeTypeToPic(curFilePath,sortlist):
    # 从 MarkType 类型最小值开始循环，第一个就是左上角，第二个就是右上角
    for index in range(len(sortlist)):
        if MarkType(sortlist[index]) == MarkType.uncensored:
            AddMarkToOnePic(curFilePath,MarkPos(index),uncensoredPath)
        if MarkType(sortlist[index]) == MarkType.cn_sub:
            AddMarkToOnePic(curFilePath,MarkPos(index),subPath)

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
