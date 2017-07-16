import boto3
import json
import os
import time
from chatbot.lex_slot_builder import build_songs_slot, build_albums_slot, build_concert_locations_slot
from zipfile import ZipFile

from botocore.exceptions import ClientError

ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
FUNCTION_NAME = 'Shakira-Botcontrol'

with ZipFile('lambda-package.zip', 'w') as myzip:
    myzip.write('chatbot/__init__.py')
    myzip.write('chatbot/botcontrol.py')
    myzip.write('chatbot/dict_operations.py')
    myzip.write('chatbot/lex_handler.py')
    myzip.write('chatbot/lex_slot_builder.py')
    myzip.write('resources/__init__.py')
    myzip.write('resources/concerts.py')
    myzip.write('resources/albums.py')
    myzip.write('resources/helper_responses.py')

''' Initial Bot configuration '''

botcontrol_function = {
    u'Code': {u'ZipFile': open('lambda-package.zip').read()},
    u'Description': u'Function controling the ShakiraChatbot, powered up by Lex',
    u'Environment': {u'Variables': {u'MASHAPE_API_KEY': os.environ['MASHAPE_API_KEY']}},
    u'FunctionName': u'{}'.format(FUNCTION_NAME),
    u'Handler': u'chatbot/botcontrol.lambda_handler',
    u'MemorySize': 128,
    u'Role': u'arn:aws:iam::{}:role/shakirachatbot-role'.format(ACCOUNT_ID),
    u'Runtime': u'python2.7',
    u'Timeout': 10,
    u'TracingConfig': {u'Mode': u'PassThrough'},
    u'Publish': True,
}

permission = {
    u'FunctionName': u'{}'.format(FUNCTION_NAME),
    u'StatementId': u'AuthorizeLex',
    u'Action': u'lambda:InvokeFunction',
    u'Principal': u'lex.amazonaws.com',
    u'SourceArn': u'arn:aws:lex:us-east-1:{}:intent:*:*'.format(ACCOUNT_ID),
}

role_policy_document = {
        'Version': '2012-10-17',
        'Statement': [
            {'Effect': 'Allow', 'Principal': {'Service': ['lambda.amazonaws.com']},
             'Action': ['sts:AssumeRole']},
        ]
    }

inline_policy = {
    'Version': '2012-10-17',
    'Statement': [
        {
            'Effect': 'Allow',
            'Action': [
                'polly:SynthesizeSpeech',
                's3:ListBucket',
                's3:PutObject',
                'logs:CreateLogGroup',
                'logs:CreateLogStream',
                'logs:PutLogEvents'
            ],
            'Resource': '*'
        }
    ]
}

''' Intents '''

about_album_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)},
                             u'type': u'CodeHook'},
    u'name': u'AboutAlbum',
    u'sampleUtterances': [u'Tell me about {album} album', u'What songs are in {album}', u'Songs of {album}',
                          u'About that album', u'About an album', u'About any album'],
    u'slots': [{u'name': u'album',
                u'priority': 1,
                u'sampleUtterances': [],
                u'slotConstraint': u'Required',
                u'slotType': u'Albums',
                u'slotTypeVersion': u'$LATEST',
                u'valueElicitationPrompt': {u'maxAttempts': 2,
                                            u'messages': [{u'content': u'What album?', u'contentType': u'PlainText'}]}}],
}

about_song_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)},
                             u'type': u'CodeHook'},
    u'name': u'AboutSong',
    u'sampleUtterances': [u'Tell me about {song} song', u'I wanna know about {song} song',
                          u'I want to know about {song} song', u'What\'s the album of {song}', u'Album of {song}',
                          u'About that song', u'About a song', u'About any song'],
    u'slots': [{u'name': u'song',
                u'priority': 1,
                u'sampleUtterances': [],
                u'slotConstraint': u'Required',
                u'slotType': u'Songs',
                u'slotTypeVersion': u'$LATEST',
                u'valueElicitationPrompt': {u'maxAttempts': 2,
                                            u'messages': [{u'content': u'What song?', u'contentType': u'PlainText'}]}}],
}

deal_with_it_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)}, u'type': u'CodeHook'},
    u'name': u'DealWithIt',
    u'sampleUtterances': [u'You are amazing', u'u r amazing', u'you suck', u'u suck', u'this is retarded', u'I hate you', u'I love you', u'this is the best chatbot', u'this is the worst chatbot']
}


