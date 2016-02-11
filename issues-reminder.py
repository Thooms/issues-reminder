import sys

import fetchers
import reminder
import senders

if __name__ == '__main__':
    gh_fetcher = fetchers.GitHubByOrgsFetcher(
        username='Thooms',
        token='fd34d109730ffb482ad9962ae829d9caa4e23f68',
        organizations=['Atilla-Learn', 'Atilla106']
    )
    slack_sender = senders.SlackSender('xoxb-20530661910-pnKWmRNf2ofvwzjNkrvmU9mx', ['#bot-test'])
    stdout_sender = senders.FileSender(sys.stdout)

    r = reminder.Reminder(
        senders=[stdout_sender, slack_sender],
        fetchers=[gh_fetcher],
        frequence=(5, 'seconds')
    )

    r.run()
