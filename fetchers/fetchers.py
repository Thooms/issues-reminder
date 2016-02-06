from collections import defaultdict
from requests.auth import HTTPBasicAuth
import requests

class GitHubFetcher:
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
