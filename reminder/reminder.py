from daemonize import Daemonize
import itertools
import schedule
import time
import yaml

class Reminder:
    def __init__(self, senders=[], fetchers=[], frequence=None):
        self.senders = senders
        self.fetchers = fetchers
        self.frequence = frequence

    def run(self):
        providers = [f.fetch() for f in self.fetchers]
        for sender in self.senders:
             sender.send(providers)

    def start_daemon(self):
        if self.frequence is None:
            raise Exception('Insufficient information provided to run as daemon')

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

        def main_loop():
            while True:
                schedule.run_pending()
                time.sleep(1)

        pidfile = '/tmp/issues-reminder.pid'

        daemon = Daemonize(app='issues-reminder', pid=pidfile, action=main_loop)
        daemon.start()
