

import LogTool
import sys
import os

def GetAllMovieInfoFile(file_dir):
	L=[]
	for dirpath, dirnames, filenames in os.walk(file_dir):  
		for file in filenames :  
			if os.path.splitext(file)[1] == '.nfo':  
				L.append(os.path.join(dirpath, file))  
	return L
