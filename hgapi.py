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
    """Empty class representing command result"""
    pass

class Revision(object):
    """A representation of a revision.
    Available fields are:
        node, rev, author, branch, parents, date, tags, desc
    A Revision object is equal to any other object 
    with the same value for node
    """
    def __init__(self, json_log):
        """Create a Revision object from a JSON representation"""
        rev = json.loads(json_log)
        
        for key in rev.keys():
            self.__setattr__(key, unquote(rev[key]))
        self.rev = int(self.rev)
        if not hasattr(self, "parent"):
            self.parents = [int(self.rev)-1]
        else:
            self.parents = [int(p) for p in self.parents.split()]

    def __eq__(self, other):
        """Returns true if self.node == other.node"""
        return self.node == other.node

class Repo(object):
    """A representation of a Mercurial repository"""
    def __init__(self, path):
        """Create a Repo object from the repository at path"""
        self.path = path

    def __getitem__(self, rev):
        """Get a Revision object for the revision identifed by rev"""
        return self.revision(rev)

    def hg_command(self, *args):
        """Run a hg command in path and return the result.
        Throws on error."""    
        proc = Popen(["hg", "--cwd", self.path] + list(args), stdout=PIPE, stderr=PIPE)
        result = HgResult()
        result.out,result.err = [x.decode("utf-8") for x in  proc.communicate()]
        result.retcode = proc.returncode
        result.success = not result.retcode
        if not result.success: 
            cmd = (" ".join(["hg", "--cwd", self.path] + list(args)))
            raise Exception("Error running %s:\n\tErr: %s\n\tOut: %s\n\tExit: %s" % (
                    cmd,result.err, result.out, result.retcode))
        return result

    def hg_init(self):
        """Initialize a new repo"""
        res = self.hg_command("init")

    def hg_id(self):
        """Get the output of the hg id command (truncated node)"""
        res = self.hg_command("id", "-i")
        return res.out.strip("\n +")
        
    def hg_rev(self):
        """Get the revision number of the current revision"""
        res = self.hg_command("id", "-n")
        str_rev = res.out.strip("\n +")
        return int(str_rev)

    def hg_add(self, filepath):
        """Add a file to the repo"""
        self.hg_command("add", filepath)

    def hg_update(self, reference):
        """Update to the revision indetified by reference"""
        self.hg_command("update", str(reference))

    def hg_heads(self):
        """Gets a list with the node id:s of all open heads"""
        res = self.hg_command("heads","--template", "{node}\n")
        return [head for head in res.out.split("\n") if head]
        
    def hg_node(self):
        """Get the full node id of the current revision"""
        res = self.hg_command("log", "-r", self.hg_id(), "--template", "{node}")
        return res.out.strip()

    def hg_commit(self, message, user=None, files=["."], close_branch=False):
        """Commit changes to the repository."""
        userspec = "-u" + user if user else ""
        close = "--close-branch" if close_branch else ""
        res = self.hg_command("commit", "-m", message, close, 
                              userspec, *files)

    log_tpl = '\{"node":"{node|short}","rev":"{rev}","author":"{author}","branch":"{branch}", "parents":"{parents}","date":"{date|isodate}","tags":"{tags}","desc":"{desc|urlescape}"}'        

    def hg_log(self, identifier):
        """Get the identified revision as a json string"""
        res = self.hg_command("log", "-r", str(identifier), 
                              "--template", self.log_tpl)
        return res.out

    def revision(self, identifier):
        """Get the identified revision as a Revision object"""
        return Revision(self.hg_log(identifier))

