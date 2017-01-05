# -*- coding: utf-8 -*-
import util
from UIAccount import Ui_Account
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from collections import OrderedDict
import var_global
import logging

log = logging.getLogger(__name__)


class AccountDialog(Ui_Account, QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        log.info("AccountDialog ouvert")
        # on initialise à partir de UI_Account
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.close_button.clicked.connect(self.reject)
        return

    def reject(self):
        # quand on appuie sur esc ou sur le boutton stop/close
        super().reject()


class AccountAction:
    def __init__(self, main_app):
        self.main_app = main_app
        return

    def on_add_account_button_clicked(self):
        log.info("add account lancé")
        account_name = self.main_app.account_name_input.text().strip()
        account_password = self.main_app.account_password_input.text().strip()
        if account_name == "" or account_password == "":
            util.Msg.show("Remplir toutes les cases")
            return
        is_admin = self.main_app.admin_check.isChecked()
        grpes = ['Administrateurs'] if is_admin else ['Utilisateurs']
        try:
            util.launch_worker_dialog(self.main_app, "add_user", account_name, account_password, grpes)
        except Warning:
            return
        return

    def on_chpwd_user_button_clicked(self):
        log.info("Chpwd lancé")
        account_name = self.main_app.account_name_input.text().strip()
        account_password = self.main_app.account_password_input.text().strip()
        if account_name == "" or account_password == "":
            util.Msg.show("Remplir toutes les cases")
            return
        try:
            util.launch_worker_dialog(self.main_app, "chpwd_user", account_name, account_password)
        except Warning:
            return
        return

    def on_list_account_button_clicked(self):
        log.info("list account lancé")
        try:
            util.launch_worker_dialog(self.main_app, "lister_users")
        except Warning:
            return

        # on affiche le résultat
        account_dialog = AccountDialog()
        html = ""
        header = ""
        title = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; text-decoration: underline; color:#0000ff;\">%s</span></p>\n"
        saut_ligne = "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
        debut_ligne = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        fin_ligne = "</p>\n"
        html_name = "<span style=\" font-size:10pt; font-weight:600;\">%s</span>"
        account_disable = "<span style=\" font-size:10pt;\">%s </span>"
        fleche = "<span style=\" font-size:10pt;\"> -&gt; </span>"
        account_enable = "<span style=\" font-size:10pt; font-weight:600; color:#00aa00;\">%s </span>"
        asterix = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">*</span>"
        end = ""
        html += header
        html_poste = ""
        sort_key = sorted(var_global.groupe_names)

        try:
            selected_machines = util.get_selected_machines(self.main_app)
        except Warning:
            # si aucune machine n'est selectionnée
            return
        log.debug("result_fct de list account: %s" % self.main_app.result_fct)
        # on crée le html
        for groupe in sort_key:
            titre_ecrit = False
            for name in var_global.groupe_names[groupe]:
                if (groupe, name) not in selected_machines.keys():
                    continue
                if not titre_ecrit:
                    # pour eviter que des groupes non selectionner s'affiche
                    html += title % groupe
                    html += saut_ligne
                    titre_ecrit = True
                html += debut_ligne
                html += html_name % name + fleche
                log.debug("list_account machines results lock")
                self.main_app.machines_results_mutex.lock()
                if self.main_app.machines_results[(groupe, name)]['error'] != "":
                    self.main_app.machines_results_mutex.unlock()
                    continue
                ordre_dict = OrderedDict(sorted(self.main_app.machines_results[(groupe, name)]['result'].items()))
                for user, info in ordre_dict.items():
                    etat, grpe = info
                    if 'Administrateurs' in grpe:
                        # le html_poste est mis dans le last_output_cmd pour pouvoir
                        # par la suite comparer les comptes facilement
                        html_poste += asterix
                    if etat == 'OK':
                        html_poste += account_enable % user
                    else:
                        html_poste += account_disable % user
                html += html_poste + fin_ligne
                self.main_app.machines_results[(groupe, name)]['result'] = html_poste
                self.main_app.machines_results_mutex.unlock()
                log.debug("list_account machines results unlock")
                html_poste = ''
            if titre_ecrit:
                html += saut_ligne
        html += end
        account_dialog.html_result.setHtml(html)
        account_dialog.exec()
        util.set_focus_item(self.main_app, selected_machines)
        return

    def on_del_account_button_clicked(self):
        log.info("del account lancé")
        account_name = self.main_app.account_name_input.text().strip()
        if account_name == "":
            util.Msg.show("Remplir la case name")
            return
        try:
            util.launch_worker_dialog(self.main_app, "del_user", account_name)
        except Warning:
            return
        return

    def on_list_groupe_button_clicked(self):
        account_name = self.main_app.account_name_input.text().strip()
        log.info("list groupe lancé sur %s" % account_name)
        if account_name == "":
            util.Msg.show("Remplir la case name")
            return
        try:
            util.launch_worker_dialog(self.main_app, "groupes_user", account_name)
        except Warning:
            return
        try:
            selected_machines = util.get_selected_machines(self.main_app)
        except Warning:
            # si aucune machine n'est selectionnée
            return
        log.debug("result de list groupe: %s" % self.main_app.machines_results)
        # on met le resultat dans last_output_cmd
        # pour pouvoir utiliser la comparaison si necessaire
        log.debug("list_group machines results lock")
        self.main_app.machines_results_mutex.lock()
        for key, m in selected_machines.items():
            if self.main_app.machines_results[key]["error"] != "":
                continue
            self.main_app.machines_results[key]["result"] = "\n".join(self.main_app.machines_results[key]["result"])
        self.main_app.machines_results_mutex.unlock()
        log.debug("list_group machines results unlock")
        util.set_focus_item(self.main_app, selected_machines)
        return
