# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SourceTreeFloder\PythonTools\CutMovie\MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(273, 178)
        self.ConfirmpushButton = QtWidgets.QPushButton(Dialog)
        self.ConfirmpushButton.setGeometry(QtCore.QRect(10, 130, 91, 41))
        self.ConfirmpushButton.setObjectName("ConfirmpushButton")
        self.ReplacepushButton_2 = QtWidgets.QPushButton(Dialog)
        self.ReplacepushButton_2.setGeometry(QtCore.QRect(160, 130, 91, 41))
        self.ReplacepushButton_2.setObjectName("ReplacepushButton_2")
        self.StartTimelabel = QtWidgets.QLabel(Dialog)
        self.StartTimelabel.setGeometry(QtCore.QRect(10, 20, 64, 18))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.StartTimelabel.setFont(font)
        self.StartTimelabel.setObjectName("StartTimelabel")
        self.EndTimelabel = QtWidgets.QLabel(Dialog)
        self.EndTimelabel.setGeometry(QtCore.QRect(10, 60, 64, 18))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.EndTimelabel.setFont(font)
        self.EndTimelabel.setObjectName("EndTimelabel")
        self.EndTimelineEdit = QtWidgets.QLineEdit(Dialog)
        self.EndTimelineEdit.setGeometry(QtCore.QRect(110, 50, 151, 31))
        self.EndTimelineEdit.setObjectName("EndTimelineEdit")
        self.StartTimelineEdit = QtWidgets.QLineEdit(Dialog)
        self.StartTimelineEdit.setGeometry(QtCore.QRect(110, 10, 151, 31))
        self.StartTimelineEdit.setObjectName("StartTimelineEdit")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(10, 90, 91, 31))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ConfirmpushButton.setText(_translate("Dialog", "确定"))
        self.ReplacepushButton_2.setText(_translate("Dialog", "重置"))
        self.StartTimelabel.setText(_translate("Dialog", "开始时间"))
        self.EndTimelabel.setText(_translate("Dialog", "结束时间"))
        self.radioButton.setText(_translate("Dialog", "替换源文件"))
