# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIMagretUtil.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1225, 641)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QGroupBox { \n"
"     border: 1px solid gray; \n"
"     /*border-radius: 20px; */\n"
"    margin-top:7px\n"
"    \n"
" } \n"
"\n"
"QGroupBox::title {\n"
"   \n"
"    left: 10px;\n"
"    top: -7px;\n"
"    padding: 0 5px 0 5px;\n"
"}\n"
"")
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.SelectionGroup = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectionGroup.sizePolicy().hasHeightForWidth())
        self.SelectionGroup.setSizePolicy(sizePolicy)
        self.SelectionGroup.setMinimumSize(QtCore.QSize(700, 0))
        self.SelectionGroup.setObjectName("SelectionGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.SelectionGroup)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.wol_button = QtWidgets.QPushButton(self.SelectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wol_button.sizePolicy().hasHeightForWidth())
        self.wol_button.setSizePolicy(sizePolicy)
        self.wol_button.setObjectName("wol_button")
        self.horizontalLayout_8.addWidget(self.wol_button)
        self.shutdown_button = QtWidgets.QPushButton(self.SelectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shutdown_button.sizePolicy().hasHeightForWidth())
        self.shutdown_button.setSizePolicy(sizePolicy)
        self.shutdown_button.setObjectName("shutdown_button")
        self.horizontalLayout_8.addWidget(self.shutdown_button)
        self.clean_button = QtWidgets.QPushButton(self.SelectionGroup)
        self.clean_button.setObjectName("clean_button")
        self.horizontalLayout_8.addWidget(self.clean_button)
        self.vnc_button = QtWidgets.QPushButton(self.SelectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vnc_button.sizePolicy().hasHeightForWidth())
        self.vnc_button.setSizePolicy(sizePolicy)
        self.vnc_button.setObjectName("vnc_button")
        self.horizontalLayout_8.addWidget(self.vnc_button)
        self.tag_button = QtWidgets.QPushButton(self.SelectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tag_button.sizePolicy().hasHeightForWidth())
        self.tag_button.setSizePolicy(sizePolicy)
        self.tag_button.setObjectName("tag_button")
        self.horizontalLayout_8.addWidget(self.tag_button)
        self.password_button = QtWidgets.QPushButton(self.SelectionGroup)
        self.password_button.setObjectName("password_button")
        self.horizontalLayout_8.addWidget(self.password_button)
        self.log_button = QtWidgets.QPushButton(self.SelectionGroup)
        self.log_button.setObjectName("log_button")
        self.horizontalLayout_8.addWidget(self.log_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.check_uncheck_button = QtWidgets.QPushButton(self.SelectionGroup)
        self.check_uncheck_button.setObjectName("check_uncheck_button")
        self.horizontalLayout_11.addWidget(self.check_uncheck_button)
        self.inverse_button = QtWidgets.QPushButton(self.SelectionGroup)
        self.inverse_button.setObjectName("inverse_button")
        self.horizontalLayout_11.addWidget(self.inverse_button)
        self.only_checkbox = QtWidgets.QCheckBox(self.SelectionGroup)
        self.only_checkbox.setObjectName("only_checkbox")
        self.horizontalLayout_11.addWidget(self.only_checkbox)
        self.ping_checkbox = QtWidgets.QCheckBox(self.SelectionGroup)
        self.ping_checkbox.setChecked(True)
        self.ping_checkbox.setObjectName("ping_checkbox")
        self.horizontalLayout_11.addWidget(self.ping_checkbox)
        self.kill_ping_button = QtWidgets.QPushButton(self.SelectionGroup)
        self.kill_ping_button.setObjectName("kill_ping_button")
        self.horizontalLayout_11.addWidget(self.kill_ping_button)
        self.label_5 = QtWidgets.QLabel(self.SelectionGroup)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_11.addWidget(self.label_5)
        self.ping_thread_edit = QtWidgets.QLineEdit(self.SelectionGroup)
        self.ping_thread_edit.setEnabled(False)
        self.ping_thread_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ping_thread_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ping_thread_edit.setObjectName("ping_thread_edit")
        self.horizontalLayout_11.addWidget(self.ping_thread_edit)
        self.ping_time_label = QtWidgets.QLabel(self.SelectionGroup)
        self.ping_time_label.setObjectName("ping_time_label")
        self.horizontalLayout_11.addWidget(self.ping_time_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter_select = QtWidgets.QSplitter(self.SelectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_select.sizePolicy().hasHeightForWidth())
        self.splitter_select.setSizePolicy(sizePolicy)
        self.splitter_select.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter_select.setBaseSize(QtCore.QSize(0, 0))
        self.splitter_select.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_select.setOpaqueResize(True)
        self.splitter_select.setChildrenCollapsible(False)
        self.splitter_select.setObjectName("splitter_select")
        self.tree_select = QtWidgets.QTreeWidget(self.splitter_select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_select.sizePolicy().hasHeightForWidth())
        self.tree_select.setSizePolicy(sizePolicy)
        self.tree_select.setMinimumSize(QtCore.QSize(190, 0))
        self.tree_select.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tree_select.setSizeIncrement(QtCore.QSize(0, 0))
        self.tree_select.setBaseSize(QtCore.QSize(0, 0))
        self.tree_select.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tree_select.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tree_select.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tree_select.setRootIsDecorated(True)
        self.tree_select.setItemsExpandable(True)
        self.tree_select.setAllColumnsShowFocus(False)
        self.tree_select.setExpandsOnDoubleClick(True)
        self.tree_select.setObjectName("tree_select")
        self.tree_select.header().setVisible(False)
        self.tree_select.header().setStretchLastSection(True)
        self.table_select = QtWidgets.QTableWidget(self.splitter_select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_select.sizePolicy().hasHeightForWidth())
        self.table_select.setSizePolicy(sizePolicy)
        self.table_select.setMinimumSize(QtCore.QSize(0, 0))
        self.table_select.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.table_select.setStyleSheet("QTableWidget::item:!enabled {\n"
"    color: black;\n"
"}\n"
"QHeaderView::section{\n"
"            border-top:0px solid #D8D8D8;\n"
"            border-left:0px solid #D8D8D8;\n"
"            border-right:1px solid #D8D8D8;\n"
"            border-bottom: 1px solid #D8D8D8;\n"
"            background-color:white;\n"
"            padding:4px;\n"
"        }\n"
"QTableCornerButton::section{\n"
"            border-top:0px solid #D8D8D8;\n"
"            border-left:0px solid #D8D8D8;\n"
"            border-right:1px solid #D8D8D8;\n"
"            border-bottom: 1px solid #D8D8D8;\n"
"            background-color:white;\n"
"        }")
        self.table_select.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table_select.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_select.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.table_select.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.table_select.setObjectName("table_select")
        self.table_select.setColumnCount(7)
        self.table_select.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_select.setHorizontalHeaderItem(6, item)
        self.table_select.horizontalHeader().setVisible(True)
        self.table_select.horizontalHeader().setDefaultSectionSize(60)
        self.table_select.horizontalHeader().setMinimumSectionSize(30)
        self.table_select.horizontalHeader().setSortIndicatorShown(True)
        self.table_select.horizontalHeader().setStretchLastSection(True)
        self.table_select.verticalHeader().setVisible(False)
        self.table_select.verticalHeader().setSortIndicatorShown(True)
        self.table_select.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_4.addWidget(self.splitter_select)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7.addWidget(self.SelectionGroup)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.CommandesGroup = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommandesGroup.sizePolicy().hasHeightForWidth())
        self.CommandesGroup.setSizePolicy(sizePolicy)
        self.CommandesGroup.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.CommandesGroup.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.CommandesGroup.setObjectName("CommandesGroup")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.CommandesGroup)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.run_file_button = QtWidgets.QPushButton(self.CommandesGroup)
        self.run_file_button.setObjectName("run_file_button")
        self.gridLayout_2.addWidget(self.run_file_button, 2, 2, 1, 1)
        self.run_cmd_button = QtWidgets.QPushButton(self.CommandesGroup)
        self.run_cmd_button.setFlat(False)
        self.run_cmd_button.setObjectName("run_cmd_button")
        self.gridLayout_2.addWidget(self.run_cmd_button, 0, 2, 1, 1)
        self.cmd_input = QtWidgets.QLineEdit(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmd_input.sizePolicy().hasHeightForWidth())
        self.cmd_input.setSizePolicy(sizePolicy)
        self.cmd_input.setMinimumSize(QtCore.QSize(0, 0))
        self.cmd_input.setText("")
        self.cmd_input.setObjectName("cmd_input")
        self.gridLayout_2.addWidget(self.cmd_input, 0, 0, 1, 1)
        self.file_input = QtWidgets.QLineEdit(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_input.sizePolicy().hasHeightForWidth())
        self.file_input.setSizePolicy(sizePolicy)
        self.file_input.setMinimumSize(QtCore.QSize(0, 0))
        self.file_input.setObjectName("file_input")
        self.gridLayout_2.addWidget(self.file_input, 2, 0, 1, 1)
        self.openfile_button = QtWidgets.QToolButton(self.CommandesGroup)
        self.openfile_button.setObjectName("openfile_button")
        self.gridLayout_2.addWidget(self.openfile_button, 2, 1, 1, 1)
        self.no_wait = QtWidgets.QCheckBox(self.CommandesGroup)
        self.no_wait.setObjectName("no_wait")
        self.gridLayout_2.addWidget(self.no_wait, 0, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.time_out = QtWidgets.QCheckBox(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_out.sizePolicy().hasHeightForWidth())
        self.time_out.setSizePolicy(sizePolicy)
        self.time_out.setObjectName("time_out")
        self.horizontalLayout.addWidget(self.time_out)
        self.time_out_input = QtWidgets.QLineEdit(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_out_input.sizePolicy().hasHeightForWidth())
        self.time_out_input.setSizePolicy(sizePolicy)
        self.time_out_input.setMinimumSize(QtCore.QSize(50, 0))
        self.time_out_input.setMaximumSize(QtCore.QSize(50, 16777215))
        self.time_out_input.setSizeIncrement(QtCore.QSize(0, 0))
        self.time_out_input.setBaseSize(QtCore.QSize(0, 0))
        self.time_out_input.setInputMethodHints(QtCore.Qt.ImhNone)
        self.time_out_input.setText("")
        self.time_out_input.setMaxLength(5)
        self.time_out_input.setObjectName("time_out_input")
        self.horizontalLayout.addWidget(self.time_out_input)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 4, 1, 1)
        self.alias_button = QtWidgets.QComboBox(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alias_button.sizePolicy().hasHeightForWidth())
        self.alias_button.setSizePolicy(sizePolicy)
        self.alias_button.setObjectName("alias_button")
        self.alias_button.addItem("")
        self.gridLayout_2.addWidget(self.alias_button, 2, 4, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.line = QtWidgets.QFrame(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.put_button = QtWidgets.QPushButton(self.CommandesGroup)
        self.put_button.setObjectName("put_button")
        self.horizontalLayout_3.addWidget(self.put_button)
        self.put_src_edit = QtWidgets.QLineEdit(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.put_src_edit.sizePolicy().hasHeightForWidth())
        self.put_src_edit.setSizePolicy(sizePolicy)
        self.put_src_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.put_src_edit.setObjectName("put_src_edit")
        self.horizontalLayout_3.addWidget(self.put_src_edit)
        self.openfile_put_button = QtWidgets.QToolButton(self.CommandesGroup)
        self.openfile_put_button.setObjectName("openfile_put_button")
        self.horizontalLayout_3.addWidget(self.openfile_put_button)
        self.label = QtWidgets.QLabel(self.CommandesGroup)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.put_dest_edit = QtWidgets.QLineEdit(self.CommandesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.put_dest_edit.sizePolicy().hasHeightForWidth())
        self.put_dest_edit.setSizePolicy(sizePolicy)
        self.put_dest_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.put_dest_edit.setObjectName("put_dest_edit")
        self.horizontalLayout_3.addWidget(self.put_dest_edit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8.addWidget(self.CommandesGroup)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.account_name_input = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_name_input.sizePolicy().hasHeightForWidth())
        self.account_name_input.setSizePolicy(sizePolicy)
        self.account_name_input.setObjectName("account_name_input")
        self.horizontalLayout_5.addWidget(self.account_name_input)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.account_password_input = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_password_input.sizePolicy().hasHeightForWidth())
        self.account_password_input.setSizePolicy(sizePolicy)
        self.account_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.account_password_input.setObjectName("account_password_input")
        self.horizontalLayout_5.addWidget(self.account_password_input)
        self.admin_check = QtWidgets.QCheckBox(self.groupBox)
        self.admin_check.setObjectName("admin_check")
        self.horizontalLayout_5.addWidget(self.admin_check)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.list_account_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_account_button.sizePolicy().hasHeightForWidth())
        self.list_account_button.setSizePolicy(sizePolicy)
        self.list_account_button.setObjectName("list_account_button")
        self.horizontalLayout_9.addWidget(self.list_account_button)
        self.chpwd_user_button = QtWidgets.QPushButton(self.groupBox)
        self.chpwd_user_button.setObjectName("chpwd_user_button")
        self.horizontalLayout_9.addWidget(self.chpwd_user_button)
        self.add_account_button = QtWidgets.QPushButton(self.groupBox)
        self.add_account_button.setObjectName("add_account_button")
        self.horizontalLayout_9.addWidget(self.add_account_button)
        self.list_groupe_button = QtWidgets.QPushButton(self.groupBox)
        self.list_groupe_button.setObjectName("list_groupe_button")
        self.horizontalLayout_9.addWidget(self.list_groupe_button)
        self.del_account_button = QtWidgets.QPushButton(self.groupBox)
        self.del_account_button.setObjectName("del_account_button")
        self.horizontalLayout_9.addWidget(self.del_account_button)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.verticalLayout_8.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.filter_input = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_input.sizePolicy().hasHeightForWidth())
        self.filter_input.setSizePolicy(sizePolicy)
        self.filter_input.setObjectName("filter_input")
        self.horizontalLayout_6.addWidget(self.filter_input)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.list_prog_button = QtWidgets.QPushButton(self.groupBox_2)
        self.list_prog_button.setObjectName("list_prog_button")
        self.horizontalLayout_10.addWidget(self.list_prog_button)
        self.uninstall_prog_button = QtWidgets.QPushButton(self.groupBox_2)
        self.uninstall_prog_button.setObjectName("uninstall_prog_button")
        self.horizontalLayout_10.addWidget(self.uninstall_prog_button)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.verticalLayout_8.addWidget(self.groupBox_2)
        self.ResultatGroup = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultatGroup.sizePolicy().hasHeightForWidth())
        self.ResultatGroup.setSizePolicy(sizePolicy)
        self.ResultatGroup.setFlat(False)
        self.ResultatGroup.setObjectName("ResultatGroup")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.ResultatGroup)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.compare_button = QtWidgets.QPushButton(self.ResultatGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compare_button.sizePolicy().hasHeightForWidth())
        self.compare_button.setSizePolicy(sizePolicy)
        self.compare_button.setObjectName("compare_button")
        self.horizontalLayout_2.addWidget(self.compare_button)
        self.seuil_label = QtWidgets.QLabel(self.ResultatGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seuil_label.sizePolicy().hasHeightForWidth())
        self.seuil_label.setSizePolicy(sizePolicy)
        self.seuil_label.setObjectName("seuil_label")
        self.horizontalLayout_2.addWidget(self.seuil_label)
        self.seuil = QtWidgets.QSpinBox(self.ResultatGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seuil.sizePolicy().hasHeightForWidth())
        self.seuil.setSizePolicy(sizePolicy)
        self.seuil.setMaximum(100)
        self.seuil.setProperty("value", 90)
        self.seuil.setObjectName("seuil")
        self.horizontalLayout_2.addWidget(self.seuil)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.resultat_label = QtWidgets.QLabel(self.ResultatGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultat_label.sizePolicy().hasHeightForWidth())
        self.resultat_label.setSizePolicy(sizePolicy)
        self.resultat_label.setObjectName("resultat_label")
        self.verticalLayout_3.addWidget(self.resultat_label)
        self.resultat_text = QtWidgets.QTextBrowser(self.ResultatGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.resultat_text.sizePolicy().hasHeightForWidth())
        self.resultat_text.setSizePolicy(sizePolicy)
        self.resultat_text.setMinimumSize(QtCore.QSize(0, 200))
        self.resultat_text.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.resultat_text.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.resultat_text.setObjectName("resultat_text")
        self.verticalLayout_3.addWidget(self.resultat_text)
        self.verticalLayout_8.addWidget(self.ResultatGroup)
        self.horizontalLayout_7.addLayout(self.verticalLayout_8)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1225, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SelectionGroup.setTitle(_translate("MainWindow", "Séléction"))
        self.wol_button.setText(_translate("MainWindow", "Wol"))
        self.shutdown_button.setText(_translate("MainWindow", "Shutdown"))
        self.clean_button.setText(_translate("MainWindow", "Clean"))
        self.vnc_button.setText(_translate("MainWindow", "vnc"))
        self.tag_button.setText(_translate("MainWindow", "Tag"))
        self.password_button.setText(_translate("MainWindow", "Password"))
        self.log_button.setText(_translate("MainWindow", "Log"))
        self.check_uncheck_button.setText(_translate("MainWindow", "Check/Uncheck selection"))
        self.inverse_button.setText(_translate("MainWindow", "Inverse checked"))
        self.only_checkbox.setText(_translate("MainWindow", "Show only checked"))
        self.ping_checkbox.setText(_translate("MainWindow", "Ping"))
        self.kill_ping_button.setText(_translate("MainWindow", "Kill ping"))
        self.label_5.setText(_translate("MainWindow", "Ping thread"))
        self.ping_thread_edit.setText(_translate("MainWindow", "100"))
        self.ping_time_label.setText(_translate("MainWindow", "Ping time:"))
        self.tree_select.headerItem().setText(0, _translate("MainWindow", "1"))
        self.table_select.setSortingEnabled(True)
        item = self.table_select.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "groupe"))
        item = self.table_select.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nom"))
        item = self.table_select.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Online"))
        item = self.table_select.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "OS"))
        item = self.table_select.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Tag"))
        item = self.table_select.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Compare"))
        item = self.table_select.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Logged"))
        self.CommandesGroup.setTitle(_translate("MainWindow", "Commandes"))
        self.run_file_button.setText(_translate("MainWindow", "Run file"))
        self.run_cmd_button.setText(_translate("MainWindow", "Run cmd"))
        self.openfile_button.setText(_translate("MainWindow", "..."))
        self.no_wait.setText(_translate("MainWindow", "no wait"))
        self.time_out.setText(_translate("MainWindow", "time out (s)"))
        self.alias_button.setItemText(0, _translate("MainWindow", "Alias"))
        self.put_button.setText(_translate("MainWindow", "Put"))
        self.openfile_put_button.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "to"))
        self.groupBox.setTitle(_translate("MainWindow", "Comptes locaux"))
        self.label_2.setText(_translate("MainWindow", "name"))
        self.label_3.setText(_translate("MainWindow", "password"))
        self.admin_check.setText(_translate("MainWindow", "admin"))
        self.list_account_button.setText(_translate("MainWindow", "lister\n"
"les comptes\n"
"locaux"))
        self.chpwd_user_button.setText(_translate("MainWindow", "Changer password"))
        self.add_account_button.setText(_translate("MainWindow", "Ajouter compte"))
        self.list_groupe_button.setText(_translate("MainWindow", "Lister les groupes"))
        self.del_account_button.setText(_translate("MainWindow", "Supprimer compte"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Programmes"))
        self.label_4.setText(_translate("MainWindow", "filtre"))
        self.list_prog_button.setText(_translate("MainWindow", "Lister prog"))
        self.uninstall_prog_button.setText(_translate("MainWindow", "Uninstall prog"))
        self.ResultatGroup.setTitle(_translate("MainWindow", "Résultats"))
        self.compare_button.setText(_translate("MainWindow", "Compare"))
        self.seuil_label.setText(_translate("MainWindow", "seuil "))
        self.resultat_label.setText(_translate("MainWindow", "Résultat du poste"))
        self.resultat_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))

