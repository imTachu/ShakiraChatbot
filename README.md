![The unofficial Shakira Chatbot](graphics/banner.jpg)

# The Unofficial Shakira Chatbot

[![Build Status][travisci-badge]][travisci-builds] 
[![Requirements Status][requiresio-badge]][requiresio-url]

## Usage

You can ask about social media, concerts (of El Dorado tour), her discography and more coming.

## Development considerations

* Datasources for this chatbot can be found in the [resources](resources) folder in this repository. I didn't create a database because didn't think it was _that_ interesting for this challenge.
* Custom slot types _concerts and albums_ values are generated from the datasource itself. See [lex slot builder](chatbot/lex_slot_builder.py)  
* There's a [deployment script](deploy.sh) that I use to rapidly deploy my AWS Lambda function without touching anything in AWS Lex.

## Architecture 

AWS Lex powers up this chatbot through 10 intents:

| Intent name                                           | Functionality                                                                                                                                                                                       | What's interesting?                                                                                                                                                                                                  |
|-------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Sing`                                                | Creates an audio file from `AWS Polly` on the fly, stores it in a S3 bucket. Uses `ElicitSlot` and `SessionAttributes`, reproduces the audio file in Facebook Messenger.                            | As of today, in the official Lex docs 'voice' and 'audio' are mentioned, but there aren't any examples. I wanted to include it here just to experiment the whole generate/store/reproduce flow.                      |
| `DealWithIt`                                          | This intent is created for the solely purpose of handling hate/love feelings towards the chatbot. I didn't want to create two intents for hate and love, so this one uses a sentiment analysis API. | Until developing this project, sentiment analysis felt to me like something very demanding and time-consuming to include in a project. Although, here I do it very simplistic, it wasn't such a hassle to implement. |
| `AboutAlbum`, `AboutSong`, `RandomGif`, `WhenConcert` | Reply based on context (slots), uses slot validations, `ElicitSlot`, `Close`.                                                                                                                       | Custom slot types values generated from the datasource itself.                                                                                                                                                       |
| `Greeting`, `Helper`, `SocialMedia`, `Thanks`         | These intents provide plain simple answers, necessary to fulfill some basic "human" interactions.                                                                                                   | IMHO, chatbots should be capable of replying to simple nice human things like "Thanks".                                                                                                                              |

## Setup steps

1. Configure your AWS access key and secret key [properly][credentials]. DO NOT publish your access key and secret key to public sites such as GitHub!
2. Configure your AWS account id in an environment variable `AWS_ACCOUNT_ID`
3. Configure a `MASHAPE_API_KEY` environment variable (Necessary for the `DealWithIt` intent, this is the sentiment analysis API), you can get one [here][mashable-twinword-api-key] 
4. Create [a virtual env][virtualenv] for the bot. 
5. Run: `source bin/activate`
6. Run: `pip install -r requirements.txt`
7. Run: `python setup.py`
8. Go to AWS Lex console, and deploy the bot in a Facebook Messenger channel following [these instructions][facebook-deploy].
9. Enjoy!

## How to use the bot

This bot is available in Facebook Messenger. Unfortunately it is not yet ready for public access but authorized users can chat with it [here][chatbot]

## Notes and known issues

* This bot was created from a sample bot version given for the [GOTO Amazon Chatbot Challenge.][hackathon-main]
* Normalization was not taken into account. If you look for a concert in New York, the chatbot won't find it if you type for example, NYC. 
* AWS Lex is a 'new' service, this chatbot brought a lot of insights, I have made a [blog post][blog-post] about it if you want to take a look :) 

[blog-post]: lalala
[chatbot]: https://www.messenger.com/t/484930695187800
[credentials]: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
[facebook-deploy]: http://docs.aws.amazon.com/lex/latest/dg/fb-bot-association.html
[hackathon-main]: http://www.amazondcn.com/challenge/index.html
[mashable-twinword-api-key]: https://market.mashape.com/twinword/sentiment-analysis-free
[requiresio-badge]: https://requires.io/github/imTachu/ShakiraChatbot/requirements.svg?branch=master
[requiresio-url]: https://requires.io/github/imTachu/ShakiraChatbot/requirements/?branch=master
[travisci-badge]: https://travis-ci.org/imTachu/ShakiraChatbot.svg?branch=master
[travisci-builds]: https://travis-ci.org/imTachu/ShakiraChatbot's
[virtualenv]: http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/

