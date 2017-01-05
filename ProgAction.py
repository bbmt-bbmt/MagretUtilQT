# -*- coding: utf-8 -*-

import util
import logging

log = logging.getLogger(__name__)


class ProgAction:
    def __init__(self, main_app):
        self.main_app = main_app
        return

    def on_list_prog_button_clicked(self):
        log.info("list prog lancé")
        filtre = self.main_app.filter_input.text().strip() or None

        try:
            util.launch_worker_dialog(self.main_app, "list_prog", filtre)
        except Warning:
            return

        title = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; text-decoration: underline; color:#0000ff;\">%s</span></p>\n"
        saut_ligne = "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
        debut_ligne = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        fin_ligne = "</p>\n"
        prog_msi = "<span style=\" font-size:10pt;color:#00aa00;\">%s</span>"
        prog_exe = "<span style=\" font-size:10pt;color:#ff0000;\">%s</span>"

        try:
            selected_machines = util.get_selected_machines(self.main_app)
        except Warning:
            # si aucune machine n'est selectionnée
            return
        # peut poser des pbm avec des char bizarre
        # log.debug("list prog result_fct: %s" % str(self.main_app.machines_results).encode("cp850", "replace").decode("cp850", "replace"))
        for key, m in selected_machines.items():
            try:
                log.debug("%s list_prog machines results lock" % m.name)
                self.main_app.machines_results_mutex.lock()
                prog32 = self.main_app.machines_results[key]["result"][0]
                prog64 = self.main_app.machines_results[key]["result"][1]
            except IndexError:
                prog32 = {}
                prog64 = {}
                log.error("%s erreur lors de la récupération à partir du registre" % m.name)
                
            finally:
                self.main_app.machines_results_mutex.unlock()
                log.debug("%s list_prog machines results unlock" % m.name)
            
            html32 = title % "Programmes 32 bits"
            html64 = title % "Programmes 64 bits"
            for prog in prog32.keys():
                if "msiexec" in prog32[prog].lower():
                    html32 += debut_ligne + prog_msi % prog + fin_ligne
                else:
                    html32 += debut_ligne + prog_exe % prog + fin_ligne

            for prog in prog64.keys():
                if "msiexec" in prog64[prog].lower():
                    html64 += debut_ligne + prog_msi % prog + fin_ligne
                else:
                    html64 += debut_ligne + prog_exe % prog + fin_ligne
            legende = title % "Légende"
            legende += debut_ligne + "les programmes en vert peuvent être désinstaller avec le boutton uninstall" + fin_ligne
            legende += debut_ligne + "les programmes en rouge doivent être désinstaller avec une commande spécifique " \
                                     "le boutton uninstall met la commande à lancer dans le résultat du poste" + fin_ligne + saut_ligne
            log.debug("%s list_prog machines results lock" % m.name)
            self.main_app.machines_results_mutex.lock()
            self.main_app.machines_results[key]["result"] = legende + html32 + saut_ligne + html64
            self.main_app.machines_results_mutex.unlock()
            log.debug("%s list_prog machines results unlock" % m.name)

        util.set_focus_item(self.main_app, selected_machines)
        return

    def on_uninstall_prog_button_clicked(self):
        filtre = self.main_app.filter_input.text().strip() or None
        log.info("uninstall lancé avec le filtre: %s" % filtre)
        try:
            util.launch_worker_dialog(self.main_app, "uninstall", filtre)
        except Warning:
            return
        return
