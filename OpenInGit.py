import sublime, sublime_plugin
import webbrowser, re, os, subprocess

class GitException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class GitFile:
    def __init__(self, filename):
        self.filename = filename
        self.cwd = os.path.sep.join(self.filename.split(os.path.sep)[0:-1])
        _, err, exitcode = self.git_command("config --get remote.origin.url")
        if exitcode != 0:
            raise GitException("This file/directory not inside a git directory!: " + err)

    # Returns the stdout, the stderr and the exit code
    def git_command(self, command):
        git = subprocess.Popen('git %s'%command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = self.cwd)
        stdout = git.stdout.read().decode("UTF-8") if git.stdout else ''
        stderr = git.stderr.read().decode("UTF-8") if git.stderr else ''
        exitcode = git.poll()
        return stdout, stderr, exitcode

    def open(self, selection = None):
        remote = re.sub(r'\.git$', '', self.git_command("config --get remote.origin.url")[0].strip())
        branch = self.git_command("rev-parse --abbrev-ref HEAD")[0].strip()
        commit = self.git_command("rev-parse HEAD")[0].strip()
        root = self.git_command("rev-parse --show-toplevel")[0].strip()
        path = re.sub(r"^/", "", self.filename.replace(root, ""))

        ref = commit if branch == "HEAD" else branch
        if remote.startswith("git@"):
            slug = re.search(r"^git@(.+)", remote).groups()[0].replace(":", "/")
        else:
            slug = remote

        if "github" in slug.lower():
            if selection:
                lines = "#" + ("L%d-L%d"%selection if len(selection) == 2 else "L%d"%selection)
            else:
                lines = ""
            url = "https://{slug}/blob/{ref}/{path}{lines}".format(slug = slug, ref = ref, path = path, lines =lines)
            webbrowser.open(url)
        elif "bitbucket" in slug.lower():
            if selection:
                lines = "#-" + ("%d:%d"%selection if len(selection) == 2 else "%d"%selection)
            else:
                lines = ""
            url = "https://{slug}/src/{ref}/{path}{lines}".format(slug = slug, ref = ref, path = path, lines =lines)
            webbrowser.open(url)
        else:
            raise GitException(remote + " is not a supported git host!")

class OpenInGitCommand(sublime_plugin.WindowCommand):
    def run(self):
        try:
            gitfile = GitFile(self.window.active_view().file_name())
            selection = self.window.active_view().sel()[0]
            if selection.a != selection.b: # Selection not empty
                firstline = self.window.active_view().rowcol(selection.a)
                lastline = self.window.active_view().rowcol(selection.b)
                lastline = (lastline[0] - 1 if lastline[1] == 0 else lastline[0]) + 1
                firstline = firstline[0] + 1
                if firstline == lastline:
                    selection = (firstline,)
                else:
                    selection = (firstline, lastline)
            else:
                selection = None
            gitfile.open(selection)
        except GitException as err:
            sublime.error_message(err.message)

class OpenInGitFromSidebarCommand(sublime_plugin.WindowCommand):
    def run(self, files = []):
        for f in files:
            try:
                gitfile = GitFile(f)
                gitfile.open()
            except GitException as err:
                sublime.error_message(err.message)
