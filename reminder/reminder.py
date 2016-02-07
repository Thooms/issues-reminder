import itertools
import yaml

class Reminder:
    def __init__(self, settings, senders=[], fetchers=[]):
        self.settings = settings
        self.senders = senders
        self.fetchers = fetchers

    def run(self):
        providers = [f.fetch() for f in self.fetchers]
        for sender in self.senders:
             sender.send(providers)
