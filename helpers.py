from discord_webhook import DiscordWebhook, DiscordEmbed
import urllib.request
import urllib.parse
import json
import os

def discord(group,result,division_id):

    webHookURL =  os.environ['discordURL']

    # do the discord stuff
    webhook = DiscordWebhook(url=webHookURL)
    embed = DiscordEmbed(title='', description="", color='581478')
    embed.add_embed_field(name="Group", value=group, inline=False)
    embed.add_embed_field(name="Result", value=result, inline=False)
    embed.add_embed_field(name="Standings", value="["+str(group)+"](https://app.recrec.io/divisions/"+ division_id +"/standings)")
    # add all the embeds to the webook
    webhook.add_embed(embed)

    # send it!
    response = webhook.execute()


def slack(group,result,division_id):
    
    # build data for request
    url =  os.environ['slackURL']
    data = json.dumps({'text': result}).encode('utf-8') #data should be in bytes
    headers = {'Content-Type': 'application/json'}

    # send it!
    req = urllib.request.Request(url, data, headers)
    resp = urllib.request.urlopen(req)
    response = resp.read()