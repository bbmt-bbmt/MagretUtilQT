# -*- coding: utf-8 -*-

from UIPassword import Ui_Password
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import var_global
import resources
import logging

log = logging.getLogger(__name__)


class PasswordDialog(Ui_Password, QtWidgets.QDialog):
        def __init__(self):
            super().__init__()
            log.info("password dialog ouvert")
            # on initialise à partir de UI_Password
            self.setupUi(self)
            self.cancel_button.clicked.connect(self.reject)
            self.OK_button.clicked.connect(self.accept)
            self.password_input.setFocus()
            self.setWindowIcon(QtGui.QIcon(":/icones/app_icon"))
            try:
                self.login_input.setText(var_global.domaine['login'])
                self.dom_input.setText(var_global.domaine['name'])
            except KeyError:
                pass

        def get_result(self):
            return self.dom_input.text(), self.login_input.text(), self.password_input.text()
