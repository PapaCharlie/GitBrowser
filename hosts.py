class Host:
    def __init__(self, gitfile):
        self.host = gitfile.get_host()
        self.branch = gitfile.get_branch()
        self.commit = gitfile.get_commit()
        self.path = gitfile.get_path()
        self.isfile = gitfile.get_isfile()
        self.ref = gitfile.get_ref()

    def matches(self, hostname):
        return hostname.lower() in self.host.lower() or self.host.lower() in hostname.lower()

    def format_url(self, selection = None):
        pass

class Github(Host):
    def __init__(self, gitfile):
        Host.__init__(self, gitfile)

    def format_url(self, selection = None):
        if self.isfile:
            if selection:
                lines = "#" + ("L%d-L%d"%selection if len(selection) == 2 else "L%d"%selection)
            else:
                lines = ""
            return "https://{host}/blob/{ref}/{path}{lines}".format(host = self.host, ref = self.ref, path = self.path, lines = lines)
        else:
            return "https://{host}/tree/{ref}/{path}".format(host = self.host, ref = self.ref, path = self.path)

class BitBucket(Host):
    def __init__(self, gitfile):
        Host.__init__(self, gitfile)

    def format_url(self, selection = None):
        if selection:
            lines = "#-" + ("%d:%d"%selection if len(selection) == 2 else "%d"%selection)
        else:
            lines = ""
        url = "https://{host}/src/{ref}/{path}{lines}".format(host = self.host, ref = self.ref, path = self.path, lines = lines)

hosts = [Github, BitBucket]
