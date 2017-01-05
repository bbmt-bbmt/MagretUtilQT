# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from UIProgress import Ui_ProgressDialog
from PyQt5 import QtWidgets
import util
import logging

log = logging.getLogger(__name__)


class ProgressDialogThread(QThread):
    """Le thread qui communiquera avec le sous process des taches
    à travers la queue. Permet de mettre à jour le resultat 
    des machines pour le process principal"""
    def __init__(self, dialog):
        super().__init__()
        self.queue = dialog.queue
        self.selected_machine = dialog.selected_machine
        self.dialog = dialog
        return

    def run(self):
        log.info("progress dialog thread lancé")
        result = self.queue.get()
        while True and result is not None:
            # peut poser des pbm avec des char bizarre
            # log.debug("result reçu: %s" % str(result).encode("cp850", "replace").decode("cp850", "replace"))
            groupe, name, result, error = result
            log.debug("%s lock machines results" % name)
            self.dialog.main_app.machines_results_mutex.lock()
            self.dialog.main_app.machines_results[(groupe, name)]['result'] = result or ""
            self.dialog.main_app.machines_results[(groupe, name)]['error'] = error or ""
            self.dialog.main_app.machines_results_mutex.unlock()
            log.debug("%s unlock machines results" % name)
            self.dialog.progress_bar_update.emit(groupe, name)
            result = self.queue.get()
        log.info("progress dialog thread terminé")
        return


class ProgressDialog(Ui_ProgressDialog, QtWidgets.QDialog):
    """affiche la fenetre progressdialog et permet au thread
    de modifier la bar et les zones de texte"""
    progress_bar_update = pyqtSignal(str, str)

    def __init__(self, queue, selected_machine, main_app):
        super().__init__()
        self.queue = queue
        self.selected_machine = selected_machine
        self.main_app = main_app
        # sert pour la progressbar
        self.total = len(self.selected_machine)
        self.done = 0
        # on initialise à partir de UI_progressdialog
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)

        # on fait le lien avec les différent signaux
        self.progress_bar_update.connect(self.on_progress_bar_update)
        self.close_button.clicked.connect(self.accept)
        self.close_button.setDisabled(True)
        self.stop_button.clicked.connect(self.reject)
        self.stop_button.setFocus()

        # pour l'affichage des zones texte
        self.list_en_cours = []
        self.list_en_erreur = []
        for m in self.selected_machine.values():
            self.list_en_cours += (m.name,)
        self.en_cours.setText(" ".join(self.list_en_cours))
        return

    def accept(self):
        self.queue.put(None)
        util.check_errors(self.selected_machine, self.main_app)
        super().accept()
        return

    def reject(self):
        # quand on appuie sur esc ou sur le boutton stop/close
        self.queue.put(None)
        super().reject()

    def on_progress_bar_update(self, groupe, name):
        self.done += 1
        self.progress_bar.setValue(self.done*100 // self.total)
        # on met à jour les zones textes
        self.list_en_cours.remove(name)
        self.en_cours.setText(" ".join(self.list_en_cours))
        if self.main_app.machines_results[(groupe, name)]["error"] != "":
            self.list_en_erreur += (name,)
        self.errors.setText(" ".join(self.list_en_erreur))
        if self.done == self.total:
            self.stop_button.setDisabled(True)
            self.close_button.setEnabled(True)
            self.close_button.setFocus()
        return
