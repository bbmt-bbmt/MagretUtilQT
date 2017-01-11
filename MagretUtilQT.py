# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from MainApp import MainApp
import sys
import os
import Privilege
import traceback
import util
import var_global
import logger
import logging
import multiprocessing
import sip

# hack pour le multiprocessing sur win
# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking
if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen


def erreur_final(e_type, e_value, e_tb):
    log = logging.getLogger(__name__)
    if e_type == KeyboardInterrupt:
        raise SystemExit(0)
    print(''.join(traceback.format_exception(e_type, e_value, e_tb)))
    log.critical(''.join(traceback.format_exception(e_type, e_value, e_tb)))
    util.Msg.show(''.join(traceback.format_exception(e_type, e_value, e_tb)), 'critical')
    return


def main(args):
    # pour eviter le crach de python à la sortie avec python3.4
    sip.setdestroyonexit(False)
    sys.excepthook = erreur_final
    if sys.argv[1:]:
        try:
            os.chdir(sys.argv[1])
        except FileNotFoundError:
            pass

    if sys.argv[2:] and sys.argv[2] == "pass_uac":
        Privilege.pass_uac()
        raise SystemExit(0)

    app = QtWidgets.QApplication(args)
    # on crée le dossier mac si il n'exite pas
    try:
        if not os.path.isdir('mac'):
            os.mkdir('mac')
    except Exception:
        util.Msg.show("Erreur lors de la création du répertoire mac", "warning")

    # on lit le fichier conf.ini qui va initialiser les variable global
    util.init_conf("conf.ini")

    log_queue = multiprocessing.Queue()
    log_dialog = logger.ui_log_dialog()
    logger.log_queue = log_queue
    log_listenner_thread = logger.LogListenerThread(var_global.debug_level, log_queue, log_dialog)
    # log_listenner_thread.setDaemon(True)
    log_listenner_thread.start()

    main_app = MainApp(log_dialog)
    # pour eviter le crash de python3.4 on exit
    app.setActiveWindow(main_app)
    
    main_app.setWindowIcon(QtGui.QIcon(":/icones/app_icon"))
    main_app.setWindowTitle("MagretUtil")

    main_app.show()

    exit_result = app.exec_()
    
    log_queue.put_nowait(None)
    log_listenner_thread.join()

    # if main_app.ping.isRunning():
    # 	main_app.ping.wait()
    # 	print("fin du ping")
    # pour éviter le crash de python au cas ou ....
    # main_app.ping.ping_process.terminate()
    # main_app.ping.terminate()
    # del main_app.ping

    # pour éviter de faire crashe python qui va attendre que tous les widget 
    # de mainwindows soit détruit
    # del main_app
    # del app
    print("tout est cool?")
    return exit_result

if __name__ == "__main__":
    # c'est pour que pyinstaller marche bien
    multiprocessing.freeze_support()
    main(sys.argv)
