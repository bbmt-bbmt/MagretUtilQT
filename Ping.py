# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, QRunnable, QThreadPool
import pythoncom
import time
import var_global
import pathlib
import util
import logging
import wmi
import multiprocessing

log = logging.getLogger(__name__)


def get_etat(online, tag, osversion, user):
    if not online:
        online_text = "0"
    else:
        online_text = '1'

    local_path = pathlib.Path('.')
    try:
        tag_file_name = list(local_path.glob("tag_file_*"))[0].name
    except (IndexError, AttributeError):
        tag_file_name = ''

    if not online or tag is None:
        tag_text = "0"
    else:
        if tag_file_name == "":
            tag_text = "0"
        elif tag_file_name == tag:
            tag_text = "1"
        elif tag == "":
            tag_text = "3"
        # si on passe à la fonction un état et non pas le nom
        # d'un fichier on garde l'état (pas terrible)
        elif tag in "0123":
            tag_text = tag
        elif tag_file_name != tag:
            tag_text = "2"
        
    osversion_text = osversion or ""
    user_text = user
    return [online_text, tag_text, osversion_text, user_text]


class WorkerThread(QRunnable):
    """Classe qui va accomplir les ping"""
    def __init__(self, machine, protect_wmi, ping_queue):
        super().__init__()
        self.protect_wmi = protect_wmi
        self.machine = machine
        self.ping_queue = ping_queue
        return

    def run(self):
        pythoncom.CoInitialize()

        try:
            self.machine.init_mac_file()
            online = self.machine.ping()
            # il peut y avoir un blocage lorsque un ordi s'éteint au cours d'une requete wmi
            # avec protectwmi et shutdown time, je fais en sorte qu'aunce requete wmi ne soit faite
            # pendant 10s si l'application à positionne un shutdown
            if self.machine.mac is None and online and not self.protect_wmi:
                self.machine.init_mac_wmi()
            tag = osversion = user = None
            if online and not self.protect_wmi:
                try:
                    tag = self.machine.tag()
                    osversion = self.machine.osversion()
                    user = self.machine.logged_user()
                except wmi.x_wmi as w:
                    tag = osversion = user = ""
                    log_msg = self.machine.name + " erreur wmi: %s " % w.info
                    if w.com_error is not None:
                        log_msg += var_global.fix_str(w.com_error.strerror)
                # je protege ce code sensible pour pas que le thread plante
                except Exception as e:
                    tag = osversion = user = ""
                    log_msg = self.machine.name + " erreur wmi: %s " % e

            if not online:
                tag = user = ""

            new_etat = get_etat(online, tag, osversion, user)

        finally:
            pythoncom.CoUninitialize()
        self.ping_queue.put((self.machine.groupe, self.machine.name, new_etat))
        return


class ControlThread(QThread):
    # ce thread permet de faire le pool.clear pour
    # accelerer la fin du process qd on wol ou on shutdown
    # sans que le ping soit desactivé
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.stop = False
        return

    def run(self):
        while True:
            control = self.process.control_queue.get()
            if control == "pause_on":
                self.process.pause = True
                self.process.pool.clear()
            elif control == "pause_off":
                self.process.pause = False
            elif control == "wmi_protect_on":
                self.process.protect_wmi = True
            elif control == "wmi_protect_off":
                self.process.wmi_time = time.time()
            elif type(control) is int:
                self.process.pool.setMaxThreadCount(control)
            elif control is None:
                self.process.stop = True
                self.process.pool.clear()
                break


