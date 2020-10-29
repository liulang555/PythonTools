import sys
import os
import DirectoryOpusTool

current_dir = os.path.dirname(os.path.abspath(__file__))
allUsedConfigDirName = "\\AllUsedConfig\\"


def ReadConfig(path):
    list = []
    try:
        file = open(path, "rb")  # 选用rb  防止读取文件出错
        # filereader=file.decode("utf-8")
    except IOError:
        print("open file fail:  " + path)
    else:
        for index in file:
            linetemp = index.decode("utf-8").strip()
            # 去掉字符串中的 \ufeff
            line = linetemp.encode('utf-8').decode('utf-8-sig')
            if line != "":
                # print(line)
                list.append(line)
        file.close()
        return list


def GetConfigPath(txtName):
    return  current_dir + allUsedConfigDirName + txtName

def ReadConfigByTxtName(txtName):
    path = GetConfigPath(txtName)
    return ReadConfig(path)

def OpenConfigDir():
    DirectoryOpusTool.OpenDirByOpenWindow(current_dir + allUsedConfigDirName)