import os
import sys
import ImgMarkTool
import MovieInfoTool
import LogTool

current_dir = os.path.dirname(os.path.abspath(__file__))
Debug = LogTool.Debug()
Debug.InitLogger(current_dir)

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
  #添加标签
  MovieInfoToolList = MovieInfoTool.MovieInfoToolList()
  MovieInfoToolList.ReadInfoFile(filePath,Debug)
  for markTypeValue in curlist:
      curName = ImgMarkTool.GetMarkTagNameByMarkType(markTypeValue)
      MovieInfoToolList.AddTag(curName)
  MovieInfoToolList.SaveNFO()
