from __future__ import print_function, unicode_literals
from subprocess import Popen, STDOUT, PIPE
try:
    from urllib import unquote
except: #python 3
    from urllib.parse import unquote
import re
import os.path
import json #for reading logs
out = print
err = print

class HgResult(object):
    pass

class Revision(object):
    def __init__(self, json_log):
        rev = json.loads(json_log)
        
        for key in rev.keys():
            self.__setattr__(key, unquote(rev[key]))
        self.rev = int(self.rev)
        if not hasattr(self, "parent"):
            self.parents = [int(self.rev)-1]
        else:
            self.parents = [int(p) for p in self.parents.split()]

class Repo(object):
    def __init__(self, path):
        self.path = path

    def __getitem__(self, rev):
        return self.hg_log(rev)

    def hg_command(self, *args):
        """Run a hg command in path and return the result"""    
        proc = Popen(["hg", "--cwd", self.path] + list(args), stdout=PIPE, stderr=PIPE)
        result = HgResult()
        result.out,result.err = [x.decode("utf-8") for x in  proc.communicate()]
        result.retcode = proc.returncode
        result.success = not result.retcode
        if not result.success: print (" ".join(["hg", "--cwd", self.path] + list(args)))
        return result

    def hg_init(self):
        """Initialize a repo"""
        res = self.hg_command("init")
        if res.success:
            return True
        err("Error: ", res.out, res.err)
        return False


    def hg_id(self):
        res = self.hg_command("id", "-i")
        if res.success:
            return res.out.strip("\n +")
        err("Error: ", res.out, res.err)
        return False

    def hg_rev(self):
        res = self.hg_command("id", "-n")
        if res.success:
            str_rev = res.out.strip("\n +")
            return int(str_rev)
        err("Error: ", res.out, res.err)
        return False


    def hg_add(self, filepath):
        res  = self.hg_command("add", filepath)
        if res.success:
            return True
        err("Error: ", res.retcode, res.out, res.err)
        return False


    def hg_commit(self, message, user=None, files=["."]):
        userspec = "-u" + user if user else ""
        res = self.hg_command("commit", "-m", message, userspec,
                          *files)
        if res.success:
            return True
        err("Error: ", res.retcode, res.out, res.err)
        return False

    log_tpl = '\{"node":"{node|short}","rev":"{rev}","author":"{author}","branch":"{branch}", "parents":"{parents}","date":"{date|isodate}","tags":"{tags}","desc":"{desc|urlescape}"}'

    def hg_log(self, identifier):
        identifier = str(identifier)
        res = self.hg_command("log", "-r", identifier, "--template", self.log_tpl)
        if not res.success:
            err("Error: ", res.retcode, res.out, res.err)
            return False

        return Revision(res.out)

