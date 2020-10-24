from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from MainUI import Ui_Dialog
import LogTool
import ConfigTool
import MovieInfoTool
import DirTool
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
Debug = LogTool.Debug()
Debug.InitLogger(current_dir)

ConfigCheboxID = 10000
TagConfiName = "TagConfig.txt"

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
        self.filePath =  sys.argv[1]
        self.workPath = sys.path[0]
        Debug.Log("self.workPath: " + self.workPath)
        self.InfoFileList = DirTool.GetAllMovieInfoFile(self.filePath)
        self.MovieInfoToolList = []
        for file in self.InfoFileList:
            Debug.Log("self.InfoFileList: " + file)
            item = MovieInfoTool.MovieInfoTool()
            item.ReadInfoFile(file,Debug)
            self.MovieInfoToolList.append(item)
        alltag = self.MovieInfoToolList[0].GetAllTags()
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
        self.configPath = self.workPath + '\\' + TagConfiName
        Debug.Log("self.configPath: " + self.configPath)
        self.configList = ConfigTool.ReadConfig(self.configPath)
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
        list = []
        for checkBox in self.checkBoxList:
            if checkBox.isChecked() == True:
                list.append(checkBox.text())
                Debug.Log("confirm_btn: " + checkBox.text())
        for item in self.MovieInfoToolList:
            item.SaveAllTag(list)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())
