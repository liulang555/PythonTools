import os
import sys
import ImgAddMark
import EditorMovieInfo
import LogToLocal

uncensoredName = r"/UNCENSORED.png"   #无码
subName = r"/SUB.png"   #字幕

thumb_end =  '-thumb.jpg'
poster_end = '-poster.jpg'
nfo_end = '.nfo'


if __name__=="__main__":
  # 当前文件的绝对路径
  current_dir = os.path.dirname(os.path.abspath(__file__))

  uncensoredPath = current_dir + uncensoredName
  subPath = current_dir + subName

  Debug = LogToLocal.Debug()
  Debug.InitLogger(current_dir)

  filePath = sys.argv[1]
  Debug.Log(filePath)

  cn_sub = 0
  uncensored = 0
  if len(sys.argv) == 4 :
    if sys.argv[2] == '1':
      uncensored = 1
      Debug.Log("无码")
    if sys.argv[3] == '1':
      cn_sub = 1
      Debug.Log("字幕")

  filenames = os.listdir(filePath)
  for filename in filenames:
    if filename.endswith(thumb_end):
      if uncensored == 1:
        ImgAddMark.AddMarkToPic(os.path.join(filePath,filename),ImgAddMark.MarkPos.LeftTop,uncensoredPath)
      if cn_sub == 1:
        ImgAddMark.AddMarkToPic(os.path.join(filePath,filename),ImgAddMark.MarkPos.RightTop,subPath)
    if filename.endswith(poster_end):
      if uncensored == 1:
        ImgAddMark.AddMarkToPic(os.path.join(filePath,filename),ImgAddMark.MarkPos.LeftTop,uncensoredPath)
      if cn_sub == 1:
        ImgAddMark.AddMarkToPic(os.path.join(filePath,filename),ImgAddMark.MarkPos.RightTop,subPath)
    if filename.endswith(nfo_end):
      if uncensored == 1:
        EditorMovieInfo.AddTag(os.path.join(filePath,filename),"无码")
      if cn_sub == 1:
        EditorMovieInfo.AddTag(os.path.join(filePath,filename),"字幕")


  # os.system("pause")
  # ImgAddMark.AddMarkToPic("D:\SourceTreeFloder\PythonTools\AddMarkToImg\SVS-033-thumb.jpg",ImgAddMark.MarkPos.LeftTop,uncensoredPath)