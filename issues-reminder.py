import senders
import fetchers
import reminder

if __name__ == '__main__':
    r = reminder.Reminder(
        'settings.yaml',
        senders_clss=[senders.SlackSender, senders.StdOutSender],
        fetcher_clss=[fetchers.GitHubFetcher]
    )
    r.run()
