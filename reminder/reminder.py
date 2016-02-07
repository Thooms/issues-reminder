import yaml

class Reminder:
    def __init__(self, settings_path='', senders=[], fetcher_clss=[]):
        self.settings = yaml.load(open(settings_path))
        self.senders = senders
        self.fetcher = fetcher_clss[0](self.settings)

    def run(self):
        issues = self.fetcher.fetch()
        for sender in self.senders:
             sender.send(issues)