greeting_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)}, u'type': u'CodeHook'},
    u'name': u'Greeting',
    u'sampleUtterances': [u'hello', u'hi', u'yo', u'what\'s up']
}

helper_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)}, u'type': u'CodeHook'},
    u'name': u'Helper',
    u'sampleUtterances': [u'What should I do', u'Help', u'Examples', u'Commands', u'How do I start', u'What can you do', u'I don\'t know what to do']
}

random_gif = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)}, u'type': u'CodeHook'},
    u'name': u'RandomGif',
    u'sampleUtterances': [u'Photos', u'Random gif', u'Give me a gif', u'gif']
}

sing_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)},
                             u'type': u'CodeHook'},
    u'name': u'Sing',
    u'sampleUtterances': [u'Sing that song'],
    u'slots': [{u'name': u'song',
                u'priority': 1,
                u'sampleUtterances': [],
                u'slotConstraint': u'Required',
                u'slotType': u'Songs',
                u'slotTypeVersion': u'$LATEST',
                u'valueElicitationPrompt': {u'maxAttempts': 2,
                                            u'messages': [{u'content': u'What song?', u'contentType': u'PlainText'}]}}],
}


social_media = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)}, u'type': u'CodeHook'},
    u'name': u'SocialMedia',
    u'sampleUtterances': [u'What\'s her contact', u'Social media', u'Twitter', u'I want her social media']
}

thanks_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(
                                               ACCOUNT_ID, FUNCTION_NAME)}, u'type': u'CodeHook'},
    u'name': u'Thanks',
    u'sampleUtterances': [u'thanks', u'thank you', u'ty']
}

when_concert_intent = {
    u'dialogCodeHook': {u'messageVersion': u'1.0',
                        u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
    u'fulfillmentActivity': {u'codeHook': {u'messageVersion': u'1.0',
                                           u'uri': u'arn:aws:lambda:us-east-1:{}:function:{}'.format(ACCOUNT_ID, FUNCTION_NAME)},
                             u'type': u'CodeHook'},
    u'name': u'WhenConcert',
    u'sampleUtterances': [u'Is she coming', u'When is the concert',  u'What are the concerts', u'Is there a concert', u'When is her concert',
                          u'When is the concert at {location}', u'When is the concert in {location}'],
    u'slots': [{u'name': u'location',
                u'priority': 1,
                u'sampleUtterances': [],
                u'slotConstraint': u'Required',
                u'slotType': u'ConcertLocations',
                u'slotTypeVersion': u'$LATEST',
                u'valueElicitationPrompt': {u'maxAttempts': 2,
                                            u'messages': [{u'content': u'In what city?', u'contentType': u'PlainText'},
                                                          {u'content': u'Ok, in which city?', u'contentType': u'PlainText'}
                                                          ]}}],
}

''' Custom slot types '''

albums_slot_type = {
    u'description': u'All Shakira albums',
    u'enumerationValues': build_albums_slot(),
    u'name': u'Albums',
}

concert_locations_slot_type = {
    u'description': u'Concert locations for El Dorado Tour (Area, Country, City)',
    u'enumerationValues': build_concert_locations_slot(),
    u'name': u'ConcertLocations',
}

songs_slot_type = {
    u'description': u'All Shakira songs',
    u'enumerationValues': build_songs_slot(),
    u'name': u'Songs',
}

bot = {
    u'abortStatement': {u'messages': [{u'content': u'Sorry, I could not understand. Goodbye.',
                                       u'contentType': u'PlainText'}]},
    u'childDirected': False,
    u'clarificationPrompt': {u'maxAttempts': 5,
                             u'messages': [{u'content': u'Sorry, can you please repeat that?',
                                            u'contentType': u'PlainText'},
                                           {u'content': u'I didn\'n get that :( can you please try something else?',
                                            u'contentType': u'PlainText'}, {u'content': u'I beg you pardon?',
                                                                            u'contentType': u'PlainText'}]},
    u'intents': [{u'intentName': u'AboutAlbum', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'AboutSong', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'DealWithIt', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'Greeting', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'Helper', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'RandomGif', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'Sing', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'SocialMedia', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'Thanks', u'intentVersion': u'$LATEST'},
                 {u'intentName': u'WhenConcert', u'intentVersion': u'$LATEST'}],
    u'locale': u'en-US',
    u'name': u'ShakiraChatbot',
    u'processBehavior': 'BUILD',
    u'voiceId': u'0'}

bot_alias = {
    u'name': u'ShakiraChatbot',
    u'botVersion': u'$LATEST',
    u'botName': u'ShakiraChatbot',
}

# Setup code

#os.system('chalice deploy')

lex = boto3.client('lex-models', region_name='us-east-1')
lambd = boto3.client('lambda', region_name='us-east-1')
iam = boto3.client('iam', region_name='us-east-1')


def wait(secs):
    time.sleep(secs)


# delete everything

try:
    iam.delete_role_policy(RoleName='shakirachatbot-role',
        PolicyName='BotAccess'
    )
    print 'Deleted inline policy for role shakirachatbot-role'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NoSuchEntity':
        raise

try:
    iam.delete_role(RoleName='shakirachatbot-role')
    print 'Deleted custom role shakirachatbot-role'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NoSuchEntity':
        raise

try:
    lambd.delete_function(FunctionName=FUNCTION_NAME)
    print 'Deleted {} lambda function'.format(FUNCTION_NAME)
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'ResourceNotFoundException':
        raise

try:
    lex.delete_bot_alias(name='ShakiraChatbot', botName='ShakiraChatbot')
    print 'Deleted alias ShakiraChatbot'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_bot(name='ShakiraChatbot')
    print 'Deleted ShakiraChatbot'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='AboutAlbum')
    print 'Deleted intent AboutAlbum'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='AboutSong')
    print 'Deleted intent AboutSong'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='DealWithIt')
    print 'Deleted intent DealWithIt'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='Greeting')
    print 'Deleted intent Greeting'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='Helper')
    print 'Deleted intent Helper'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='RandomGif')
    print 'Deleted intent RandomGif'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='Sing')
    print 'Deleted intent Sing'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='SocialMedia')
    print 'Deleted intent SocialMedia'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='Thanks')
    print 'Deleted intent Thanks'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_intent(name='WhenConcert')
    print 'Deleted intent WhenConcert'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_slot_type(name='Albums')
    print 'Deleted slot type Albums'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_slot_type(name='ConcertLocations')
    print 'Deleted slot type ConcertLocations'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise

