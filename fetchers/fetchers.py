from collections import defaultdict
from requests.auth import HTTPBasicAuth
import requests

import issues

class GitHubByOrgsFetcher:
    def __init__(self, username='', token='', organizations=[]):
        self.organizations = organizations
        self.api_url = 'https://api.github.com/orgs/{}/issues'
        self.auth = HTTPBasicAuth(username, token)
        self.params = {'filter': 'all'}
        self.headers = {'Accept': 'application/vnd.github.v3+json'}

    def organize_issues(self, res):
        # Gather issues by repo
        d = defaultdict(list)
        for r in res:
            d[r['repository_url']].append(r)

        # Build a correct Provider object
        provider = issues.Provider('GitHub')
        for issue_list in d.values():
            if not issue_list:
                continue
            repo = issues.Repository(
                issue_list[0]['repository']['name'],
                issue_list[0]['repository']['html_url']
            )
            for issue in issue_list:
                repo.add_issue(
                    issues.Issue(issue['title'], issue['html_url'], issue['user']['login'])
                )
            provider.add_repository(repo)
        return provider


    def fetch(self):
        res = []
        for url in (self.api_url.format(org) for org in self.organizations):
            req = requests.get(url, auth=self.auth, params=self.params, headers=self.headers)
            res.extend(req.json())

        return self.organize_issues(res)
