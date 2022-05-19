from cgitb import text
import os
from re import S
from numpy import block
import slack


class SlackBot:
    client = None

    def __init__(self):
        slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.client = slack.WebClient(token=slack_bot_token)
       
    def success_send(self, message):
        slack_channel = os.getenv('SLACK_CHANNEL')
        self.client.chat_postMessage(channel=slack_channel, text=message)

    def send(self):
        slack_channel = os.getenv('SLACK_CHANNEL')
        branch = os.getenv('GITHUB_BRANCH')
        commit = os.getenv('GITHUB_COMMIT')
        status = os.getenv('JOB_STATUS')
        pr_url = os.getenv('PR_URL')

        if status == "failure" or status == "cancelled":
            msg = 'Branch [{}] at commit [{}] with status [{}]'.format(branch, commit, status)
        else:
            committer = branch.split("/")[0]
            msg = 'Please review pull request from {} at {}'.format(committer, pr_url)    
        self.client.chat_postMessage(channel=slack_channel, text = '<!channel> ' + msg )        

if __name__ == "__main__":
    slack_bot = SlackBot()
    slack_bot.send()