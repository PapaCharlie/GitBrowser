from .hosts import hosts
import webbrowser, re, os, subprocess

class GitException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class GitFile:
    def __init__(self, filename):
        self.filename = filename
        if os.path.isdir(filename):
            self.cwd = self.filename
            self.isfile = False
        else:
            self.cwd = os.path.sep.join(self.filename.split(os.path.sep)[0:-1])
            self.isfile = True
        _, err, exitcode = self.git_command("config --get remote.origin.url")
        if exitcode != 0:
            raise GitException("\"%s\" is not inside a git directory!"%self.filename)
        self.remote = None
        self.branch = None
        self.commit = None
        self.root = None
        self.path = None
        self.host = None
        self.ref = None

    def git_command(self, command):
        git = subprocess.Popen('git %s'%command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = self.cwd)
        stdout = git.stdout.read().decode("UTF-8") if git.stdout else ''
        stderr = git.stderr.read().decode("UTF-8") if git.stderr else ''
        exitcode = git.poll()
        return stdout, stderr, exitcode

    def get_remote(self):
        if self.remote is None:
            self.remote = re.sub(r'\.git$', '', self.git_command("config --get remote.origin.url")[0].strip())
        return self.remote

    def get_branch(self):
        if self.branch is None:
            self.branch = branch = self.git_command("rev-parse --abbrev-ref HEAD")[0].strip()
        return self.branch

    def get_commit(self):
        if self.commit is None:
            self.commit = self.git_command("rev-parse HEAD")[0].strip()
        return self.commit

    def get_root(self):
        if self.root is None:
            self.root = self.git_command("rev-parse --show-toplevel")[0].strip()
        return self.root

    def get_path(self):
        if self.path is None:
            self.path = re.sub(r"^/", "", self.filename.replace(self.get_root(), ""))
        return self.path

    def get_host(self):
        if self.host is None:
            if self.get_remote().startswith("git@"):
                self.host = re.search(r"^git@(.+)", self.get_remote()).groups()[0].replace(":", "/")
            else:
                self.host = self.get_remote()
        return self.host

    def get_ref(self):
        if self.ref is None:
            self.ref = self.get_commit() if self.get_branch() == "HEAD" else self.get_branch()
        return self.ref

    def get_isfile(self):
        return self.isfile

    def open(self, selection = None):
        for host in hosts:
            h = host(self)
            if h.matches:
                webbrowser.open(h.format_url(selection))
                return
        raise GitException(remote + " is not a supported git host!")
