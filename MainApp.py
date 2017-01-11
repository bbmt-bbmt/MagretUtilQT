# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui
from UIMagretUtil import Ui_MainWindow
import resources
from RunAction import RunAction
from AccountAction import AccountAction
from ProgAction import ProgAction
import re
import os
from PasswordDialog import PasswordDialog
import Privilege
import util
import time
import var_global
import shutil
import logging
import glob
from Ping import Ping
from logger import QtHandler

log = logging.getLogger(__name__)


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
        
    # on ajoute une signal
    # utiliser pour la classe ping pour mettre à jour l'affichage
    # dans le thread principal
    update_line_table = pyqtSignal(QtWidgets.QTableWidgetItem, str, str, str, str)

    def __init__(self, log_dialog=None):
        super().__init__()
        log.info("init main_app")
        self.setupUi(self)
        self.log_dialog = log_dialog

        # dictionnaire qui va permettre de stocker le résultat
        # des fonctions de machine pour l'affichage dans
        # des dialog spécifique
        self.result_fct_mutex = QMutex()
        self.result_fct = {}

        # dictionnaire qui va stocker le resultats et les erreurs des machines
        # {nom:{result:__,error:___}}
        self.machines_results_mutex = QMutex()
        self.machines_results = {}
        for key in var_global.dict_machines.keys():
            self.machines_results[key] = {'result': '', 'error': ''}

        # les differents slot regroupés dans des classes
        self.run_action = RunAction(self)
        self.account_action = AccountAction(self)
        self.prog_action = ProgAction(self)

        log.info("Péparation de l'interface")

        # on recupère les key du dict dans l'ordre pour l'affichage
        sort_key = sorted(var_global.groupe_names)

        # racine du tree
        tree_item0 = QtWidgets.QTreeWidgetItem(self.tree_select)
        tree_item0.setText(0, "Groupes de machines")
        tree_item0.setCheckState(0, Qt.Unchecked)
        tree_item0.setIcon(0, QtGui.QIcon(":/icones/groupe_ordi"))

        # current line permet de rajouter le nombre de ligne a tablewidget
        # au fur et à mesure de sa construction
        current_table_line = 0
        for groupe_name in sort_key:
            nbre = len(var_global.groupe_names[groupe_name])
            # on remplie treewidget
            self.table_select.setRowCount(current_table_line + nbre)
            tree_item1 = QtWidgets.QTreeWidgetItem(tree_item0)
            tree_item1.setText(0, groupe_name)
            tree_item1.setCheckState(0, Qt.Unchecked)
            tree_item1.setIcon(0, QtGui.QIcon(":/icones/groupe_ordi"))
            # on remplie tablewidget
            for name in var_global.groupe_names[groupe_name]:
                # item_groupe servira plus tard pour retrouver à quel groupe
                # appartient item_machine_name
                item_groupe = QtWidgets.QTableWidgetItem()
                item_groupe.setText(groupe_name)
                item_machine_name = QtWidgets.QTableWidgetItem()
                item_machine_name.setCheckState(Qt.Unchecked)
                item_machine_name.setText(name)
                item_machine_name.setIcon(QtGui.QIcon(":/icones/ordi"))
                item_online = QtWidgets.QTableWidgetItem()
                item_online.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                icon = QtGui.QIcon(":/icones/disable")
                item_online.setIcon(icon)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(Qt.NoBrush)
                item_online.setForeground(brush)
                item_online.setText('0')
                item_osversion = QtWidgets.QTableWidgetItem()
                item_osversion.setFlags(Qt.NoItemFlags)
                item_logged = QtWidgets.QTableWidgetItem()
                item_logged.setFlags(Qt.NoItemFlags)
                item_compare = QtWidgets.QTableWidgetItem()
                item_compare.setForeground(brush)
                item_compare.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                item_tag = QtWidgets.QTableWidgetItem()
                item_tag.setForeground(brush)
                item_tag.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                item_tag.setText("0")
                self.table_select.setItem(current_table_line, 0, item_groupe)
                self.table_select.setItem(current_table_line, 1, item_machine_name)
                self.table_select.setItem(current_table_line, 2, item_online)
                self.table_select.setItem(current_table_line, 3, item_osversion)
                self.table_select.setItem(current_table_line, 4, item_tag)
                self.table_select.setItem(current_table_line, 5, item_compare)
                self.table_select.setItem(current_table_line, 6, item_logged)
                current_table_line += 1

        # on cache la colonne groupe
        self.table_select.setColumnHidden(0, True)

        # on expand le tree pour voir tous les noms et
        # on adapte la table avec le contenu des colonnes
        self.tree_select.expandAll()
        self.table_select.horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

        # on initialise les différent comportment du tree et du table widget
        self.init_tree_select()
        self.init_table_select()

        log.info("Connection des différents signaux")
        # on connecte les différents signaux
        self.tree_select.itemChanged.connect(self.update_table_select)
        self.table_select.itemChanged.connect(self.update_tree_select)
        self.table_select.itemClicked.connect(self.on_item_clicked)
        # le reste utilise autoconnect et pyqtslot

        # connect pour la partie run du GUI à partir de la classe RunAction
        self.run_cmd_button.clicked.connect(self.run_action.on_run_cmd_button_clicked)
        self.cmd_input.returnPressed.connect(self.run_action.on_run_cmd_button_clicked)
        self.run_file_button.clicked.connect(self.run_action.on_run_file_button_clicked)
        self.openfile_button.clicked.connect(self.run_action.on_openfile_button_clicked)
        self.file_input.returnPressed.connect(self.run_action.on_run_file_button_clicked)
        self.openfile_put_button.clicked.connect(self.run_action.on_openfile_put_button_clicked)
        self.put_button.clicked.connect(self.run_action.on_put_button_clicked)
        self.alias_button.currentIndexChanged[str].connect(self.run_action.on_alias_button_indexChanged)

        # connect pour la partie account
        self.add_account_button.clicked.connect(self.account_action.on_add_account_button_clicked)
        self.chpwd_user_button.clicked.connect(self.account_action.on_chpwd_user_button_clicked)
        self.list_account_button.clicked.connect(self.account_action.on_list_account_button_clicked)
        self.del_account_button.clicked.connect(self.account_action.on_del_account_button_clicked)
        self.list_groupe_button.clicked.connect(self.account_action.on_list_groupe_button_clicked)

        # connect pour la partie prog
        self.list_prog_button.clicked.connect(self.prog_action.on_list_prog_button_clicked)
        self.uninstall_prog_button.clicked.connect(self.prog_action.on_uninstall_prog_button_clicked)

        self.ping = Ping(self)
        self.ping.daemon = False
        self.ping.start()
        return

    def init_tree_select(self):
        # on rajoute à l'objet deux proprietes
        # la liste des items et l'item racine
        list_items = util.get_all_items(self.tree_select)
        root_item = list_items[0]
        list_items = list_items[1:]
        dict_name_items = {item.text(0): item for item in list_items}
        self.tree_select.root_item = root_item
        self.tree_select.dict_name_items = dict_name_items
        return

    def init_table_select(self):
        # on ajoute 2 propriétés
        # un dict goupe-item et un compteur de box checker
        # un dict_item (groupe, nom):item
        list_items_name = [(self.table_select.item(i, 0).text(), self.table_select.item(i, 1))
                           for i in range(0, self.table_select.rowCount())]
        dict_groupe_items = {}
        for elmt in list_items_name:
            try:
                dict_groupe_items[elmt[0]] += (elmt[1],)
            except KeyError:
                dict_groupe_items[elmt[0]] = (elmt[1],)

        dict_items = {(self.table_select.item(i, 0).text(), self.table_select.item(i, 1).text()): self.table_select.item(i, 1)
                      for i in range(0, self.table_select.rowCount())}

        keys = var_global.groupe_names.keys()
        # compteur pour les checkbox par rapport au groupe
        check_count = {k: 0 for k in keys}
        self.table_select.check_count = check_count
        self.table_select.dict_items = dict_items

        # on ajoute un mutex, table_select étant accéder par différent thread
        self.table_select.mutex = QMutex()

        self.update_line_table.connect(self.on_update_line_table)
        return

    def update_table_select(self, current_item, i):
        # on bloque le signal et on pose un mutex
        # plusieur thread peuvent accedere au tablewidget
        # appeler lors d'un clique sur le tree
        self.table_select.blockSignals(True)
        log.debug("update_table_select lock and bloc table")
        self.table_select.mutex.lock()
        groupe = current_item.text(i)
        log.info("Tree item cliqué %s" % groupe)
        try:
            # si on coche une case dans le tree
            # on coche toutes les machines correspondant au groupe
            # dans la table et on met à jour le compteur de check dans la table
            for key, item in self.table_select.dict_items.items():
                # ne sert qu'a declancher le Key error si on clique sur la racine
                # à voir comment mieux faire
                var_global.groupe_names[groupe]
                if key[0] != groupe:
                    # si l'item n'est pas dans le groupe concerné on pass
                    continue
                item.setCheckState(current_item.checkState(i))
                self.table_select.check_count[groupe] = (len(var_global.groupe_names[groupe])
                                                         if current_item.checkState(i) == Qt.Checked else 0)
        except KeyError:
            # le key error c'est pour gerer l'item racine
            for g, listes in var_global.groupe_names.items():
                self.table_select.check_count[g] = (len(listes)
                                                    if current_item.checkState(i) == Qt.Checked else 0)
                for item_name in listes:
                    self.table_select.dict_items[(g, item_name)].setCheckState(current_item.checkState(i))
        self.table_select.mutex.unlock()
        self.table_select.blockSignals(False)
        log.debug("update_table_select unlock and unbloc table")
        # on met à jour les check box du tree select
        self.update_tree_widget(current_item)
        self.on_only_checkbox_clicked()
        return

    def update_tree_widget(self, current_item=None):
        """sert à mettre à jour le checkbox de la racine"""
        # il faut bloquer les signaux sinon à chaque changement fait 
        # dans la fonction on relance la fonction
        self.tree_select.blockSignals(True)
        # on recupere tous les items et on separe la racine du reste

        root_item = self.tree_select.root_item
        list_items = self.tree_select.dict_name_items.values()

        # a chaque click sur treewidget on parcourt tous pour mettre 
        # à jour l'état de la racine
        if current_item == root_item:
            if root_item.checkState(0) == Qt.Checked:
                for item in list_items:
                    item.setCheckState(0, Qt.Checked)
            if root_item.checkState(0) == Qt.Unchecked:
                for item in list_items:
                    item.setCheckState(0, Qt.Unchecked)
        else:
            check_count = 0
            partial_check_count = 0
            # on compte les items checker ou partialement checké
            for item in list_items:
                if item.checkState(0) == Qt.Checked:
                    check_count += 1
                if item.checkState(0) == Qt.PartiallyChecked:
                    partial_check_count += 1
            # on met à jour le checkbox de la racine
            if check_count == len(list_items):
                root_item.setCheckState(0, Qt.Checked)
            if check_count == 0:
                root_item.setCheckState(0, Qt.Unchecked)
            if 0 < check_count < len(list_items):
                root_item.setCheckState(0, Qt.PartiallyChecked)
            if partial_check_count != 0:
                root_item.setCheckState(0, Qt.PartiallyChecked)
            if root_item.checkState(0) == Qt.Checked:
                for item in list_items:
                    item.setCheckState(0, Qt.Checked)
        self.tree_select.blockSignals(False)
        return

    def update_tree_select(self, item):
        # appeler lors d'un clic sur la tablewidget
        log.info("Item cliqué %s" % item.text())
        self.tree_select.blockSignals(True)
        row = self.table_select.row(item)
        groupe = self.table_select.item(row, 0).text()
        # on met à jour le compteur pour savoir si
        # toutes les machines du groupe sont checker ou pas
        if item.checkState() == Qt.Checked:
            self.table_select.check_count[groupe] += 1
        else:
            self.table_select.check_count[groupe] -= 1

        # puis on met à jour le tree avec partial ou check
        # en fonction du compteur
        if self.table_select.check_count[groupe] == len(var_global.groupe_names[groupe]):
            self.tree_select.dict_name_items[groupe].setCheckState(0, Qt.Checked)
        elif self.table_select.check_count[groupe] == 0:
            self.tree_select.dict_name_items[groupe].setCheckState(0, Qt.Unchecked)
        else:
            self.tree_select.dict_name_items[groupe].setCheckState(0, Qt.PartiallyChecked)
        self.tree_select.blockSignals(False)
        # on rappelle cette fonction pour mettre à jour
        # les widget du tree en fonction des partial check
        self.update_tree_widget()
        self.on_only_checkbox_clicked()
        return

    @pyqtSlot()
    def on_check_uncheck_button_clicked(self):
        log.debug("on check uncheck lock table")
        self.table_select.mutex.lock()
        selected_items = self.table_select.selectedItems()
        for item in selected_items:
            if item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
        self.table_select.mutex.unlock()
        log.debug("on check uncheck unlock table")
        return

    @pyqtSlot()
    def on_ping_checkbox_clicked(self):
        if not self.ping_checkbox.isChecked():
            self.ping.pause = True
        else:
            try:
                i = int(self.ping_thread_edit.text())
            except ValueError:
                i = 10
                self.ping_thread_edit.setText(str(i))
            if self.ping.isFinished():
                self.ping = Ping(self, i)
                self.ping.daemon = False
                self.ping.start()
            else:
                self.ping.set_max_thread(i)
            self.ping.pause = False
        return

    @pyqtSlot()
    def on_kill_ping_button_clicked(self):
        util.Msg.show("Attention Killer le processus ping peut laisser des dossiers sur les machines\n"
                      "Ne pas oublier de lancer la commande clean")
        self.ping.ping_process.terminate()
        self.ping.terminate()
        self.ping_checkbox.setCheckState(Qt.Unchecked)
        self.ping_thread_edit.setEnabled(True)
        self.ping_time_label.setText("Ping killed")
        return

    @pyqtSlot()
    def on_inverse_button_clicked(self):
        log.debug("on inverse button lock table")
        self.table_select.mutex.lock()
        for item in self.table_select.dict_items.values():
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
        self.table_select.mutex.unlock()
        log.debug("on inverse button unlock table")
        return

    def on_update_line_table(self, item, online_text, tag_text, osversion_text, user_text):
        """appeler par le ping thread pour mettre à jour
        une ligne si une machine change d'etat"""
        log.info("Mise à jour de l' item %s" % item.text())
        self.table_select.blockSignals(True)
        log.debug("on update line table lock bloc table")
        self.table_select.mutex.lock()
        row = util.get_row(item, self)
        online_item = row['online']
        os_item = row['osversion']
        logged_item = row['logged']
        tag_item = row["tag"]

        online_item.setText(online_text)
        osversion = osversion_text
        os_item.setText(osversion)

        logged_item.setText(user_text)

        icon = QtGui.QIcon(":/icones/disable")
        # text = "0"
        if online_text == "1":
            icon = QtGui.QIcon(":/icones/enable")
            # text = "1"
        elif online_text == "2":
                icon = QtGui.QIcon(":/icones/error")
                # text = "2"
        online_item.setIcon(icon)

        icon = QtGui.QIcon()
        if online_text == "1" or online_text == "2":
            if tag_text == "1":
                icon = QtGui.QIcon(":/icones/enable")
            elif tag_text == "2":
                icon = QtGui.QIcon(":/icones/purple")
            elif tag_text == "3":
                    icon = QtGui.QIcon(":/icones/error")

        tag_item.setIcon(icon)
        tag_item.setText(tag_text)

        # obliger de tout parcourir car les lignes correspondant aux 
        # items peuvent changer (qt qui les changent)
        if self.only_checkbox.isChecked():
            for i in range(0, self.table_select.rowCount()):
                if self.table_select.item(i, 1).checkState() == Qt.Checked:
                    self.table_select.setRowHidden(i, False)
                else:
                    self.table_select.setRowHidden(i, True)
        else:
            for i in range(0, self.table_select.rowCount()):
                self.table_select.setRowHidden(i, False)

        self.table_select.horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
        self.table_select.horizontalHeader().setStretchLastSection(True)
        
        self.table_select.mutex.unlock()
        self.table_select.blockSignals(False)
        log.debug("on update line table unlock unbloc table")
        return

    @pyqtSlot()
    def on_wol_button_clicked(self):
        self.ping.pause = True

        while not (self.ping.ping_process_pause or self.ping.isFinished()):
            time.sleep(2)
        self.ping.enable_wmi_protect()
        if self.ping_checkbox.isChecked():
            self.ping.pause = False
        try:
            selected_machines = util.get_selected_machines(self, etat="all")
        except Warning:
            self.ping.disable_wmi_protect()
            return

        for m in selected_machines.values():
            m.wol()
            log.info("wol %s" % m.name)
        util.Msg.show("wol en cours sur %s machine(s)" % len(selected_machines))

        self.ping.disable_wmi_protect()
        return

    @pyqtSlot()
    def on_clean_button_clicked(self):
        log.info("Clean lancé")
        # on en profite pour effacer tous les input de l'interface
        self.cmd_input.setText("")
        self.file_input.setText("")
        self.put_src_edit.setText("")
        self.put_dest_edit.setText("")
        self.time_out_input.setText("")
        self.account_name_input.setText("")
        self.account_password_input.setText("")
        self.filter_input.setText("")

        util.del_messages(self)

        try:
            util.launch_worker_dialog(self, "clean")
        except Warning:
            return
        for f in os.listdir():
            if re.fullmatch(r'^todel[0-9]{1,4}[0-9|a-f]{32}$', f):
                shutil.rmtree(f, ignore_errors=True)
        return

    def set_item_error(self, item):
        """met en rouge l'item donné"""
        log.info("Item %s mis à rouge" % item.text())
        self.table_select.blockSignals(True)
        self.table_select.mutex.lock()
        row = self.table_select.row(item)
        col = self.table_select.column(item)
        online_item = self.table_select.item(row, col + 1)
        icon = QtGui.QIcon(":/icones/error")
        online_item.setIcon(icon)
        online_item.setText("2")
        self.table_select.mutex.unlock()
        self.table_select.blockSignals(False)
        return

    def set_item_OK(self, item):
        """met en rouge l'item donné"""
        log.info("Item %s mis à vert" % item.text())
        self.table_select.blockSignals(True)
        self.table_select.mutex.lock()
        row = self.table_select.row(item)
        col = self.table_select.column(item)
        online_item = self.table_select.item(row, col + 1)
        icon = QtGui.QIcon(":/icones/enable")
        online_item.setIcon(icon)
        online_item.setText("1")
        self.table_select.mutex.unlock()
        self.table_select.blockSignals(False)
        return

    @pyqtSlot(QtWidgets.QTableWidgetItem)
    def on_item_clicked(self, item):
        """permet d'afficher le résultat ou l'erreur d'une machine
        si on la selectionne dans la table"""
        log.info("Item %s cliqué" % item.text())
        if item in self.table_select.selectedItems() and len(self.table_select.selectedItems()) == 1:
            row = self.table_select.row(item)
            groupe_item = self.table_select.item(row, 0)
            groupe = groupe_item.text()
            name = item.text()
            self.resultat_label.setText("Résultat du poste " + name)
            self.resultat_text.setText(str(self.machines_results[(groupe, name)]["result"]))
            if self.machines_results[(groupe, name)]["error"] != "":
                self.resultat_text.setText(str(self.machines_results[(groupe, name)]["error"]))
        return

    @pyqtSlot()
    def on_compare_button_clicked(self):
        log.info("Comparaison lancé")
        try:
            selected_machines = util.get_selected_machines(self)
        except Warning:
            return

        if len(self.table_select.selectedItems()) != 1:
            return
        try:
            seuil = int(self.seuil.text())
        except ValueError:
            seuil = 100
        item = self.table_select.selectedItems()[0]
        row = self.table_select.row(item)
        groupe_item = self.table_select.item(row, 0)
        groupe = groupe_item.text()
        name = item.text()
        str_ref = self.machines_results[(groupe, name)]["result"]
        # on parcours dans ce sens pour avoir un ref sur l'item à modifier
        for key, item in self.table_select.dict_items.items():
            groupe, name = key
            if (groupe, name) in selected_machines.keys():
                row = self.table_select.row(item)
                compare_item = self.table_select.item(row, 5)
                str_cmp = self.machines_results[(groupe, name)]["result"]
                score = util.score_str(str_cmp, str_ref)
                self.table_select.blockSignals(True)
                self.table_select.mutex.lock()
                log.debug("comparaison score %s %s %s" % (item.text(), name, score))
                if score < seuil:
                    icon = QtGui.QIcon(":/icones/error")
                    compare_item.setText("1")
                else:
                    icon = QtGui.QIcon(":/icones/enable")
                    compare_item.setText("0")
                compare_item.setIcon(icon)
                self.table_select.blockSignals(False)
                self.table_select.mutex.unlock()
        return

    def reset_compare(self):
        log.info("Reset compare lancé")
        for i in range(0, len(self.table_select.dict_items)):
            compare_item = self.table_select.item(i, 5)
            icon = QtGui.QIcon()
            self.table_select.blockSignals(True)
            self.table_select.mutex.lock()
            compare_item.setIcon(icon)
            compare_item.setText("")
            self.table_select.blockSignals(False)
            self.table_select.mutex.unlock()
        return

    @pyqtSlot()
    def on_only_checkbox_clicked(self):
        if self.only_checkbox.isChecked():
            for item in self.table_select.dict_items.values():
                row = self.table_select.row(item)
                if item.checkState() == Qt.Unchecked:
                    self.table_select.setRowHidden(row, True)
                else:
                    self.table_select.setRowHidden(row, False)
        else:
            for i in range(0, len(self.table_select.dict_items)):
                self.table_select.setRowHidden(i, False)
        self.table_select.horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
        self.table_select.horizontalHeader().setStretchLastSection(True)
        return

    @pyqtSlot()
    def on_password_button_clicked(self):
        password_dialog = PasswordDialog()
        if password_dialog.exec():
            domaine, login, password = password_dialog.get_result()
            path = os.getcwd()
            try:
                Privilege.get_privilege(login, password, domaine, uac=True)
                self.ping.stop = True
                raise SystemExit(0)
            except OSError as o:
                util.Msg.show("Erreur lors de l'élevation de privilège: " + var_global.fix_str(o.strerror),
                              "critical")
                log.error("Erreur lors de l'élevation de privilège: " + var_global.fix_str(o.strerror))
                # on restaure le path
                os.chdir(path)
        return

    @pyqtSlot()
    def on_tag_button_clicked(self):
        log.info("Tag lancé")
        for f in glob.glob("tag_file_*"):
            os.remove(f)
        name_file = "tag_file_" + str(int(time.time()))
        tag_file = open(name_file, "w")
        tag_file.close()
        try:
            util.launch_worker_dialog(self, "put_tag", name_file)
        except Warning:
            return

        tag_file = open(name_file, "w")
        tag_file.close()
        return

    @pyqtSlot()
    def on_vnc_button_clicked(self):
        try:
            selected_machines = util.get_selected_machines(self)
        except Warning:
            return
        if len(selected_machines) != 1:
            util.Msg.show("Séléctionner qu'une seule machine")
            return
        machine = list(selected_machines.values())[0]
        log.info("Vnc lancé sur %s" % machine.name)
        process = QProcess()
        process.start('vnc\\vncviewer.exe /listen')
        machine.vnc_open(os.getenv('COMPUTERNAME'))
        util.Msg.show("close vnc")
        process.terminate()
        machine.vnc_close()
        return

    @pyqtSlot()
    def on_shutdown_button_clicked(self):
        # on active le wmi protect
        self.ping.pause = True
        while not (self.ping.ping_process_pause or self.ping.isFinished()):
            time.sleep(2)
        self.ping.enable_wmi_protect()
        if self.ping_checkbox.isChecked():
            self.ping.pause = False
        try:
            util.launch_worker_dialog(self, "shutdown")
        except Warning:
            return

        # on reactive le wmi
        self.ping.disable_wmi_protect()
        return

    @pyqtSlot()
    def on_log_button_clicked(self):
        self.log_dialog.show()
        return

    def closeEvent(self, event):
        # on cache pour que ping.wait ne soit pas visible
        self.hide()

        # on termine proprement les pings
        # pour eviter des erreurs
        self.ping.stop = True
        if self.ping.isRunning():
            self.ping.wait()

        # on reset les handler du logger pour eviter que des messages en attente
        # ne soit écrit dans le ui_dialog qui n'existera plus
        # pas terrible le qthandler devrait être ajouté dans cette classe et supprimer dans 
        # cette classe
        root = logging.getLogger()
        root.handlers = [h for h in root.handlers if type(h) != QtHandler]
        event.accept()
        return
