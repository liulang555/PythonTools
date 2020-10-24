import os
import sys
import ImgMarkTool

if __name__=="__main__":
  # 当前文件的绝对路径
  filePath = sys.argv[1]
  curlist = []
  if len(sys.argv) == 4 :
    if sys.argv[2] == '1':
      curlist.append(ImgMarkTool.MarkType.uncensored.value)
    if sys.argv[3] == '1':
      curlist.append(ImgMarkTool.MarkType.cn_sub.value)
  ImgMarkTool.AddMark(filePath,curlist)
    # if filename.endswith(nfo_end):
    #   if uncensored == 1:
    #     EditorMovieInfo.AddTag(os.path.join(filePath,filename),"无码")
    #   if cn_sub == 1:
    #     EditorMovieInfo.AddTag(os.path.join(filePath,filename),"字幕")
