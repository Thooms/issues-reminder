from collections import defaultdict
from requests.auth import HTTPBasicAuth
from termcolor import colored
import requests
import yaml

class IssuesFetcher:
    def __init__(self, settings_path):
        self.settings = yaml.load(open(settings_path))
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
    def __init__(self, issues):
        self.issues = issues

    def send(self):
        raise Exception('Please implement this method.')

class MailSender(Sender):
    def send(self):
        pass

class SlackSender(Sender):
    def send(self):
        pass

class StdOutSender(Sender):
    def send(self):
        for repo_url, issues in self.issues.items():
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
        self.settings_path = settings_path
        self.senders_clss = senders_clss
        self.fetcher = IssuesFetcher(self.settings_path)

    def run(self):
        issues = self.fetcher.fetch()
        for cls in self.senders_clss:
            s = cls(issues)
            s.send()



if __name__ == '__main__':
    r = Reminder('settings.yaml', MailSender, SlackSender, StdOutSender)
    r.run()
