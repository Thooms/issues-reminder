from daemonize import Daemonize
import itertools
import schedule
import time

class Reminder:
    def __init__(self, senders=[], fetchers=[]):
        self.senders = senders
        self.fetchers = fetchers

    def run(self):
        providers = [f.fetch() for f in self.fetchers]
        for sender in self.senders:
             sender.send(providers)

    def schedule(self, r, ev, unit):
        if unit == 'seconds':
            schedule.every(ev).seconds.do(r)
        elif unit == 'minutes':
            schedule.every(ev).minutes.do(r)
        elif unit == 'hours':
            schedule.every(ev).hours.do(r)
        elif unit == 'days':
            schedule.every(ev).days.do(r)

    def start_daemon(self):
        for sender in self.senders:
            ev, unit = sender.schedule_ev, sender.schedule_unit
            def r():
                providers = [f.fetch() for f in self.fetchers]
                sender.send(providers)
            self.schedule(r, ev, unit)

        def main_loop():
            while True:
                schedule.run_pending()
                time.sleep(1)

        pidfile = '/tmp/issues-reminder.pid'

        daemon = Daemonize(app='issues-reminder', pid=pidfile, action=main_loop)
        daemon.start()

    def test_run(self):
        for sender in self.senders:
            ev, unit = sender.schedule_ev, sender.schedule_unit
            def r():
                providers = [f.fetch() for f in self.fetchers]
                sender.send(providers)
            self.schedule(r, ev, unit)

        while True:
            schedule.run_pending()
            time.sleep(1)

