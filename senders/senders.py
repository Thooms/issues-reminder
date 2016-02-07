from jinja2 import Template
from slacker import Slacker
from termcolor import colored

class Sender:
    def __init__(self, settings):
        self.settings = settings

    def send(self, providers):
        raise Exception('Please implement this method.')

class MailSender(Sender):
    def send(self):
        pass

class SlackSender(Sender):
    def __init__(self, settings):
        super().__init__(settings)
        self.template = Template(open('senders/slack.tpl').read())
        self.slack = Slacker(self.settings['slack']['api-token'])

    def send(self, providers):
        self.slack.chat.post_message('#bot-test', self.slack_message(providers))

    def slack_message(self, providers):
        return self.template.render(data=providers)

class StdOutSender(Sender):
    def send(self, providers):
        for provider in providers:
            print(colored(
                'From {}'.format(provider.name),
                'blue',
                attrs=['bold']
            ))

            for repo in provider.repos:
                repo_txt = colored(
                    '* {} ({})'.format(repo.name, repo.url),
                    'red'
                )
                print(repo_txt)

                for iss in repo.issues:
                    issue_name = colored(
                        '{}'.format(iss.title),
                        'yellow'
                    )
                    print('{} ({})'.format(issue_name, iss.url))
                print()
