from collections import defaultdict
from requests.auth import HTTPBasicAuth
from slacker import Slacker
from termcolor import colored
import requests
import yaml

class GitHubIssuesFetcher:
    def __init__(self, settings):
        self.settings = settings
        self.api_url = 'https://api.github.com/orgs/{}/issues'
        self.auth = HTTPBasicAuth(
            self.settings['github-username'],
            self.settings['github-token']
        )
        self.params = {'filter': 'all'}
        self.headers = {'Accept': 'application/vnd.github.v3+json'}

    def organize_issues(self, issues):
        d = defaultdict(list)
        for issue in issues:
            d[issue['repository_url']].append(issue)
        return d

    def fetch(self):
        """
        Fetches the raw issues data, and returns it organized it by
        organization/repo.
        """
        orgs = self.settings['github-organizations']
        res = []
        for url in (self.api_url.format(org) for org in orgs):
            req = requests.get(url, auth=self.auth, params=self.params, headers=self.headers)
            res.extend(req.json())

        return self.organize_issues(res)

class Sender:
    def __init__(self, settings, issues):
        self.issues = issues
        self.settings = settings

    def send(self):
        raise Exception('Please implement this method.')

class MailSender(Sender):
    def send(self):
        pass

class SlackSender(Sender):
    def send(self):
        slack = Slacker(self.settings['slack']['api-token'])
        slack.chat.post_message('#bot-test', self.slack_message())

    def slack_message(self):
        # This is ugly a.f. but it works fine.
        return 'Hello there, here are the open issues and pull requests of the week! :gift:\n{}'.format(
            '\n'.join([
                '\n\n• `{}` ({})\n{}'.format(
                    issues[0]['repository']['name'],
                    issues[0]['repository']['html_url'],
                    '\n'.join(['_{}_ ({})'.format(
                        issue['title'],
                        issue['html_url']
                    ) for issue in issues])
                )
                for _, issues in self.issues.items()
            ])
        )

class StdOutSender(Sender):
    def send(self):
        for _, issues in self.issues.items():
            repo_txt = colored(
                '* {} ({})'.format(
                    issues[0]['repository']['name'],
                    issues[0]['repository']['html_url']
                ),
                'red',
                attrs=['bold']
            )
            print(repo_txt)
            for issue in issues:
                issue_name = colored(
                    '{}'.format(issue['title']),
                    'yellow'
                )
                print('{} ({})'.format(issue_name, issue['html_url']))
            print()

class Reminder:
    def __init__(self, settings_path, *senders_clss):
        self.settings = yaml.load(open(settings_path))
        self.senders_clss = senders_clss
        self.fetcher = GitHubIssuesFetcher(self.settings)

    def run(self):
        issues = self.fetcher.fetch()
        for cls in self.senders_clss:
            s = cls(self.settings, issues)
            s.send()



if __name__ == '__main__':
    r = Reminder('settings.yaml', SlackSender, StdOutSender)
    r.run()
