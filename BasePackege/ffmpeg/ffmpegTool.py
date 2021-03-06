# coding=utf-8
import subprocess
import re
import os
from decimal import Decimal
import math
import sys
import LogTool
# python -m pip install pypiwin32    安装方式，使用cmd执行这句
from win32com.shell import shell, shellcon

#系统属性
CREATE_NO_WINDOW = 0x08000000
#ffmpeg exe名字
ffmpegName = 'ffmpeg'
#获取当前文件的绝对路径
abs_file = __file__
#分割字符串找到文件夹路径
abs_dir = abs_file[:abs_file.rfind("\\")]
#拼接成ffmpeg 路径
ffmpegPath = abs_dir + '\\' + ffmpegName
MergeFileListName = r"\\filelist.txt"
#可以剪切生产的视频个数
CDMaxNum = 100

Debug = LogTool.Debug()
Debug.InitLogger(sys.path[0])

class ffmpegTool:
    #剪切视频
    def CutMovie(self, path, starttime, endtime, isReplace):
        # 日志还是打印到调用方的文件夹中
        # self.Debug = LogToLocal.Debug()
        # self.Debug.InitLogger(sys.path[0])

        # 创建新的生成的.mp4文件路径
        newFile = self.GetNewFileName(path)
        Debug.Log('newFile: '+newFile)
        startcut = self.GetStartTime(starttime)
        endcut = self.GetStartTime(endtime)
        videoInfo = self.get_video_length(path,ffmpegPath)  # 视频信息获取 为一tuple
        # Debug.Log(videoInfo)
        duration = videoInfo[0]  # 时长 秒
        # 毫秒更精确 6秒
        startPoint = self.millisecToAssFormat(startcut)  # 毫秒更精确 6秒
        # 毫秒更精确 13.5秒 #duration*1000-endcut*1000 #毫秒更精确 13.5秒
        endPoint = self.millisecToAssFormat(duration*1000-endcut-startcut)
        Debug.Log('*'*50)
        Debug.Log("startPoint:  "+startPoint+"     endPoint:"+endPoint)
        # self.cutVideo(startPoint,endPoint,path,newFile)
        retcode = self.cutVideo(startPoint, endPoint, path, newFile,ffmpegPath)
        Debug.Log(retcode)
		# 如果需要删除源文件
        if retcode == 1 and isReplace == True:
            # os.remove(path)
			# 删除到回收站
            self.deltorecyclebin(path)
            curpath = path
			# 去掉源文件中的-CD1  -CD2等文字
            for num in range(1, CDMaxNum):
                curpath = curpath.replace('-CD'+str(num), '')
            Debug.Log('replace name'+curpath)
            os.rename(newFile, curpath)
        # return retcode
        return 1

    # 获取一个未曾创建的名字
    def GetNewFileName(self, path):
        curpath = path
        for num in range(1, CDMaxNum):
            curpath = curpath.replace('-CD'+str(num), '')
        # Debug.Log("ffmpegMod GetNewFileName curpath"+curpath)
        # Debug.Log("ffmpegMod GetNewFileName curpath[:-4]"+curpath[:-4])
        basename = os.path.basename(path)
        file = os.path.splitext(basename)
        for num in range(1, CDMaxNum):
            # curpath[:-4]  是去掉最后四个字符(.mp4)的全路径
            #  curpath       D:\媒体库\101520-001.mp4
            #  curpath[:-4]  D:\媒体库\101520-001
            newFile = curpath[:-4]+'-CD'+str(num)+file[1]
            if not os.path.exists(newFile):
                return newFile

    # 获取视频的 duration 时长 长 宽
    def get_video_length(self, path,ffmpegPath):
        Debug.Log('ffmpegMod get_video_length start ')
        process = subprocess.Popen(
            [ffmpegPath, '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        Debug.Log('stdout')
        Debug.Log(stdout)
        pattern_duration = re.compile(
            "Duration:\s{1}(\d+?):(\d+?):(\d+\.\d+?),")
        # ",\s{1}(\d+?)x(\d+?)\s{1}\["
        pattern_size = re.compile(",\s{1}(\d{3,4})x(\d{3,4})\s{0,2}")
        matches = re.search(pattern_duration, stdout.decode('utf-8')).groups()
        Debug.Log("matches:  "+str(matches))
        size = re.search(pattern_size, stdout.decode('utf-8')).groups()
        Debug.Log('size: ')
        Debug.Log(size)
        #matches = re.search(r"Duration:\s{1}(?P\d+?):(?P\d+?):(?P\d+\.\d+?),", stdout, re.DOTALL).groupdict()
        hours = Decimal(matches[0])
        minutes = Decimal(matches[1])
        seconds = Decimal(matches[2])
        total = 0
        total += 60 * 60 * hours
        total += 60 * minutes
        total += seconds
        width = size[0]
        height = size[1]
        return [total, width, height]
    # 从输入的时间转换为可识别的

    def GetStartTime(self, startArg):
        startlist = startArg.split('.')
        startsencond = 0
        if len(startlist) == 0:
            startsencond = 0
        elif len(startlist) == 1:
            startsencond = int(startlist[0])
        elif len(startlist) == 2:
            startsencond = int(startlist[0])*60+int(startlist[1])
        elif len(startlist) == 3:
            startsencond = int(startlist[0])*3600 + \
                int(startlist[1])*60+int(startlist[2])
        return startsencond*1000
        # 从秒转换为 ffpeg识别的时间格式

    def millisecToAssFormat(self, t):
        tm = t
        hao = tm % 1000
        tm = tm/1000
        miao = tm % 60
        tm = tm/60
        fen = tm % 60
        tm = tm/60
        shi = tm
        hao = hao/10
        return "%02d:%02d:%02d" % (shi, fen, miao)

    def cutVideo(self, startPoint, endPoint, path, newFile,ffmpegPath):
        command = [ffmpegPath, '-ss', startPoint, '-t', endPoint, '-accurate_seek',
                   '-i', path, '-codec', 'copy', '-avoid_negative_ts', '1', newFile]
        subprocess.call(command, creationflags = CREATE_NO_WINDOW)
        return 1
        # 删除到回收站

    def deltorecyclebin(self,filename):
        # print('deltorecyclebin', filename)
        # os.remove(filename) #直接删除文件，不经过回收站
        res = shell.SHFileOperation((0, shellcon.FO_DELETE, filename, None, shellcon.FOF_SILENT |
                                 shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION | shellcon.FOF_NOERRORUI, None, None))  # 删除文件到回收站
        if not res[1]:
            os.system('del '+filename)

    #合成
    # ffmpeg -f concat -i filelist.txt -c copy output.mkv
    def MergeMovie(self,path):
        Debug.Log("MergeMovie path: "+path)
        fileListTxtPath = path + MergeFileListName
        curVideolist,curOtherFilelist = self.GenerateMergeFileListTxt(path,fileListTxtPath)
        Debug.Log("fileListTxtPath: "+fileListTxtPath)
        newFile = self.GetMergeNewFileName(curVideolist)
        if newFile == None:
            return 1
        Debug.Log("newFile: "+newFile)
        command = [ffmpegPath,'-f', 'concat','-safe','0','-i', fileListTxtPath,'-c','copy',newFile]
        subprocess.call(command, creationflags = CREATE_NO_WINDOW)
        # process = subprocess.Popen(
        # [ffmpegPath,'-f', 'concat','-safe','0','-i', fileListTxtPath,'-c','copy',newFile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # stdout, stderr = process.communicate()
        # Debug.Log(stdout)
        # Debug.Log(stderr)
        self.DeleteOtherFile(fileListTxtPath,curVideolist,curOtherFilelist)
        return 1
    #生成合成需要的配置txt文件
    def GenerateMergeFileListTxt(self,path,fileListTxtPath):
        if os.path.exists(fileListTxtPath):
            os.remove(fileListTxtPath)
        #不递归遍历文件夹 找出所有文件
        curVideolist=[]
        curOtherFilelist=[]
        for filename in os.listdir(path):
            curFilePath = os.path.join(path, filename)
            if os.path.splitext(filename)[1] == '.nfo':
                Debug.Log("nfo file : " + curFilePath)
                curOtherFilelist.append(curFilePath)
            elif os.path.splitext(filename)[1] == '.jpg':
                Debug.Log("jpg file : " + curFilePath)
                curOtherFilelist.append(curFilePath)
            else:
                Debug.Log("vedio file : " + curFilePath)
                curVideolist.append(curFilePath)
        with open(fileListTxtPath,"a") as file:   #只需要将之前的”w"改为“a"即可，代表追加内容
            for curFilePath in curVideolist:
                Debug.Log("Add vedio file to txt: " + curFilePath)
                file.write("file \'"+curFilePath+"\'\n")
        return curVideolist,curOtherFilelist
    #获取合成后的视频名字
    def GetMergeNewFileName(self,curVideolist):
        for curFilePath in curVideolist:
            pathSplite = os.path.splitext(curFilePath)
            for num in range(1, CDMaxNum):
                cdEndStr = '-CD'+str(num)
                if pathSplite[0].endswith(cdEndStr):
                    newFile = curFilePath.replace(cdEndStr, '')
                    return newFile
        Debug.Log("GetMergeNewFileName fail: ")
        return None
    #合成之后删除不要的图片和nfo文件
    def DeleteOtherFile(self,fileListTxtPath,curVideolist,curOtherFilelist):
        if os.path.exists(fileListTxtPath):
            os.remove(fileListTxtPath)
        for curFilePath in curOtherFilelist:
            if os.path.exists(curFilePath):
                # os.remove(curFilePath)
                self.deltorecyclebin(curFilePath)
        for curFilePath in curVideolist:
            if os.path.exists(curFilePath):
                self.deltorecyclebin(curFilePath)