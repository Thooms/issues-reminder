from jinja2 import Template
from slacker import Slacker
from termcolor import colored

class Sender:
    def __init__(self, settings):
        self.settings = settings

    def send(self, issues):
        raise Exception('Please implement this method.')

class MailSender(Sender):
    def send(self):
        pass

class SlackSender(Sender):
    def __init__(self, settings):
        super().__init__(settings)
        self.template = Template(open('senders/slack.tpl').read())
        self.slack = Slacker(self.settings['slack']['api-token'])

    def send(self, issues):
        self.slack.chat.post_message('#bot-test', self.slack_message(issues))

    def slack_message(self, issues):
        return self.template.render(data=issues.items())

class StdOutSender(Sender):
    def send(self, issues):
        for _, issues in issues.items():
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
