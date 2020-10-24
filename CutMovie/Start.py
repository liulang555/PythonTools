# > nul 2>&1 || cd "%~dp0" && python "%~0" && goto :eof
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from MainUI import Ui_Dialog
import ffmpegTool

class mywindow(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.ConfirmpushButton.clicked.connect(self.confirm_btn)
        self.ReplacepushButton_2.clicked.connect(self.Replace_Btn)
        self.StartTimelineEdit.returnPressed.connect(
            self.StartTimelineEdit_function)
        self.EndTimelineEdit.returnPressed.connect(self.confirm_btn)
        self.setWindowTitle(sys.argv[1])

    def confirm_btn(self):
        print(self.StartTimelineEdit.text())
        print(self.EndTimelineEdit.text())
        ffpeg = ffmpegTool.ffmpegTool()
        path = sys.argv[1]  # 从批处理传进参数 文件的完整路径
        #print("批处理文件里面的路径参数：  "+path)
        retcode = ffpeg.CutMovie(
            path, self.StartTimelineEdit.text(), self.EndTimelineEdit.text(),self.radioButton.isChecked())
        if retcode == 1:
            self.close()

    def StartTimelineEdit_function(self):
        self.EndTimelineEdit.setFocus()

    def Replace_Btn(self):
        self.StartTimelineEdit.setText('')
        self.EndTimelineEdit.setText('')


if __name__ == "__main__":
    import sys
    # os.system("taskkill /f /im cmd.exe")
    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())
