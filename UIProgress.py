# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIProgress.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.setWindowModality(QtCore.Qt.NonModal)
        ProgressDialog.resize(400, 353)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progress_bar = QtWidgets.QProgressBar(ProgressDialog)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout.addWidget(self.progress_bar)
        self.line = QtWidgets.QFrame(ProgressDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(ProgressDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.en_cours = QtWidgets.QTextEdit(ProgressDialog)
        self.en_cours.setReadOnly(True)
        self.en_cours.setObjectName("en_cours")
        self.verticalLayout.addWidget(self.en_cours)
        self.line_2 = QtWidgets.QFrame(ProgressDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.label_2 = QtWidgets.QLabel(ProgressDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.errors = QtWidgets.QTextEdit(ProgressDialog)
        self.errors.setReadOnly(True)
        self.errors.setObjectName("errors")
        self.verticalLayout.addWidget(self.errors)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.stop_button = QtWidgets.QPushButton(ProgressDialog)
        self.stop_button.setObjectName("stop_button")
        self.horizontalLayout.addWidget(self.stop_button)
        self.close_button = QtWidgets.QPushButton(ProgressDialog)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Progress"))
        self.label.setText(_translate("ProgressDialog", "Machines en cours"))
        self.label_2.setText(_translate("ProgressDialog", "Machines en erreur"))
        self.stop_button.setText(_translate("ProgressDialog", "Stop"))
        self.close_button.setText(_translate("ProgressDialog", "Close"))

