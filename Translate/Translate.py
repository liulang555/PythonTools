# coding: utf-8
import os  # 引入文件操作库
import sys
import LogTool
import MovieInfoTool

current_dir = os.path.dirname(os.path.abspath(__file__))
Debug = LogTool.Debug()
Debug.InitLogger(current_dir)

if __name__=="__main__":
	curpath = "D:\\媒体库\\输出目录\\#Akina（アキナ）\\FC2-796722.nfo"
	#添加标签
	curMovieInfoTool = MovieInfoTool.MovieInfoTool()
	curMovieInfoTool.ReadInfoFile(curpath,Debug)
	curMovieInfoTool.TranslateToChinese()
	curMovieInfoTool.SaveNFO()
