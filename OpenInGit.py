import sublime, sublime_plugin
import webbrowser, re, os, subprocess

class OpenInGitCommand(sublime_plugin.WindowCommand):
    def current_file(self):
        return self.window.active_view().file_name()

    def pwd(self):
        return os.path.sep.join(self.current_file().split(os.path.sep)[0:-1])

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
            path = re.sub(r"^/", "", self.current_file().replace(root, ""))

            ref = commit if branch == "HEAD" else branch
            if remote.startswith("git@"):
                slug = re.search(r"^git@(.+)", remote).groups()[0].replace(":", "/")
            else:
                slug = remote

            if "github" in slug.lower():
                url = "https://{slug}/blob/{ref}/{path}".format(slug = slug, ref = ref, path = path)
                print(ref)
                print(url)
                webbrowser.open(url)
            else:
                sublime.error_message(remote + " is not a supported git host!")
            # for region in self.window.active_view().sel():
            #     if region.a != region.b: # Selection not empty
            #         firstline = self.window.active_view().rowcol(region.a)[0] + 1
            #         lastline = self.window.active_view().rowcol(region.b)[0] + 1
            #     else:
            #         pass
        else:
            sublime.error_message("This is not inside a git directory!: " + err)

class OpenInGitFromSidebarCommand(sublime_plugin.WindowCommand):
    def run(self):
        pass
