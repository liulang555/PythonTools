

import subprocess
import sys
import os

#参考页面
# http://127.0.0.1:36787/v12.12/index.html#!Documents/DOpusRT_Reference.htm
dopusrtPath = r"C:\\Program Files\\GPSoftware\\Directory Opus\\dopusrt.exe"

#打开一个文件夹  如果当前有已经打开的文件窗口，就复用这个窗口
def OpenDirByOpenWindow(file_dir):
    process = subprocess.Popen(
        [dopusrtPath, '/acmd','Go', file_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()
    # stdout, stderr = process.communicate()
    # print(stdout)
    # print(stderr)
