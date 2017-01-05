# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UILog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_log_dialog(object):
    def setupUi(self, log_dialog):
        log_dialog.setObjectName("log_dialog")
        log_dialog.resize(838, 578)
        self.verticalLayout = QtWidgets.QVBoxLayout(log_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(log_dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.max_line = QtWidgets.QSpinBox(log_dialog)
        self.max_line.setMaximum(5000)
        self.max_line.setProperty("value", 500)
        self.max_line.setObjectName("max_line")
        self.horizontalLayout.addWidget(self.max_line)
        self.label = QtWidgets.QLabel(log_dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.regex_edit1 = QtWidgets.QLineEdit(log_dialog)
        self.regex_edit1.setObjectName("regex_edit1")
        self.horizontalLayout.addWidget(self.regex_edit1)
        self.error_label1 = QtWidgets.QLabel(log_dialog)
        self.error_label1.setStyleSheet("")
        self.error_label1.setTextFormat(QtCore.Qt.AutoText)
        self.error_label1.setObjectName("error_label1")
        self.horizontalLayout.addWidget(self.error_label1)
        self.label_3 = QtWidgets.QLabel(log_dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.regex_edit2 = QtWidgets.QLineEdit(log_dialog)
        self.regex_edit2.setObjectName("regex_edit2")
        self.horizontalLayout.addWidget(self.regex_edit2)
        self.error_label2 = QtWidgets.QLabel(log_dialog)
        self.error_label2.setStyleSheet("")
        self.error_label2.setTextFormat(QtCore.Qt.AutoText)
        self.error_label2.setObjectName("error_label2")
        self.horizontalLayout.addWidget(self.error_label2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.log_text_edit = QtWidgets.QPlainTextEdit(log_dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.log_text_edit.setFont(font)
        self.log_text_edit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.log_text_edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.log_text_edit.setObjectName("log_text_edit")
        self.verticalLayout.addWidget(self.log_text_edit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.stop_start_button = QtWidgets.QPushButton(log_dialog)
        self.stop_start_button.setObjectName("stop_start_button")
        self.horizontalLayout_2.addWidget(self.stop_start_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(log_dialog)
        QtCore.QMetaObject.connectSlotsByName(log_dialog)

    def retranslateUi(self, log_dialog):
        _translate = QtCore.QCoreApplication.translate
        log_dialog.setWindowTitle(_translate("log_dialog", "Log"))
        self.label_2.setText(_translate("log_dialog", "Max line"))
        self.label.setText(_translate("log_dialog", "Regex filtre1"))
        self.error_label1.setText(_translate("log_dialog", "<html><head/><body><p><span style=\" color:#ff0000;\">error</span></p></body></html>"))
        self.label_3.setText(_translate("log_dialog", "filtre 2"))
        self.error_label2.setText(_translate("log_dialog", "<html><head/><body><p><span style=\" color:#ff0000;\">error</span></p></body></html>"))
        self.stop_start_button.setText(_translate("log_dialog", "Stop/Start"))

