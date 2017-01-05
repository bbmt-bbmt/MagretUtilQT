# -*- coding: utf-8 -*-

import logging
import logging.handlers
from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from UILog import Ui_log_dialog
import re
# classe qui initialise le logger pour le process courant et
# qui lance un thread qui va permettre de logger les autres processus


# variable qui permet de fixer la queue utiliser par le logger
# utile pour le passer aux autre process
log_queue = None


class LogListenerThread(Thread):
    def __init__(self, level, log_queue, ui_log):
        super().__init__()
        self.log_queue = log_queue
        log_queue = log_queue
        root = logging.getLogger()
        h1 = logging.handlers.RotatingFileHandler('activity.log', 'a', 1000000, 1)

        h1.setLevel(level)
        h2 = QtHandler(ui_log)
        h2.setLevel(level)
        f = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
        h1.setFormatter(f)
        h2.setFormatter(f)
        root.addHandler(h1)
        root.addHandler(h2)
        root.setLevel(level)
        return

    def run(self):
        while True:
            try:
                record = self.log_queue.get()
                if record is None:
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except Exception as e:
                print("merde", e)
        return


class QtHandler(logging.Handler):
    """Permet d'envoyer les log dans une fenetre dediée: ui_log_dialog"""
    def __init__(self, ui_log):
        super().__init__()
        self.ui_log = ui_log
        self.ui_log.log_text_edit.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.ui_log.write_msg.emit(msg)


class ui_log_dialog(Ui_log_dialog, QtWidgets.QDialog):
    """fenetre qui va recevoir les log du logger"""
    write_msg = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.text = []
        self.stop_start_button.setText("Stop")
        self.write_msg.connect(self.write_text)
        self.regex_edit1.textChanged.connect(self.on_text_changed)
        self.regex_edit2.textChanged.connect(self.on_text_changed)
        self.stop_start_button.clicked.connect(self.on_stop_start_button_clicked)
        return

    def on_stop_start_button_clicked(self):
        if self.stop_start_button.text() == "Stop":
            self.write_msg.disconnect()
            self.stop_start_button.setText("Start")
        else:
            self.write_msg.connect(self.write_text)
            self.stop_start_button.setText("Stop")
        return

    def write_text(self, msg):
        self.error_label1.setText("")
        self.error_label2.setText("")
        if msg != "":
            self.text.append(msg)
        expression1 = self.regex_edit1.text().strip()
        expression2 = self.regex_edit2.text().strip()
        max_line = self.max_line.value()
        len_text = len(self.text)
        if len_text >= max_line:
            self.text = self.text[len_text - max_line+1:]
        if expression1 != "":
            try:
                text = [line for line in self.text if re.search(expression1, line)]
            except Exception:
                text = ""
                self.error_label1.setText('<span style=\" color:#ff0000;\">%s</span>' % "regex error")
            if expression2 != "":
                try:
                    text = [line for line in text if re.search(expression2, line)]
                except Exception:
                    text = ""
                    self.error_label2.setText('<span style=\" color:#ff0000;\">%s</span>' % "regex error")
        else:
            text = self.text
        self.log_text_edit.setPlainText("\n".join(text))
        self.log_text_edit.verticalScrollBar().setValue(self.log_text_edit.verticalScrollBar().maximum())
        return

    def on_text_changed(self, txt):
        self.write_text("")
        return
