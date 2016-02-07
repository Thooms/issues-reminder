from daemonize import Daemonize
import schedule
import time
import yaml

import fetchers
import reminder
import senders

if __name__ == '__main__':
    r = reminder.Reminder(
        'settings.yaml',
        senders_clss=[senders.SlackSender, senders.StdOutSender],
        fetcher_clss=[fetchers.GitHubFetcher]
    )

    settings = yaml.load(open('settings.yaml'))
    ev = settings['freq']['every']
    unit = settings['freq']['unit']

    if unit == 'seconds':
        schedule.every(ev).seconds.do(r.run)
    elif unit == 'minutes':
        schedule.every(ev).minutes.do(r.run)
    elif unit == 'hours':
        schedule.every(ev).hours.do(r.run)
    elif unit == 'days':
        schedule.every(ev).days.do(r.run)
    else:
        raise Exception('Bad time unit in settings.yaml')

    def main_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    pid = '/tmp/issues-reminder.pid'
    # use foreground=True for debugging
    daemon = Daemonize(app='issues-reminder', pid=pid, action=main_loop)
    daemon.start()
