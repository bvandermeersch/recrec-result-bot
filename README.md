AWS Serverless RecRec Match Bot

Will create a match bot that reports match results to discord or slack every 15mins

Developed using node 14.7.6 and Python3.8

```
nvm use 14.17.6
npm install -g serverless

sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-stage-manager
```

Environtments supported development, staging, production

Create an env file for each environment in the following format using the included example file:

.env.development.yml

.env.staging.yml

.env.production.yml

Fill in all the appropriate variables

Deploy to aws:

```serverless deploy --stage production```

This will launch a lambda function to AWS with the production .env file


requires a DB with a matches and seasons table
