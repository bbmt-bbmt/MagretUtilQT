# -*- coding: utf-8 -*-

import socket
import struct
import win32net
import win32netcon
import pywintypes
import wmi as WmiModule
import re
import os
import Psexec

from PyQt5.QtCore import QProcess
from var_global import fix_str

import logging

log = logging.getLogger(__name__)

REMOTE_PATH = 'c:\\'


def extract_prog(registrty_str):
    result_dict = {}
    progs = registrty_str.split("\n\n")
    for prog in progs:
        name = None
        uninstall = None
        lines = prog.split("\n")
        for line in lines:
            if "DisplayName" in line:
                name = " ".join(line.split()[2:])
            if "UninstallString" in line:
                uninstall = " ".join(line.split()[2:])
            if name and uninstall:
                result_dict[name] = uninstall
    return result_dict


class Machine:
    """Class qui représente un ordi et son état"""
    def __init__(self, name, groupe=None):
        self.name = name
        self.groupe = groupe
        self.mac = None
        self.os_version = None
        self._vnc_uid = None
        self.registry_open = False
        return

    def wol(self):
        """ wake on lan """
        mac = self.mac
        if mac is None:
            log.error("%s: L'adresse mac n'est pas défini" % self.name)
            return

        if len(mac) == 12:
            pass
        elif len(mac) == 12 + 5:
            sep = mac[2]
            mac = mac.replace(sep, '')
        else:
            log.error("%s format d'adresse mac incorrect" % self.name) 
            return

        # Construction du paquet magique
        data = ''.join(['FFFFFFFFFFFF', mac * 16])
        send_data = b''

        for i in range(0, len(data), 2):
            send_data = b''.join([send_data,
                                  struct.pack('B', int(data[i: i + 2], 16))])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(('192.168.1.20',0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, ('<broadcast>', 0))
        sock.sendto(send_data, ('<broadcast>', 7))
        sock.sendto(send_data, ('<broadcast>', 9))
        return

    def shutdown(self):
        process = QProcess()
        process.start("shutdown /m \\\\" + self.name + " /s /f /t 0")
        process.waitForFinished()
        return

    def run_remote_cmd(self, cmd, timeout=None, no_wait_output=False):
        """Lance une commande dos sur la machine
        Utilise PsExec """
        try:
            _psexec = Psexec.PsExec(self.name, REMOTE_PATH)

            result, output_data = _psexec.run_remote_cmd(cmd,
                                                         timeout,
                                                         no_wait_output)
            if result == 0:
                return fix_str(output_data)
            else:
                log.error("%s la commande %s n'a pas pu être lancé" % (self.name, cmd))
                return ""
        finally:
            # pour forcer le garbage collector à l'effacer
            _psexec = None
        return

    def run_remote_file(self, file, param,
                        timeout=None, no_wait_output=False):
        """Lance un fichier executable dos sur la machine
        Utilise PsExec """
        try:
            _psexec = Psexec.PsExec(self.name, REMOTE_PATH)
            result, output_data = _psexec.run_remote_file(file, param, timeout,
                                                          no_wait_output)
            if result == 0:
                return fix_str(output_data)
            else:
                log.error("%s le fichier %s n'a pas pu être lancé à distance" % (self.name, file))
        finally:
            _psexec = None
            pass
        return

    def clean(self):
        todel_files = self.run_remote_cmd("dir /B c:\\ ")
        for name in todel_files.split():
            if re.fullmatch(r'^todel[0-9]{1,4}[0-9|a-f]{32}$', name):
                self.run_remote_cmd('rd /s /q %s%s' % (REMOTE_PATH, name))
        return

    def _run_gui_file(self, local_file, login):
        """Permet de lancer un executable de la machine local avec
        les droits de l'utilisateur connecté et ainsi pouvoir interagir
        avec le bureau
        """
        # j'utilise schtask plutot que du wmi car l'implémentation avec wmi
        # repose sur la commande déprécié at
        process1 = QProcess()
        process1.start('schtasks /create /tn todel /tr "' + local_file + '" /s ' + self.name + ' /ru '
                       + login + ' /sc ONSTART /it /f')
        process1.waitForFinished()

        process2 = QProcess()
        process2.start('schtasks /run /tn todel /s ' + self.name + ' /i')
        process2.waitForFinished()

        process3 = QProcess()
        process3.start('schtasks /delete /tn todel /s ' + self.name + ' /f')
        process3.waitForFinished()
        return

    def _logged(self):
        """ Retourne le login de l'utilisateur connecté sur la machine
        pour pouvoir après le donner à run_gui_file
        """
        # try:
        wmi = WmiModule.WMI(self.name)
        user_logged = wmi.Win32_ComputerSystem()[0].UserName
        # except WmiModule.x_wmi as w:
        #         self.message_erreur += self.name + " erreur wmi: %s " % w.info
        #         if w.com_error is not None:
        #             self.message_erreur += fix_str(w.com_error.strerror)
        #         log.error("Logged %s %s" % (self.name, self.message_erreur))
        #         user_logged = None
        log.debug("%s user logged %s " % (self.name, user_logged))
        return user_logged

    def logged_user(self):
        try:
            user_logged = self._logged().split('\\')[1]
        except AttributeError:
            user_logged = ""
        return user_logged

    def vnc_open(self, computer_name):
        """ lance le serveur sur la machine après avoir copié tous les
        fichiers nécessaire
        """
        try:
            _psexec = Psexec.PsExec(self.name, REMOTE_PATH)
            self._vnc_uid = _psexec._get_uid()
            remote_directory = os.path.join(_psexec.remote_path, self._vnc_uid)
            vnc_file = ['vnc\\winvnc.exe', 'vnc\\UltraVNC.ini', 'vnc\\vnchooks.dll']

            for file in vnc_file:
                _psexec._net_copy(file, remote_directory)

            cmd_run = os.path.join(remote_directory, 'winvnc.exe')
            cmd_connect = os.path.join(remote_directory,
                                       "winvnc.exe -connect " + computer_name)

            login = self._logged()
            if login is not None:
                self._run_gui_file(cmd_run, login)
                self._run_gui_file(cmd_connect, login)
            else:
                log.warning("%s aucun utilisateur connecté" % self.name)
                self.vnc_close()
                raise Warning("%s aucun utilisateur connecté" % self.name)
        finally:
            _psexec = None
        return

    def vnc_close(self):
        """ Kill le server vnc de la machine
        """
        try:
            process = QProcess()
            process.start("taskkill /F /IM winvnc.exe /s  " + self.name)
            process.waitForFinished()
        finally:
            self._vnc_uid = None
        self.clean()
        return

    def put(self, file_path, dir_path):
        try:
            _psexec = Psexec.PsExec(self.name, REMOTE_PATH)
            _psexec._net_copy(file_path, dir_path)
        finally:
            _psexec = None
        return

    def ping(self):
        try:
            process = QProcess()
            process.start("ping.exe -n 1 -w 1000 -4 " + self.name)
            process.waitForFinished()
            result_ping = process.readAllStandardOutput()
            result_ping = bytes(result_ping).decode('cp850', errors='ignore')
            # recupere l'ip dans la réponse (allumé ou pas)
            # on ne peut pas tester reçus = 1, car lors l'host est injoignablre on recoit
            # quand meme un packet
            # on teste TTL=
            match_etat = re.search(r'TTL=', result_ping)
            etat = True if match_etat else False
        except (IndexError, AttributeError):
            etat = False
        log.debug("%s etat: %s" % (self.name, etat))
        return etat

    def osversion(self):
        # si deja fait on ne recommence pas
        if self.os_version is None:
            wmi = WmiModule.WMI(self.name)
            wmi_operating_system = wmi.Win32_OperatingSystem()[0]
            self.os_version = wmi_operating_system.Version
        log.debug("%s osversion: %s" % (self.name, self.os_version))
        return self.os_version

    def init_mac_file(self):
        # si ce n'est pas none c'est qu'on a deja l'adresse
        if self.mac is not None:
            return self.mac
        try:
            # si le fichier qui stocke l'adresse mac existe,
            # on tente de le récupérer
            with open('mac\\' + self.name + '.txt', 'r') as f:
                self.mac = f.readline().strip('\n')
        except FileNotFoundError:
            pass
        return self.mac

    def init_mac_wmi(self):
        # si ce n'est pas none c'est qu'on a deja l'adresse
        if self.mac is not None:
            return self.mac

        try:
            wmi = WmiModule.WMI(self.name)
            wmi_net_configs = wmi.Win32_NetworkAdapterConfiguration()
            for net_config in wmi_net_configs:
                if self.name == net_config.DnsHostName:
                    self.mac = net_config.MACAddress
        except WmiModule.x_wmi as w:
            log_msg = self.name + " erreur wmi: %s " % w.info
            if w.com_error is not None:
                log_msg += fix_str(w.com_error.strerror)
                log.error("%s %s" % (self.name, log_msg))
        # si l'adresse mac est trouvé on l'écrit dans un fichier
        # si le fichier n'existe pas
        if self.mac is not None:
            path = os.path.join('mac', self.name + '.txt')
            if os.path.isdir('mac') and not os.path.isfile(path):
                with open(path, 'w') as f:
                    f.write(self.mac)
        log.debug(self.name + " mac: %s" % self.mac)
        return self.mac

    def tag(self):
        name_tag_file = self.run_remote_cmd("dir /B c:\\tag_file_*")
        try:
            name_tag_file = re.search('tag_file_[\\d]*', name_tag_file).group(0)
        except (IndexError, AttributeError):
            name_tag_file = ''
        log.debug("%s tag: %s" % (self.name, name_tag_file))
        return name_tag_file

    def put_tag(self, file_name):
        self.run_remote_cmd("del c:\\tag_file_*")
        self.put(file_name, "c:\\")
        return

    def list_prog(self, filtre):
        result_prog32 = {}
        result_prog64 = {}
        registry32_str = self.run_remote_cmd("reg query HKLM\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall /s")
        registry64_str = self.run_remote_cmd("reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall /s")
        result_prog64 = extract_prog(registry64_str)
        if "rreur" in registry32_str:
            result_prog32 = result_prog64
            result_prog64 = {}
        else:
            result_prog32 = extract_prog(registry32_str)

        if filtre is not None:
            result_prog32 = {key: value for key, value in result_prog32.items()
                             if filtre.lower() in key.lower()}
            result_prog64 = {key: value for key, value in result_prog64.items()
                             if filtre.lower() in key.lower()}

        # # ce log debug peut poser pbm avec des char bizarre
        # # log.debug("%s prog32:%s prog64:%s" % (self.name, result_prog32, result_prog64))
        return result_prog32, result_prog64

    def lister_users(self):
        """liste les utilisateurs et retourne un tableau {nom_user:état}
        état peut être degraded ou ok suivant que le compte est activé ou non """
        decalage = len(self.name) + 1
        users_groupes = {}
        wmi = WmiModule.WMI(self.name)
        wmi_UserAccount = wmi.Win32_UserAccount(LocalAccount=True)
        users = [{user.Caption[decalage:]:user.status}
                 for user in wmi_UserAccount]
        users_groupes = {name: (etat, self.groupes_user(name)) for user in users for name, etat in user.items()}
        log.debug("%s users:%s" % (self.name, users_groupes))
        return users_groupes

    def groupes_user(self, user):
        """retourne un dict contenant la liste des groupes de user """
        groupes = []
        decalage = len(self.name) + 1
        wmi = WmiModule.WMI(self.name)
        wmi_UserAccount = wmi.Win32_UserAccount(Name=user, LocalAccount=True)
        if wmi_UserAccount:
            groupes = [groupe.Caption[decalage:]
                       for groupe in wmi_UserAccount[0].associators("Win32_GroupUser")]
        log.debug("%s groupes %s:%s" % (self.name, user, groupes))
        return groupes

    def add_user(self, login, password, groupes):
        parametre_user = {
            'name': login,
            'password': password,
            'flags': win32netcon.UF_NORMAL_ACCOUNT | win32netcon.UF_SCRIPT | win32netcon.UF_DONT_EXPIRE_PASSWD,
            'priv': win32netcon.USER_PRIV_USER
        }
        try:
            win32net.NetUserAdd(self.name, 1, parametre_user)
        except pywintypes.error as error:
            log_erreur = "Erreur lors de la création du compte "\
                         + login + " : " + fix_str(error.strerror)
            log.error("%s %s" % (self.name, log_erreur))
            raise Warning(log_erreur)

        for groupe in groupes:
            try:
                win32net.NetLocalGroupAddMembers(self.name, groupe, 3,
                                                 [{'domainandname': login}])
            except pywintypes.error as error:
                log_erreur = "Erreur lors de l'attribution du groupe "\
                             + groupe + " : " + fix_str(error.strerror)
                log.error("%s %s" % (self.name, log_erreur))
                raise Warning(log_erreur)
        return

    def del_user(self, login):
        """ Supprime le compte login de la machine"""
        try:
            win32net.NetUserDel(self.name, login)
        except pywintypes.error as error:
            log_erreur = "Erreur lors de la suppression de l'utilisateur "\
                         + login + " : " + fix_str(error.strerror)
            log.error("%s %s" % (self.name, log_erreur))
            raise Warning(log_erreur)
        return

    def chpwd_user(self, login, password):
        """Change le mot de passe du compte login """
        try:
            info = win32net.NetUserGetInfo(self.name, login, 3)
            info['password'] = password
            info['flags'] = info['flags'] | win32netcon.UF_DONT_EXPIRE_PASSWD
            win32net.NetUserSetInfo(self.name, login, 3, info)
        except pywintypes.error as error:
            log_erreur = "Erreur lors du changement de password de l'utilisateur "\
                         + login + " : " + fix_str(error.strerror)
            log.error("%s %s" % (self.name, log_erreur))
            raise Warning(log_erreur)
        return

    def uninstall(self, name):
        log.debug("Uninstall %s sur %s" % (name, self.name))
        prog_3264 = self.list_prog(name)
        prog = prog_3264[0].copy()
        prog.update(prog_3264[1])
        if len(prog) != 1 or not prog:
            log_error = ("erreur dans le nom du programme à desinstaller "
                         "le nom peut correspondre à plusieur programme ou le nom n'existe pas")
            log.error("%s %s" % (self.name, log_error))
            raise Warning(log_error)

        prog_name, cmd_uninstall = prog.popitem()
        log.debug("%s uninstall cmd %s" % (self.name, cmd_uninstall))
        if "msiexec" not in cmd_uninstall.lower():
            return cmd_uninstall
        else:
            try:
                uid_prog = re.findall(r"\{[a-zA-Z0-9-]*\}", cmd_uninstall)[0]
                self.run_remote_cmd("msiexec.exe /qn /x " + uid_prog, no_wait_output=True)
            except IndexError:
                log_error = "impossible de desinstaller le logiciel"
                log.error("%s %s" % (self.name, log_error))
                raise Warning(log_error)
        return


def main():
    pass

if __name__ == '__main__':
    main()
