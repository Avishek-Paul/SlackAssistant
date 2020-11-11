from slackclient import SlackClient
import config
import random

class chatMonitorPlugin:

    def __init__(self):
        self.keywords = ["!chatMonitor"]
        self.client = SlackClient(config.admin_token)
        self.self.approved_users_map = config.channel_monitor

    def execute(self, event):
        
        user = event.get('user')
        channel = event.get('channel')
        ts = event.get('ts', 'event_ts')

        if user not in self.self.approved_users_map[channel]:
            self.client.api_call("chat.delete", channel=channel, ts=ts, as_user=True)