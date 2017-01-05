# -*- coding: utf-8 -*-

import multiprocessing
import pythoncom
from PyQt5.QtCore import QRunnable, QThreadPool
import logging

class ProcessWorker(multiprocessing.Process):
    """permet de lancer un nouveau process qui lancera des threads
    pour executer la tache sur chaque machine
    puis mettre le resultat dans queue"""
    class WorkerThread(QRunnable):
        def __init__(self, queue, machine, methode_name, *args):
            super().__init__()
            self.machine = machine
            self.methode_name = methode_name
            self.args = args
            self.queue = queue
            return

        def run(self):
            pythoncom.CoInitialize()
            try:
                result = getattr(self.machine, self.methode_name)(*self.args)
                self.queue.put((self.machine.groupe, self.machine.name, result,""))
            except AttributeError:
                pass
            except Exception as e:
                # je protege le thread pour eviter que son plantage plante le process
                # et que plus aucune donnée ne soit envoyé dans la queue
                # progress dialog restera en attente alors que plus rien ne peut arriver
                self.queue.put((self.machine.groupe, self.machine.name, "", str(e)))
            finally:
                pythoncom.CoUninitialize()
            return

    def __init__(self, log_queue, dialog_queue, dict_machines, methode_name, *args):
        super().__init__()
        self.dialog_queue = dialog_queue
        self.log_queue = log_queue
        self.dict_machines = dict_machines
        self.methode_name = methode_name
        self.args = args
        self.pool = None
        return

    def run(self):
        # on configure le logger pour tout envoyer dans la queue
        # le données seront récupérées dans le thread du processus principal
        # dédié à ça
        qh = logging.handlers.QueueHandler(self.log_queue)
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        # on reset les handlers au cas ou lors du fork du process
        # le nouveau process herite de la config du process principal
        root.handlers = []
        root.addHandler(qh)
        log = logging.getLogger(__name__)
        log.info("Sous process traitement des taches machines créé")
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(100)
        for machine in self.dict_machines.values():
            w = self.WorkerThread(self.dialog_queue, machine, self.methode_name, *self.args)
            self.pool.start(w)
            log.info("thread %s lancé" % machine.name)
        self.pool.waitForDone()
        log.info("Sous process traitement des taches machines  terminé")
        return
