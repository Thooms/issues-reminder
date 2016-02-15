from daemonize import Daemonize
import itertools
import schedule
import time

class Reminder:
    def __init__(self, senders=[], fetchers=[], frequence=None):
        self.senders = senders
        self.fetchers = fetchers
        self.frequence = frequence

    def run(self):
        providers = [f.fetch() for f in self.fetchers]
        for sender in self.senders:
             sender.send(providers)

    def run(self,sender):
        providers = [f.fetch() for f in self.fetchers]
        sender.send(providers)

    def start_daemon(self):
        if self.frequence is None:
            raise Exception('Insufficient information provided to run as daemon')
        elif type(self.frequence) is tuple:
            ev, unit = self.frequence

            if unit == 'seconds':
                schedule.every(ev).seconds.do(self.run)
            elif unit == 'minutes':
                schedule.every(ev).minutes.do(self.run)
            elif unit == 'hours':
                schedule.every(ev).hours.do(self.run)
            elif unit == 'days':
                schedule.every(ev).days.do(self.run)
            else:
                raise Exception('Bad unformation provided to run as daemon')

        elif type(self.frequence) is list:
            for sender, val in zip_longest(self.senders, self.frequence):
                if sender == None or val == None:
                    raise Exception('Size of senders list and frequence list aren\'t equal')
                ev, unit = val

            if unit == 'seconds':
                schedule.every(ev).seconds.do(self.run(sender))
            elif unit == 'minutes':
                schedule.every(ev).minutes.do(self.run(sender))
            elif unit == 'hours':
                schedule.every(ev).hours.do(self.run(sender))
            elif unit == 'days':
                schedule.every(ev).days.do(self.run(sender))
            else:
                raise Exception('Bad unformation provided to run as daemon')

        else:
            raise Exception('Bad information provided to run as deamon')

        def main_loop():
            while True:
                schedule.run_pending()
                time.sleep(1)

        pidfile = '/tmp/issues-reminder.pid'

        daemon = Daemonize(app='issues-reminder', pid=pidfile, action=main_loop)
        daemon.start()
