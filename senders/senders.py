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
        # This is ugly a.f. but it works fine.
        return 'Hello there, here are the open issues and pull requests of the week! :gift:\n{}'.format(
            '\n'.join([
                '\n\n• `{}` ({})\n{}'.format(
                    issues[0]['repository']['name'],
                    issues[0]['repository']['html_url'],
                    '\n'.join(['_{}_ ({})'.format(
                        issue['title'],
                        issue['html_url']
                    ) for issue in issues])
                )
                for _, issues in self.issues.items()
            ])
        )

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
