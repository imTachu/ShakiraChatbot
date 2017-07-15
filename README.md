# The _unofficial_ Shakira Chatbot

[![Build Status][travisci-badge]][travisci-builds] 

## Usage

You can ask about social media, concerts (of El Dorado tour), her discography and more coming.

## Development considerations

* Datasources for this chatbot can be found in the [resources](resources) folder in this repository. I didn't create a database because didn't think it was _that_ interesting for this challenge.
* Custom slot types _concerts and albums_ values are generated from the datasource itself. See [lex_helper](lex_slot_builder.py)  
* Besides setting up AWS credentials, this project relies on the AWS account ID (to do the actual Lex deployment), this is set via the environment variable `AWS_ACCOUNT_ID` _see_ [setup.py](setup.py)
* I included another [deployment script](deploy.sh) because I needed to rapidly deploy my AWS Lambda function without touching anything in AWS Lex.

## Architecture 

The bot has xx intents [TODO] 

## Setup steps

1. Configure your AWS access key and secret key [properly][credentials]. DO NOT publish your access key and secret key to public sites such as github!
2. Preferably, create [a virtual env][virtualenv] for the bot. 
3. Configure your AWS account id in an environment variable `AWS_ACCOUNT_ID`
4. Run: `source bin/activate`
5. Run: `pip install -r requirements.txt`
6. Run: `python setup.py`
7. Go to AWS Lex console, [deploy the bot][facebook-deploy] in a Facebook Messenger channel.

## How to use the bot

This bot is available in Facebook Messenger. 

## Notes

* This bot was created from a sample bot version given for the [GOTO Amazon Chatbot Challenge.][hackathon-main]
* This can be extendend A LOT (not-only studio albums), chart positions, etc

[credentials]: https://github.com/awslabs/chalice#credentials
[facebook-deploy]: http://docs.aws.amazon.com/lex/latest/dg/fb-bot-association.html
[hackathon-main]: http://www.amazondcn.com/challenge/index.html
[travisci-badge]: https://travis-ci.org/imTachu/ShakiraChatbot.svg?branch=master
[travisci-builds]: https://travis-ci.com/imTachu/ShakiraChatbot
[virtualenv]: http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/

