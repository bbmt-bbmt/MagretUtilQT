# -*- coding: utf-8 -*-

import configparser
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtCore import *
import difflib
import var_global
from Machine import Machine
import multiprocessing
from ProcessWorker import ProcessWorker
from ProgressDialog import ProgressDialog, ProgressDialogThread
import time
from collections import OrderedDict
import logger
import logging

log = logging.getLogger(__name__)


def get_subtree_nodes(tree_widget_item):
    """ retourne tous les QTreeWidgetItems sous la racine"""
    nodes = [tree_widget_item]
    for i in range(tree_widget_item.childCount()):
        nodes.extend(get_subtree_nodes(tree_widget_item.child(i)))
    return nodes


def get_all_items(tree_widget):
    """retourne tous les items d'un QTreeWidget"""
    all_items = []
    for i in range(tree_widget.topLevelItemCount()):
        top_item = tree_widget.topLevelItem(i)
        all_items.extend(get_subtree_nodes(top_item))
    return all_items


class Msg:
    """permet d'afficher un message avec un niveau d'information"""
    @staticmethod
    def show(text, level="information"):
        if level == "critical":
            qlevel = QMessageBox.Critical
        elif level == "warning":
            qlevel = QMessageBox.Warning
        else:
            qlevel = QMessageBox.Information
        msg_box = QMessageBox()
        msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        msg_box.setText(text)
        msg_box.setIcon(qlevel)
        msg_box.exec()


def init_conf(fichier):
    log.info("initialisation du fichier conf")
    """ Retourne les variables necessaire pour le fonctionnement retourne un
    dictionnaire {nom_groupe:nbre_poste}"""
    try:
        config = configparser.ConfigParser()
        config.read(fichier, encoding="utf-8-sig")
    except configparser.Error:
        Msg.show("Erreur lors de l'initialisation du fichier ini", "critical")
        raise SystemExit(0)

    groupes_dict = {'GroupesMagret': {}, 'Groupes': {}, 'GroupesFile': {}}
    domaine = {}
    try:
        try:
            for groupe in config['GroupesMagret']:
                num_poste = config['GroupesMagret'][groupe].split('-')[1]
                try:
                    nbre_poste = int(num_poste[1:])
                except ValueError:
                    nbre_poste = 0
                if nbre_poste != 0:
                    groupes_dict['GroupesMagret'][groupe.upper()] = nbre_poste
        except KeyError:
            pass

        try:
            for groupe in config['Groupes']:
                groupes_dict['Groupes'][groupe.upper()] = config['Groupes'][groupe]
        except KeyError:
            pass

        try:
            groupes_dict['GroupesFile']['file'] = config['GroupesFile']['file'] 
        except KeyError:
            pass

    except Exception as e:
        Msg.show('Erreur de lecture du fichier config', "warning")
        raise e
    domaine['name'] = config.get('Domaine', 'domaine', fallback=None)
    domaine['login'] = config.get('Domaine', 'login', fallback=None)
    var_global.domaine = domaine

    var_global.debug_level = getattr(logging, config.get('Debug', 'level', fallback='info').upper())

    # une fois le fichier config lu, on crée une variable global (pas bien)
    # qui contient les noms des groupes + le nom des machines + les machines crées

    # [GroupesMagret]
    for ini_salle, nbre in groupes_dict['GroupesMagret'].items():
        # on reécrit le nom des machines
        num = len(str(nbre)) if nbre >= 10 else 2
        str_template = '%s-P%0--i'.replace('--', str(num))
        names_machines = [str_template % (ini_salle, i) for i in range(1, nbre+1)]
        machines = {Machine(name, ini_salle) for name in names_machines}
        var_global.groupe_names[ini_salle] = names_machines
        var_global.dict_machines.update({(m.groupe, m.name): m for m in machines})

    # [Groupes]
    for ini_groupe, list_machines in groupes_dict['Groupes'].items():
        list_machines = list_machines.split(',')
        machines = {Machine(name, ini_groupe) for name in list_machines}
        var_global.groupe_names[ini_groupe] = list_machines
        var_global.dict_machines.update({(m.groupe, m.name): m for m in machines})

    # [GroupesFile]
    try:
        file = open(groupes_dict['GroupesFile']['file'], encoding="utf-8-sig", errors='replace')
        for line in file:
            list_name = line.strip(" \n,").split(',')
            if list_name[1:]:
                machines = {Machine(name, list_name[0]) for name in list_name[1:]}
                var_global.groupe_names[list_name[0]] = list_name[1:]
                var_global.dict_machines.update({(m.groupe, m.name): m for m in machines})
    except FileNotFoundError:
        Msg.show(fichier + ": Fichier csv introuvable", "warning")
    except KeyError:
        pass
    log.debug("init conf: dict_machine: %s groupe_name: %s domaine: %s" % 
              (var_global.dict_machines, var_global.groupe_names, var_global.domaine))
    return


