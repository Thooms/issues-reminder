import schedule
import time
import yaml

import senders
import fetchers
import reminder

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

    while True:
        schedule.run_pending()
        time.sleep(1)
