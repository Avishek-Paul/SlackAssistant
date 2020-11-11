
import importlib
import glob
import config
import logging
import logging.config
from celery import Celery

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging_config.ini')

app = Celery('slack_assistant', broker=config.broker)

# def loadPlugins(sef):
files = [f.replace('/','.')[:-3] for f in glob.glob("plugins/*.py") if '__' not in f] #grabs all plugin names from plugins folder
plugins = []
for file_ in files:
    plugin_module = importlib.import_module(file_)
    raw_plugin = getattr(plugin_module, file_.split('.')[1])
    plugin_instance = raw_plugin()
    plugins.append(plugin_instance)

@app.task
def eventHandler(event):
    eventType = event.get('type', "")
    kw = None

    if eventType == "message":
        if event.get('text', "").startswith('!'): #for traditional plugins
            message = event.get('text')
            kw = [message.split()[0]]
        if event.get("channel") in config.channel_monitor.keys(): #for monitoring channels
            kw = ['!chatMonitor']

    elif eventType == "reaction_added" or eventType=="reaction_removed": #for reaction-based plugins
        kw = [event.get('reaction', None), 'reactionBased']

    elif eventType == "user_typing":
        kw = ["!trollbot"]
        
    if not kw:
        return

    for plugin in plugins:
        if any(x in plugin.keywords for x in kw):
            logger.debug("Keywords matched: %s", plugin.keywords)            
            plugin.execute(event)
