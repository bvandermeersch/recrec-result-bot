from discord_webhook import DiscordWebhook, DiscordEmbed
import urllib.request
import urllib.parse
import json
import os

def discord(webHookURL,group,result,division_id):

    # do the discord stuff
    webhook = DiscordWebhook(url=webHookURL, rate_limit_retry=True)
    embed = DiscordEmbed(title='', description="", color='581478')
    embed.add_embed_field(name="Group", value=group, inline=False)
    embed.add_embed_field(name="Result", value=result, inline=False)
    embed.add_embed_field(name="Standings", value="["+str(group)+"](https://app.recrec.io/divisions/"+ division_id +"/standings)")
    # add all the embeds to the webook
    webhook.add_embed(embed)

    # send it!
    response = webhook.execute()


def slack(webHookURL,group,result,division_id):
    
    # build data for request
    data = json.dumps({'text': result}).encode('utf-8') #data should be in bytes
    headers = {'Content-Type': 'application/json'}

    # send it!
    req = urllib.request.Request(webHookURL, data, headers)
    resp = urllib.request.urlopen(req)
    response = resp.read()