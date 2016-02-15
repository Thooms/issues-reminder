
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

Those are the units that fetch project issues.

### Fetch GitHub issues

It is used to fetch all the issues belonging to a list of
organizations.  You define it like this:

```
gh_fetcher = fetchers.GitHubByOrgsFetcher(
        username='YourGitHubUsernale',
        token='YourGithubAccessToken',
        organizations=['A', 'List', 'Of', 'Organizations']
)
```

### Fetch GitLab issues

It is used to fetch all the issues for a list of repository.

```
gl_fetcher = fetchers.GitLabByRepoFetcher(
    gitlab_url='https://gitlab.com',
    gitlab_token='YourGitLabToken',
    repos=['Thooms/metadata-ws', 'NameSpace/repo']
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
        fetchers=[gh_fetcher, gl_fetcher],
        frequence=(5, 'seconds')
)
```
Alternatively, you can precise separate frequencies for each sender. Note that the senders and linked frequencies must be in the same order.

```
r = reminder.Reminder(
        senders=[stdout_sender, slack_sender, mail_sender],
        fetchers=[gh_fetcher, gl_fetcher],
        frequence=[(5, 'seconds'), (7, 'days'), (2, 'hours')]
)
```

Then you can either use `r.run()` for a one-time run, or
`r.start_daemon()` to schedule it and start it as a background
process.
