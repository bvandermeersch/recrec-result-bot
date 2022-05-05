import json
import os
import pymysql
import http.client
import logging
import dbFunctions
import helpers
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def recrecbot(event, context):

    api_key = os.environ['apiKey']
    rds_host  = os.environ['rdsHost']
    name = os.environ['rdsUsername']
    password = os.environ['rdsPassword']
    db_port = os.environ['rdsPort']
    db_name = os.environ['rdsDBName']

    # db connection
    try:
        mysql_conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        print(mysql_conn)

    except pymysql.MySQLError as e:
        
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        sys.exit()

    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    # get all active seasons      
    seasons = dbFunctions.get_seasons(mysql_conn)

    # loop the seasons
    for s in seasons:

        # set season id
        season_id = s[1]

        # set up the GET request to get season information
        http_conn = http.client.HTTPSConnection("app.recrec.io")
        payload = ''
        headers = {
          'X-Api-Key': api_key
        }
        # send it
        http_conn.request("GET", "/api/matches?season_id=" + season_id, payload, headers)
        
        # get and parse response
        res = http_conn.getresponse()
        data = res.read() 
        data = json.loads(data)
        
        # loop the results
        for d in data:

            # check if a match_id exists in DB
            match_exists = dbFunctions.check_for_match(mysql_conn,season_id,d['id'])

            # no match_id in DB
            if match_exists == 0:
                
                # check if the match was actually played by checking scores
                if d['away_score'] == None and d['home_score'] == None:
                    # match not played continue to next record
                    continue
                else:
                    # build match result
                    player1 = d['home_competitor']['name']
                    player2 = d['away_competitor']['name']

                    group = d['division']['name']
                    group_id = d['division']['id']

                    player1_score = d['home_score']
                    player2_score = d['away_score']

                    # format result depending on who won
                    if player1_score > player2_score:
                        result = player1 + " defeated " + player2 + " " + str(player1_score) + "-" + str(player2_score)
                    else:
                        result = player2 + " defeated " + player1 + " " + str(player2_score) + "-" + str(player1_score)

                    # insert new row
                    dbFunctions.insert_match(mysql_conn,season_id, d['id'])

                    if s[3]:
                        discord_url = s[3]
                        helpers.discord(discord_url,group,result,group_id)

                    if s[4]:
                        slack_url = s[4]
                        helpers.slack(slack_url,group,result,group_id)