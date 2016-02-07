import yaml

class Reminder:
    def __init__(self, settings, senders=[], fetcher_clss=[]):
        self.settings = settings
        self.senders = senders
        self.fetcher = fetcher_clss[0](self.settings)

    def run(self):
        issues = self.fetcher.fetch()
        for sender in self.senders:
             sender.send(issues)
