import sublime
import sublime_plugin
from .utils import GitFile, GitException


class OpenWithGitBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        try:
            filename = self.window.active_view().file_name()
            if filename is not None:
                gitfile = GitFile(filename)
                selection = self.window.active_view().sel()[0]
                if selection.a != selection.b:
                    firstline = min(
                        self.window.active_view().rowcol(selection.a),
                        self.window.active_view().rowcol(selection.b)
                    )
                    lastline = max(
                        self.window.active_view().rowcol(selection.a),
                        self.window.active_view().rowcol(selection.b)
                    )
                    lastline = (lastline[0] - 1 if lastline[1] == 0
                                else lastline[0]) + 1
                    firstline = firstline[0] + 1
                    if firstline == lastline:
                        selection = (firstline,)
                    else:
                        selection = (firstline, lastline)
                else:
                    selection = None
                gitfile.open(selection)
            else:
                sublime.error_message("Cannot open this file!")
        except GitException as err:
            sublime.error_message(str(err))


class OpenWithGitBrowserFromSidebarCommand(sublime_plugin.WindowCommand):
    def run(self, paths=[]):
        for path in paths:
            try:
                gitfile = GitFile(path)
                gitfile.open()
            except GitException as err:
                sublime.error_message(str(err))
