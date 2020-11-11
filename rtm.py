import datetime 
import config
from slackclient import SlackClient
from tasker import *
import logging
import logging.config

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

class SlackAssistant:
    client = SlackClient(config.bot_token)

    def __init__(self):
        self.sentPing = False

    def run(self):
        if self.client.rtm_connect():

            while self.client.server.connected is True:
                
                try: #wrapped in try to prevent error on raspberry Pi

                    response = self.client.rtm_read()
                    currTime = datetime.datetime.now()

                    #Event-based stuff here
                    if response:
                        try: #wrapped in try to catch plugin errors
                            event = response[0]
                            logger.debug(str(event))
                            if event['type'] not in config.ignoredEvents and event.get("subtype") != 'bot_message':
                                eventHandler.delay(event) #puts the task into rabbitmq for celery to execute
                        except Exception as e:
                            logger.error("Error has occured while handling event: " + str(e))

                    #Ping
                    if (currTime.second % 30 == 0) and not self.sentPing:
                        logger.debug("30 seconds has elapsed, sending a ping!")
                        self.client.server.ping()
                        self.sentPing = True
                    elif (currTime.second % 30 != 0) and self.sentPing:
                        self.sentPing = False

                except Exception as e:
                    logger.error("Error has occured while reading rtm: " + str(e))
        else:
            logger.error("Connection Failed!")

if __name__=="__main__":
    slack_assistant = SlackAssistant()
    slack_assistant.run()
