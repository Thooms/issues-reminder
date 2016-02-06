from jinja2 import Template
from slacker import Slacker
from termcolor import colored

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
        template = Template(open('senders/slack.tpl').read())
        return template.render(data=self.issues.items())

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
