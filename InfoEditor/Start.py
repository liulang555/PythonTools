from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from MainUI import Ui_Dialog
import LogTool
import ConfigTool
import MovieInfoTool
import ImgMarkTool
import DirTool
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
Debug = LogTool.Debug()
Debug.InitLogger(current_dir)

ConfigCheboxID = 10000
TagConfiName = "编辑标签--预设标签.txt"

class mywindow(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.confirm_btn)
        self.pushButton_2.clicked.connect(self.openConfig_btn)
        self.checkBox.stateChanged.connect(self.AllMovieInfoListCheckBox)
        self.InitMovieInfoList()
        self.InitConfigList()

    def InitMovieInfoList(self):
        self.filePath = sys.argv[1]
        self.workPath = sys.path[0]
        self.MovieInfoToolList = MovieInfoTool.MovieInfoToolList()
        self.MovieInfoToolList.ReadInfoFile(self.filePath,Debug)
        alltag = self.MovieInfoToolList.GetAllTags()
        self.checkBoxList = []
        for index in range(len(alltag)):
            Debug.Log("alltag: " + alltag[index])
            checkBox = QtWidgets.QCheckBox(alltag[index], self)
            checkBox.id_ = index
            checkBox.setChecked(True)
            self.checkBoxList.append(checkBox)
            checkBox.stateChanged.connect(self.SelectTag)
            self.verticalLayout.addWidget(checkBox)
    def InitConfigList(self):
        self.configList = ConfigTool.ReadConfigByTxtName(TagConfiName)
        for index in range(len(self.configList)):
            Debug.Log("configList: " + self.configList[index] )
            checkBox = QtWidgets.QCheckBox(self.configList[index], self)
            checkBox.id_ = index + ConfigCheboxID
            checkBox.stateChanged.connect(self.SelectTag)
            self.verticalLayout_2.addWidget(checkBox)
            self.checkBoxList.append(checkBox)

    def SelectTag(self, state):
        checkBox = self.sender()
        if state == QtCore.Qt.Unchecked:
            Debug.Log('取消选择 : '+ checkBox.text())
        elif state == QtCore.Qt.Checked:
            Debug.Log('选择 : '+ checkBox.text())

    def openConfig_btn(self):
        Debug.Log("openConfig_btn: ")
        os.system(r'notepad ' + self.configPath)

    def AllMovieInfoListCheckBox(self, state):
        if state == QtCore.Qt.Unchecked:
            Debug.Log('取消选择 : '+ self.checkBox.text())
            for checkBox in self.checkBoxList:
                if checkBox.id_ < ConfigCheboxID :
                    checkBox.setChecked(False)
        elif state == QtCore.Qt.Checked:
            Debug.Log('选择 : '+ self.checkBox.text())
            for checkBox in self.checkBoxList:
                if checkBox.id_ < ConfigCheboxID :
                    checkBox.setChecked(True)

    def confirm_btn(self):
        Debug.Log("confirm_btn: ")
        curlist = []
        for checkBox in self.checkBoxList:
            if checkBox.isChecked() == True:
                curlist.append(checkBox.text())
                Debug.Log("confirm_btn: " + checkBox.text())
        self.MovieInfoToolList.SaveAllTag(curlist)
        self.close()
        self.SetImgMark(curlist)
        Debug.Log("编辑成功！")
    #添加水印
    def SetImgMark(self,curlist):
        ImgMarkTool.AddMarkBytagList(self.filePath,curlist)

if __name__ == "__main__":
    Debug.Log("self.workPath: " + sys.path[0])
    Debug.Log("self.filePath: " + sys.argv[1][:-1])
    curlist = DirTool.GetAllMovieInfoFile(sys.argv[1][:-1],Debug)
    Debug.Log("self.InfoFileList count: " + str(len(curlist)))
    if len(curlist) == 0:
        Debug.Log("路径选择错误")
    else:
        app = QtWidgets.QApplication(sys.argv)
        ui = mywindow()
        ui.show()
        sys.exit(app.exec_())
