import sublime, sublime_plugin
from .utils import *

class OpenWithGitBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        try:
            gitfile = GitFile(self.window.active_view().file_name())
            selection = self.window.active_view().sel()[0]
            if selection.a != selection.b:
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
            sublime.error_message(str(err))

class OpenWithGitBrowserFromSidebarCommand(sublime_plugin.WindowCommand):
    def run(self, paths = []):
        for path in paths:
            try:
                gitfile = GitFile(path)
                gitfile.open()
            except GitException as err:
                sublime.error_message(str(err))