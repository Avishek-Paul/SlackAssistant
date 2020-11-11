from slackclient import SlackClient
import config
import random
import re
import logging
import logging.config

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

class diceRollPlugin:

    def __init__(self):
        self.keywords = ["!roll", "!Roll"]
        self.client = SlackClient(config.bot_token)

    def execute(self, event):

        logger.info("Running diceRollPlugin")

        channel = event['channel']
        message = event['text']

        kw = message.split()[0]
        payload = "".join(message.split()[1:])

        if kw in self.keywords:
            try:
                numDice = int(payload.split('d')[0])

                if 'x' in payload:
                    maxNum = int(re.findall(r"d(.*?)x", payload)[0])
                    numRolls = int(payload.split('x')[1])
                else:
                    maxNum = int(payload.split('d')[1])
                    numRolls = 1

                for i in range(numRolls):
                    result = [random.randint(1, maxNum) for i in range(numDice)]
                    sum_ = sum(result)
                    response = "You rolled a {} \n".format(sum_) + "`{}`".format(str(result))
                    self.client.api_call("chat.postMessage", thread_ts=event['ts'], channel=channel, text=response)
                
            except Exception as e:
                response = "Please put in format !roll [XdYxZ]\nX=Number of Dice, Y=Max number on Dice, Z=Number of Rolls\n`{}`".format(e)
                self.client.api_call("chat.postMessage", thread_ts=event['ts'], channel=channel, text=response)