def get_selected_machines(mainapp, etat="on"):
    mainapp.table_select.mutex.lock()
    selected_name = []
    for i in range(0, mainapp.table_select.rowCount()):
        if mainapp.table_select.item(i, 1).checkState() == Qt.Unchecked:
            continue
        if etat == "all":
            selected_name.append((mainapp.table_select.item(i, 0).text(), mainapp.table_select.item(i, 1).text()))
        elif mainapp.table_select.item(i, 2).text() != "0":
            selected_name.append((mainapp.table_select.item(i, 0).text(), mainapp.table_select.item(i, 1).text()))

    mainapp.table_select.mutex.unlock()
    select_machines = {key: m for key, m in var_global.dict_machines.items() if
                       key in selected_name}
    log.debug("machines selectionnées: %s" % str(select_machines.keys()))
    if len(select_machines) == 0:
        Msg.show("Aucune machine allumée selectionnée")
        raise Warning
    return select_machines


def del_messages(main_app):
    for message in main_app.machines_results.values():
        message['error'] = ''
        message['result'] = ''
    return


def score_str(str1, str2):
    score = difflib.SequenceMatcher(None, str1.strip(), str2.strip()).ratio() * 100
    return score


def check_errors(dict_machines, main_app):
    # si une machine a un message d'erreur
    # on met item_online en rouge
    for key in dict_machines.keys():
        if main_app.machines_results[key]['error'] != "":
            main_app.set_item_error(main_app.table_select.dict_items[key])
    return


def launch_worker_dialog(main_app, methode, *args, selected_machines=None, etat="on"):
    if selected_machines is None:
        selected_machines = get_selected_machines(main_app, etat)
    main_app.reset_compare()
    # on efface les vieux resultats
    del_messages(main_app)
    # on lance le process qui lancera les threads pour chaque machine
    dialog_queue = multiprocessing.Queue()
    log_queue = logger.log_queue
    w = ProcessWorker(log_queue, dialog_queue, selected_machines, methode, *args)
    log.info("sous process lancé")
    w.start()
    # on lance la fenetre et le thread progressdialog pour mettre à jour le process courant
    # et avoir un affichage de la progression
    progress_dialog = ProgressDialog(dialog_queue, selected_machines, main_app)
    dialog_thread = ProgressDialogThread(progress_dialog)
    dialog_thread.start()
    result = progress_dialog.exec()
    w.join(5)
    # on kill le process lancer
    if w.is_alive():
        w.terminate()
    log.info("sous process terminé")
    # pour que la queue ait le temps de se terminer proprement
    # sans provoquer d'erreur à la sortie de la fonction
    time.sleep(0.5)
    set_focus_item(main_app, selected_machines)
    if result == QDialog.Rejected:
        raise Warning
    return


def set_focus_item(main_app, selected_machines):
    item = list(selected_machines)[0]
    main_app.table_select.setCurrentItem(main_app.table_select.dict_items[item])
    main_app.table_select.itemClicked.emit(main_app.table_select.dict_items[item])
    return


def lire_alias_ini():
    """lit le fichier alias.ini et retourne
un dict{'alias': {'cmd':'commande','option':valeur}}
les options sont facultatives
"""
    try:
        config = configparser.ConfigParser()
        config.read("alias.ini", encoding="utf-8-sig")
    except configparser.Error as c:
        log.critical("erreur lors de l'initialisation du fichier alias.ini: %s" % c)
        raise SystemExit(0)

    dict_alias = {}
    # commandes_name = {"select", "selected", "update", "users", "run",
    #                   "result", "prog", "cmp", "flush", "put", "wol",
    #                   "shutdown", "vnc", "help", "errors", "password",
    #                   "tag", "quit"}

    try:
        dict_alias = {nom: dict(config.items(nom)) for nom in config.sections()}
    except Exception:
        Msg.show("Erreur de lecture du fichier d'alias")
    ordre_dict = OrderedDict(sorted(dict_alias.items()))
    return ordre_dict


def get_row(item, main_app):
    row = main_app.table_select.row(item)
    online_item = main_app.table_select.item(row, 2)
    osversion_item = main_app.table_select.item(row, 3)
    tag_item = main_app.table_select.item(row, 4)
    logged_item = main_app.table_select.item(row, 6)
    return {'name': item, 'online': online_item, 'osversion': osversion_item, 'tag': tag_item, "logged": logged_item}