try:
    lex.delete_slot_type(name='Songs')
    print 'Deleted slot type Songs'
    wait(3)
except ClientError, e:
    if e.response['Error']['Code'] != 'NotFoundException':
        raise


role = iam.create_role(RoleName='shakirachatbot-role', AssumeRolePolicyDocument=json.dumps(role_policy_document))['Role']
print 'Created custom role shakirachatbot-role'
wait(3)

iam.put_role_policy(RoleName='shakirachatbot-role', PolicyName='BotAccess', PolicyDocument=json.dumps(inline_policy))
print 'Created inline policy for role shakirachatbot-role'
wait(10)

lambd.create_function(**botcontrol_function)
print 'Created lambda function {}'.format(FUNCTION_NAME)
wait(3)

lambd.add_permission(**permission)
wait(3)
print 'Assigned permissions authorizing Lex to call {}'.format(FUNCTION_NAME)

lex.put_slot_type(**albums_slot_type)
print 'Created slot type Albums'
wait(3)

lex.put_slot_type(**concert_locations_slot_type)
print 'Created slot type ConcertLocations'
wait(3)

lex.put_slot_type(**songs_slot_type)
print 'Created slot type Songs'
wait(7)

lex.put_intent(**about_album_intent)
wait(3)
print 'Created AboutAlbum intent'

lex.put_intent(**about_song_intent)
wait(3)
print 'Created AboutSong intent'

lex.put_intent(**deal_with_it_intent)
wait(3)
print 'Created DealWithIt intent'

lex.put_intent(**greeting_intent)
wait(3)
print 'Created Greeting intent'

lex.put_intent(**helper_intent)
wait(3)
print 'Created Helper intent'

lex.put_intent(**random_gif)
wait(3)
print 'Created RandomGif intent'

lex.put_intent(**sing_intent)
wait(3)
print 'Created Sing intent'

lex.put_intent(**social_media)
wait(3)
print 'Created SocialMedia intent'

lex.put_intent(**thanks_intent)
wait(3)
print 'Created Thanks intent'

lex.put_intent(**when_concert_intent)
wait(3)
print 'Created WhenConcert intent'

lex.put_bot(**bot)
wait(3)
print 'Created bot'

lex.put_bot_alias(**bot_alias)
print 'Created bot alias'
wait(5)

os.unlink('lambda-package.zip')

print 'All done, exiting...'
