import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

#installed slackclient/dotenv
#install flask/slackeventsapi

env_path = Path('.') / '.env'
load_dotenv(env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call('auth.test')['user_id']

#subscribes to events (messages in this example)
#depending on bots permissions we can have it read messages from all channels
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    print(event)
    #sends message to a specific channel
    #this will run infinitely unless we specify a stopping condition
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)



#can specify port here too
if __name__ == "__main__":
    app.run(debug=True)


