import sublime, sublime_plugin
import webbrowser, re, os, subprocess

class OpenInGitCommand(sublime_plugin.WindowCommand):
    def pwd(self):
        return os.path.sep.join(self.window.active_view().file_name().split(os.path.sep)[0:-1])

    # Returns the stdout, the stderr and the exit code
    def git_command(self, command):
        git = subprocess.Popen('git %s'%command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = self.pwd())
        stdout = git.stdout.read().decode("UTF-8") if git.stdout else ''
        stderr = git.stderr.read().decode("UTF-8") if git.stderr else ''
        exitcode = git.poll()
        return stdout, stderr, exitcode

    def run(self):
        remote, err, exitcode = self.git_command("config --get remote.origin.url")
        if not exitcode:
            remote = re.sub(r'\.git$', '', remote.rstrip())
            branch = self.git_command("rev-parse --abbrev-ref HEAD")[0].rstrip()
            commit = self.git_command("rev-parse HEAD")[0].rstrip()
            root = self.git_command("rev-parse --show-toplevel")[0].rstrip()
            if "github" in remote.lower():
                
            for region in self.window.active_view().sel():
                if region[0] != region[1]: # Selection not empty
                    firstline = self.window.active_view().rowcol(region.a)[0] + 1
                    lastline = self.window.active_view().rowcol(region.b)[0] + 1
                else:
                    pass
        else:
            sublime.error_message("This is not inside a git directory!: " + err)