class PingWorker(multiprocessing.Process):
    def __init__(self, ping_queue, control_queue, dict_machines, max_thread=100):
        super().__init__()
        self.ping_queue = ping_queue
        self.control_queue = control_queue
        self.protect_wmi = False
        self.wmi_time = None
        self.dict_machines = dict_machines
        self.pool = None
        self.max_thread = max_thread
        self.pause = False
        self.stop = False
        return

    def run(self):
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(self.max_thread)
        control_thread = ControlThread(self)
        control_thread.start()
        while True:
            ping_time = time.time()
            if self.wmi_time:
                t = time.time() - self.wmi_time
                if t > 10:
                    self.protect_wmi = False
                    self.wmi_time = False
            for machine in self.dict_machines.values():
                w = WorkerThread(machine, self.protect_wmi, self.ping_queue)
                self.pool.start(w)
            self.pool.waitForDone()
            ping_time = time.time()-ping_time
            self.ping_queue.put("Ping time : %s s" % int(ping_time))
            if self.pause:
                self.ping_queue.put("pause_ok")
            while self.pause and not self.stop:
                time.sleep(2)
            if self.stop:
                control_thread.wait()
                break
        return


class Ping(QThread):

    def __init__(self, main_app, max_thread=100):
        super().__init__()
        self.stop = False
        self.pause = False
        self.ping_process_pause = False
        self.main_app = main_app
        self.ping_queue = multiprocessing.Queue()
        self.control_queue = multiprocessing.Queue()
        self.ping_process = PingWorker(self.ping_queue, self.control_queue, var_global.dict_machines, max_thread)
        return

    def enable_wmi_protect(self):
        log.info("wmi protect on")
        self.control_queue.put("wmi_protect_on")
        return

    def disable_wmi_protect(self):
        log.info("wmi protect on")
        self.control_queue.put("wmi_protect_off")
        return

    def set_max_thread(self, i):
        log.info("pingmax thread %s" % i)
        self.control_queue.put(i)
        return

    def run(self):
        log.info("Ping process lancé")
        self.ping_process.start()
        # pas terrible, le trhead ping manipule un element de l'interface
        self.main_app.ping_thread_edit.setEnabled(False)
        while not self.stop:
            # on initialise les adresses mac connu
            for m in var_global.dict_machines.values():
                if m.mac is None:
                    m.init_mac_file()
            result_ping = self.ping_queue.get()
            log.debug("result ping: %s" % str(result_ping))
            if self.pause:
                log.info("ping pause")
                self.control_queue.put("pause_on")
                while self.ping_queue.get() != "pause_ok":
                    continue
                self.ping_process_pause = True
                self.main_app.ping_thread_edit.setEnabled(True)
                while self.pause and not self.stop:
                    time.sleep(2)
                log.info("ping pause end")
                self.ping_process_pause = False
                if self.stop:
                    break
                self.main_app.ping_thread_edit.setEnabled(False)
                self.control_queue.put("pause_off")
            # si le process envoie un message time on l'affiche dans l'ui
            if "time" in result_ping:
                self.main_app.ping_time_label.setText(result_ping)
                continue
            *key, new_etat = result_ping
            key = tuple(key)
            # on recupere les infos de l'interface pour pouvoir les comparer
            row_item = util.get_row(self.main_app.table_select.dict_items[key], self.main_app)
            online_item_text = row_item["online"].text()
            osversion_item_text = row_item["osversion"].text()
            tag_item_text = row_item["tag"].text()
            logged_item_text = row_item["logged"].text()
            old_etat = [online_item_text, tag_item_text, osversion_item_text, logged_item_text]

            # si il y a une erreur sur la machine on modifie l"état avant de comparer
            if new_etat[0] == "1" and self.main_app.machines_results[key]['error'] != '':
                new_etat[0] = '2'
            # ce if sert à detecter si wmi est activé ou pas
            # pour ne pas changer l'affichage
            if new_etat[1:] == ["0", "", None]:
                new_etat[1:] = old_etat[1:]
            if old_etat != new_etat:
                self.main_app.update_line_table.emit(
                    self.main_app.table_select.dict_items[key], *new_etat)
        self.control_queue.put(None)
        self.ping_process.join(20)
        if self.ping_process.is_alive():
            log.info("ping process kill")
            self.ping_process.terminate()
        log.info("ping process end")
        return
