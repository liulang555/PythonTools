

import LogTool
import sys
import os

def GetAllMovieInfoFile(file_dir,Debug):
	L=[]
	for filename in os.listdir(file_dir):
		if os.path.splitext(filename)[1] == '.nfo':
			Debug.Log("isnfo: "+os.path.join(file_dir,filename))
			L.append(os.path.join(file_dir,filename))
	return L
