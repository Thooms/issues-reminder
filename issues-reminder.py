import sys
import yaml

import fetchers
import reminder
import senders

if __name__ == '__main__':
    settings = yaml.load(open('settings.yaml'))

    gh_fetcher = fetchers.GitHubByOrgsFetcher(settings)
    slack_sender = senders.SlackSender(settings)
    stdout_sender = senders.FileSender(settings, sys.stdout)

    r = reminder.Reminder(
        settings,
        senders=[stdout_sender, slack_sender],
        fetchers=[gh_fetcher],
        frequence=(5, 'seconds')
    )

    r.start_daemon()
