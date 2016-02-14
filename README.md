
# Install

```
$ virtualenv -p `which python3` venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

# Usage

This software is made of 3 basic components, which you have to use to
build your own reminder.

## Imports

```
import fetchers
import reminder
import senders
```

## Fetchers

Those are the units that fetch project issues. There's currently only
one implemented, the `GitHubByOrgsFetcher`, which process the set of
issues in one or many GitHub organizations.

You define it like this:

```
gh_fetcher = fetchers.GitHubByOrgsFetcher(
        username='YourGitHubUsernale',
        token='YourGithubAccessToken',
        organizations=['A', 'List', 'Of', 'Organizations']
)
```

## Senders

Those are the units that output the list of issues fetched. Two of
them are provided for now.

### Send to Slack

You can use the `SlackSender` like this:

```
slack_sender = senders.SlackSender('YouSlackToken', ['#chan1', '#chan2'])
```

### Send by Mail

You can use the `MailSender` like this:

```
mail_sender = senders.MailSender('smtp.example.com', 'from@example.com', 'to@exemple.com')
```

### Print on terminal/send to file

You can use the `FileSender` like this:

```
stdout_sender = senders.FileSender(sys.stdout)
logfile_sender = senders.FileSender(open('myLogFile.log', 'w'))
```

## Gluing it all together

You have to use the `Reminder` class:

```
r = reminder.Reminder(
        senders=[stdout_sender, slack_sender, mail_sender],
        fetchers=[gh_fetcher],
        frequence=(5, 'seconds')
)
```

Then you can either use `r.run()` for a one-time run, or
`r.start_daemon()` to schedule it and start it as a background
process.
