# > nul 2>&1 || cd "%~dp0" && python "%~0" && goto :eof
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from MainUI import Ui_Dialog
import ImgMarkTool
import os
import sys
import LogTool
import MovieInfoTool

current_dir = os.path.dirname(os.path.abspath(__file__))
Debug = LogTool.Debug()
Debug.InitLogger(current_dir)


class mywindow(QtWidgets.QWidget, Ui_Dialog):
  def __init__(self):
    super(mywindow, self).__init__()
    self.setupUi(self)
    self.pushButton.clicked.connect(self.confirm_btn)
    self.InitMarkList()

  def InitMarkList(self):
    self.filePath = sys.argv[1]
    Debug.Log("filePath: " + self.filePath)
    self.checkBoxList = []
    for index in range(len(ImgMarkTool.MarkTagName)):
        Debug.Log("InitMarkList: " + ImgMarkTool.MarkTagName[index] )
        checkBox = QtWidgets.QCheckBox(ImgMarkTool.MarkTagName[index], self)
        checkBox.id_ = index
        checkBox.stateChanged.connect(self.SelectTag)
        self.horizontalLayout.addWidget(checkBox)
        self.checkBoxList.append(checkBox)

  def confirm_btn(self):
    curlist = []
    for checkBox in self.checkBoxList:
        if checkBox.isChecked() == True:
            curlist.append(checkBox.text())
            Debug.Log("confirm_btn: " + checkBox.text())
    ImgMarkTool.AddMarkBytagList(self.filePath,curlist)
    #添加标签
    MovieInfoToolList = MovieInfoTool.MovieInfoToolList()
    MovieInfoToolList.ReadInfoFile(self.filePath,Debug)
    for curName in curlist:
        MovieInfoToolList.AddTag(curName)
    MovieInfoToolList.SaveNFO()
    Debug.Log("编辑成功！")
    self.close()
  def SelectTag(self, state):
    checkBox = self.sender()
    if state == QtCore.Qt.Unchecked:
        Debug.Log('取消选择 : '+ checkBox.text())
    elif state == QtCore.Qt.Checked:
        Debug.Log('选择 : '+ checkBox.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())
