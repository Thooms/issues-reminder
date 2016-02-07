
class Issue:
    def __init__(self, title, url, author):
        self.title = title
        self.url = url
        self.author = author

class Repository:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.issues = []

    def add_issue(self, issue):
        self.issues.append(issue)

class Provider:
    """
    Stores a set of issues that come from repos from a unique provider
    (like GitHub or GitLab)
    """

    def __init__(self, name):
        self.name = name
        self.repos = []

    def add_repository(self, repository):
        self.repos.append(repository)
