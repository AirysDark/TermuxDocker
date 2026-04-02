# -*- coding: utf-8 -*-
"""Implements the TermuxDocker command line interface."""

import os
import sys
from termuxdocker.msg import Msg
from termuxdocker.cmdparser import CmdParser
from termuxdocker.config import Config
from termuxdocker.container.localrepo import LocalRepository
from termuxdocker.cli import TermuxDockerCLI


class TMain:
    """Methods correspond directly to TermuxDocker CLI commands."""

    STATUS_OK = 0
    STATUS_ERROR = 1

    def __init__(self, argv):
        """Initialize variables"""
        self.argv = argv
        self.cmdp = None
        self.local = None
        self.cli = None

    def _prepare_exec(self):
        """Prepare configuration, parse and execute CLI"""
        self.cmdp = CmdParser()
        self.cmdp.parse(self.argv)

        allow_root = self.cmdp.get("--allow-root", "GEN_OPT")
        if not (os.geteuid() or allow_root):
            Msg().err("Error: do not run as root !")
            sys.exit(self.STATUS_ERROR)

        # Config file override
        conf_file = self.cmdp.get("--config=", "GEN_OPT")
        if conf_file:
            Config().getconf(conf_file)
        else:
            Config().getconf()

        # Verbosity / debug
        if self.cmdp.get("--debug", "GEN_OPT") or self.cmdp.get("-D", "GEN_OPT"):
            Config.conf['verbose_level'] = Msg.DBG
        elif self.cmdp.get("--quiet", "GEN_OPT") or self.cmdp.get("-q", "GEN_OPT"):
            Config.conf['verbose_level'] = Msg.MSG
        Msg().setlevel(Config.conf['verbose_level'])

        # Insecure flag
        if self.cmdp.get("--insecure", "GEN_OPT"):
            Config.conf['http_insecure'] = True

        # Repository override
        topdir = self.cmdp.get("--repo=", "GEN_OPT")
        if topdir:
            Config.conf['topdir'] = topdir

        # Initialize local repository
        self.local = LocalRepository()
        if not self.local.is_repo():
            if topdir:
                Msg().err("Error: invalid TermuxDocker repository:", topdir)
                sys.exit(self.STATUS_ERROR)
            else:
                Msg().out("Info: creating repo: " + Config.conf['topdir'],
                          l=Msg.INF)
                self.local.create_repo()

        # Initialize CLI
        self.cli = TermuxDockerCLI(self.local)

    def execute(self):
        """Command parsing and execution"""
        self._prepare_exec()
        cmds = {
            "search": self.cli.do_search, "help": self.cli.do_help,
            "images": self.cli.do_images, "pull": self.cli.do_pull,
            "create": self.cli.do_create, "ps": self.cli.do_ps,
            "run": self.cli.do_run, "version": self.cli.do_version,
            "rmi": self.cli.do_rmi, "mkrepo": self.cli.do_mkrepo,
            "import": self.cli.do_import, "load": self.cli.do_load,
            "export": self.cli.do_export, "clone": self.cli.do_clone,
            "protect": self.cli.do_protect, "rm": self.cli.do_rm,
            "name": self.cli.do_name, "rmname": self.cli.do_rmname,
            "verify": self.cli.do_verify, "logout": self.cli.do_logout,
            "unprotect": self.cli.do_unprotect, "rename": self.cli.do_rename,
            "showconf": self.cli.do_showconf, "save": self.cli.do_save,
            "inspect": self.cli.do_inspect, "login": self.cli.do_login,
            "setup": self.cli.do_setup, "install": self.cli.do_install,
            "tag": self.cli.do_tag, "manifest": self.cli.do_manifest,
        }

        # Help / version shortcuts
        if len(self.argv) == 1 or self.cmdp.get("-h", "GEN_OPT") or self.cmdp.get("--help", "GEN_OPT"):
            return self.cli.do_help(self.cmdp)

        if self.cmdp.get("-V", "GEN_OPT") or self.cmdp.get("--version", "GEN_OPT"):
            return self.cli.do_version(self.cmdp)

        # Command execution
        command = self.cmdp.get("", "CMD")
        if command in cmds:
            if self.cmdp.get("--help", "CMD_OPT"):
                Msg().out(cmds[command].__doc__)
                return self.STATUS_OK
            if command in ["version", "showconf"]:
                return cmds[command](self.cmdp)
            if command != "install":
                self.cli.do_install(None)
            exit_status = cmds[command](self.cmdp)
            if self.cmdp.missing_options():
                Msg().err("Error: syntax error at: %s" %
                          " ".join(self.cmdp.missing_options()))
                return self.STATUS_ERROR
            return exit_status

        Msg().err("Error: invalid command:", command, "\n")
        return self.STATUS_ERROR
