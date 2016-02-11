from jinja2 import Template
from slacker import Slacker
from termcolor import colored
import sys

class Sender:
    def send(self, providers):
        raise Exception('Please implement this method.')

class MailSender(Sender):
    def send(self):
        pass

class SlackSender(Sender):
    def __init__(self, slack_api_token, chans):
        self.chans = chans
        self.template = Template(open('senders/slack.tpl').read())
        self.slack = Slacker(slack_api_token)

    def send(self, providers):
        for chan in self.chans:
            self.slack.chat.post_message(chan, self.slack_message(providers))

    def slack_message(self, providers):
        return self.template.render(data=providers)

class FileSender(Sender):
    def __init__(self, fobj=sys.stdout):
        self.fobj = fobj

    def send(self, providers):
        for provider in providers:
            print(colored(
                'From {}'.format(provider.name),
                'blue',
                attrs=['bold']
            ), file=self.fobj)

            for repo in provider.repos:
                repo_txt = colored(
                    '* {} ({})'.format(repo.name, repo.url),
                    'red'
                )
                print(repo_txt, file=self.fobj)

                for iss in repo.issues:
                    issue_name = colored(
                        '{}'.format(iss.title),
                        'yellow'
                    )
                    print('{} ({})'.format(issue_name, iss.url), file=self.fobj)
                print('', file=self.fobj)
