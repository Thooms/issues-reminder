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

class GitLabByRepoFetcher:
    def __init__(self, gitlab_url='', gitlab_token='', repos=[]):
        self.gitlab_url = gitlab_url
        self.gitlab_token = gitlab_token
        self.repos_names = repos

    def call_gitlab_api(self, endpoint):
        return requests.get(
            '{}/api/v3/{}'.format(self.gitlab_url, endpoint),
            headers={'PRIVATE-TOKEN': self.gitlab_token}
        )

    def fetch_repos_metadata(self):
        self.repos_metadata = []
        for name in self.repos_names:
            req = self.call_gitlab_api('projects/{}'.format(name.replace('/', '%2F')))
            if req.status_code == 200:
                self.repos_metadata.append(req.json())

    def fetch(self):
        self.fetch_repos_metadata()

        provider = issues.Provider('Gitlab')
        for repo in self.repos_metadata:
            req = self.call_gitlab_api('projects/{}/issues'.format(repo['id']))
            if req.status_code == 200:
                rep = issues.Repository(repo['name_with_namespace'], repo['web_url'])
                for issue in req.json():
                    if issue['state'] == 'opened':
                        rep.add_issue(issues.Issue(
                            issue['title'],
                            '{}/issues/{}'.format(repo['web_url'], issue['iid']),
                            issue['author']['username']
                        ))
                provider.add_repository(rep)
        return provider
