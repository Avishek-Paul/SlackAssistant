import config
from slackclient import SlackClient

class reactionCounterPlugin:
    def __init__(self):
        self.keywords = ['!rankings', '!Rankings', '!ranking', '!Ranking', 'reactionBased']
        self.client = SlackClient(config.bot_token)
        self.db = config.mongoClient

    def execute(self, event):

        if event['type'] == 'message':
            
            message = event.get("text", "")

            if len(message.split()) > 1:

                num = int(message.split()[1])

                maxGiversRaw = self.db.find(sort=[('given', -1)])
                maxReceiversRaw = self.db.find(sort=[('received', -1)])

                mGBase = "The #{} reactor is <@{}> with {} reacts given.\n"
                mRBase = "The #{} reacted is <@{}> with {} reacts received.\n"

                m1 = ""
                m2 = ""

                for i in range(num):
                    
                    try:
                        gItem = maxGiversRaw[i]
                        rItem = maxReceiversRaw[i]

                        m1 += mGBase.format(i+1, gItem['user_id'], gItem['given'])
                        m2 += mRBase.format(i+1, rItem['user_id'], rItem['received'])
                    
                    except:
                        break

            else:

                maxGiverRaw = self.db.find_one(sort=[('given', -1)])
                maxReceiverRaw = self.db.find_one(sort=[('received', -1)])
            
                m1 = "The #1 reactor is <@{}> with {} reacts given.\n".format(maxGiverRaw['user_id'], maxGiverRaw['given'])
                m2 = "The #1 reacted is <@{}> with {} reacts received.\n".format(maxReceiverRaw['user_id'], maxReceiverRaw['received'])

            self.client.api_call("chat.postMessage", thread_ts=event['ts'], channel=event['channel'], text="```{}```".format(m1))
            self.client.api_call("chat.postMessage", thread_ts=event['ts'], channel=event['channel'], text="```{}```".format(m2))


        elif event['type'] == 'reaction_added': #or event['type'] == 'reaction_removed':
            self.updateCounter(event, 1)
        elif event['type'] == 'reaction_removed':
            self.updateCounter(event, -1)
        
    def updateCounter(self, event, val):
        reaction = event['reaction']
        channel = event['item']['channel']
        reactor = event['user'] #react giver
        reacted = event['item_user'] #react receiver
        
        if reactor == reacted:
            return

        reactorRaw = self.client.api_call("users.info", user=reactor)
        reactedRaw = self.client.api_call("users.info", user=reacted)

        reactorReal = reactorRaw['user']['real_name']
        reactorDisplay = reactorRaw['user']['profile']['display_name']

        reactedReal = reactedRaw['user']['real_name']
        reactedDisplay = reactedRaw['user']['profile']['display_name']
        

        #increment the reactor
        self.db.update_one({'user_id' : reactor}, 
                            {
                                '$set' : {'display' : reactorDisplay, 'real': reactorReal}, 
                                '$inc' : {'given' : val}
                            }, 
                            upsert=True)

        #increments the reacted
        self.db.update_one({'user_id' : reacted}, 
                            {
                                '$set' : {'display' : reactedDisplay, 'real': reactedReal}, 
                                '$inc' : {'received' : val}
                            }, 
                            upsert=True)