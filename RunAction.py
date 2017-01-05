# -*- coding: utf-8 -*-

import util
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *
import logging

log = logging.getLogger(__name__)


class RunAction:
    def __init__(self, main_app):
        self.main_app = main_app
        self.dict_alias = util.lire_alias_ini()
        for key in self.dict_alias.keys():
            self.main_app.alias_button.addItem(key)
        return

    def on_run_cmd_button_clicked(self):
        log.info("run cmd cliqué")
        # on récupère la valeur des checkbox
        no_wait = self.main_app.no_wait.isChecked()
        time_out = None
        if self.main_app.time_out.isChecked():
            try:
                time_out = int(self.main_app.time_out_input.text())
            except ValueError:
                time_out = None
        cmd = self.main_app.cmd_input.text().strip()
        log.debug("run cmd cmd: %s timeout: %s no_wait: %s" % (cmd, time_out, no_wait))
        try:
            util.launch_worker_dialog(self.main_app, "run_remote_cmd", cmd, time_out, no_wait)
        except Warning:
            return
        return

    def on_run_file_button_clicked(self):
        log.info("run file cliqué")
        no_wait = self.main_app.no_wait.isChecked()
        time_out = None
        if self.main_app.time_out.isChecked():
            try:
                time_out = int(self.main_app.time_out_input.text())
            except ValueError:
                time_out = None

        # on recupere le nom du file et les parametres
        file = self.main_app.file_input.text().strip().split()
        param = " ".join(file[1:])
        try:
            file = file[0]
        except IndexError:
            util.Msg.show("Aucun fichier séléctionné")
            return
        log.debug("run file file: %s param: %s timeout: %s no_wait: %s" % (file, param, time_out, no_wait))
        try:
            util.launch_worker_dialog(self.main_app, "run_remote_file", file, param, time_out, no_wait)
        except Warning:
            return
        return

    def on_openfile_button_clicked(self):
        file = QFileDialog.getOpenFileName(None, "Run file", "", "exe (*.exe *.msi)")
        self.main_app.file_input.setText(file[0])
        return

    def on_openfile_put_button_clicked(self):
        file = QFileDialog.getOpenFileName(None, "Put file")
        self.main_app.put_src_edit.setText(file[0])
        return

    def on_put_button_clicked(self):
        log.info("put cliqué")
        # on recupere le nom du file
        file = self.main_app.put_src_edit.text().strip()
        directory = self.main_app.put_dest_edit.text().strip()
        if file == "" or directory == "":
            util.Msg.show("Remplir toues les cases")
            return
        try:
            util.launch_worker_dialog(self.main_app, "put", file, directory)
        except Warning:
            return
        return

    def on_alias_button_indexChanged(self, text):
        try:
            options = self.dict_alias[text].keys()
        except KeyError:
            return
        log.info("alias cliqué: %s" % options)
        try:
            if self.dict_alias[text]["no_wait"].lower() == "true":
                self.main_app.no_wait.setCheckState(Qt.Checked)
        except KeyError:
            self.main_app.no_wait.setCheckState(Qt.Unchecked)
        try:
            self.main_app.time_out_input.setText(self.dict_alias[text]["time_out"])
            self.main_app.time_out.setCheckState(Qt.Checked)
        except KeyError:
            self.main_app.time_out_input.setText("")
            self.main_app.time_out.setCheckState(Qt.Unchecked)

        if "cmd" in options:
            self.main_app.cmd_input.setText(self.dict_alias[text]["cmd"])
            self.on_run_cmd_button_clicked()
        if "file" in options:
            self.main_app.file_input.setText(self.dict_alias[text]["file"])
            self.on_run_file_button_clicked()
        self.main_app.alias_button.setCurrentIndex(0)
        return
