import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
from PIL import Image
from wordcloud import STOPWORDS, ImageColorGenerator, WordCloud
from slackclient import SlackClient

stopWords = config.stopWords

class wordCloudPlugin:

    def __init__(self):
        self.keywords = ["!cloud", "!wordcloud"]
        self.client = SlackClient(config.admin_token)

    def execute(self, event):

        channel = event.get('channel')
        rawMessages = self.client.api_call("channels.history", channel=channel)
        
        if not rawMessages["ok"]:
            self.client.api_call("chat.postMessage", thread_ts=event['ts'], channel=channel, text="Error forming the word cloud :(")
            return

        text = ""
        for messageObj in rawMessages["messages"]:
            text += " " + messageObj["text"].strip()

        while rawMessages["has_more"]:
            rawMessages = self.client.api_call("channels.history", channel=channel, 
                            count=1000, latest=rawMessages["messages"][-1]["ts"])
            for messageObj in rawMessages["messages"]:
                text += " " + messageObj["text"].strip()

        text = text.lower()
        text = " ".join([word for word in text.split() if word not in stopWords])
        text = re.sub(r"\s+", ' ', text)
        text = re.sub('<[^>]+>', '', text)
        text = re.sub(r"[^a-z .]", '', text) #remove all characters that aren't letters, spaces, or periods
        
        if text:

            wordcloud = WordCloud(width=1600, height=800).generate(text)
            filepath = 'plugins/wordClouds/word_cloud_' + channel + '.png'

            plt.figure( figsize=(20,10), facecolor='k')
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(filepath, facecolor='k', bbox_inches='tight')

            # wordcloud.to_file(filepath)
            file = open(filepath, 'rb')
            self.client.api_call("files.upload", channels=channel,
                                file=file,
                                initial_comment="WordCloud Generated!")       