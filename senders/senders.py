from email.mime.text import MIMEText
from jinja2 import Template
from slacker import Slacker
from termcolor import colored
import smtplib
import sys

class Sender:
    def send(self, providers):
        raise Exception('Please implement this method.')

class MailSender(Sender):
    def __init__ (self, ev, unit, smtp_server, sender_address, recipient_address):
        if unit not in ['seconds', 'minutes', 'hours', 'days']:
            raise Exception('Bad scheduling information provided')
        self.template = Template(open('senders/mail.tpl').read())
        self.smtp = smtp_server
        self.msg_from = sender_address
        self.msg_to = recipient_address
        self.schedule_unit = unit
        self.schedule_ev = ev

    def send(self, providers):
        msg = MIMEText(self.template.render(data=providers))
        msg['Subject'] = 'Issues reminder'
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        s = smtplib.SMTP(self.smtp)
        s.send_message(msg)
        s.quit()

class SlackSender(Sender):
    def __init__(self, ev, unit, slack_api_token, chans):
        if unit not in ['seconds', 'minutes', 'hours', 'days']:
            raise Exception('Bad scheduling information provided')
        self.chans = chans
        self.template = Template(open('senders/slack.tpl').read())
        self.slack = Slacker(slack_api_token)
        self.schedule_unit = unit
        self.schedule_ev = ev

    def send(self, providers):
        for chan in self.chans:
            self.slack.chat.post_message(chan, self.slack_message(providers))

    def slack_message(self, providers):
        return self.template.render(data=providers)

class FileSender(Sender):
    def __init__(self, ev, unit, fobj=sys.stdout):
        if unit not in ['seconds', 'minutes', 'hours', 'days']:
            raise Exception('Bad scheduling information provided')
        self.fobj = fobj
        self.schedule_unit = unit
        self.schedule_ev = ev

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
