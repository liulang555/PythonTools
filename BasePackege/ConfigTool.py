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

def SaveConfigToEnd(txtName,content):
    try:
        path = GetConfigPath(txtName)
        file = open(path, "a", encoding='utf-8')#写入文件，若文件不存在则会先创建再写入，但不会覆盖原文件，而是追加在文件末尾
        file.write('\n'+content)
        file.close()
    except IOError:
        print("save file fail:  " + path+" content: "+content)

def GetConfigPath(txtName):
    return  current_dir + allUsedConfigDirName + txtName

def ReadConfigByTxtName(txtName):
    path = GetConfigPath(txtName)
    return ReadConfig(path)

def OpenConfigDir():
    DirectoryOpusTool.OpenDirByOpenWindow(current_dir + allUsedConfigDirName)