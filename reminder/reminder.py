import yaml

class Reminder:
    def __init__(self, settings_path='', senders_clss=[], fetcher_clss=[]):
        self.settings = yaml.load(open(settings_path))
        self.senders_clss = senders_clss
        self.fetcher = fetcher_clss[0](self.settings)

    def run(self):
        issues = self.fetcher.fetch()
        for cls in self.senders_clss:
            s = cls(self.settings, issues)
            s.send()
