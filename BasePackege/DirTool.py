

import LogTool
import sys
import os

#当前文件夹中文件，不遍历子文件夹
def GetAllMovieInfoFile(file_dir,Debug):
	L=[]
	for filename in os.listdir(file_dir):
		if os.path.splitext(filename)[1] == '.nfo':
			Debug.Log("isnfo: "+os.path.join(file_dir,filename))
			L.append(os.path.join(file_dir,filename))
	return L
#当前目录中文件，递归遍历所有文件夹
def get_allfile_name(file_dir):
    L=[]
    for dirpath, dirnames, filenames in os.walk(file_dir):
        for file in filenames :
            if os.path.splitext(file)[1] == '.nfo':
                L.append(os.path.join(dirpath, file))
    return L
