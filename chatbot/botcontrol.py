# coding=utf-8
from __future__ import print_function
from chatbot.dict_operations import fetch_concert_locations, fetch_albums, find_album_by_name, format_concerts
from chatbot.lex_handler import close, close_with_response_card, delegate, elicit_slot, get_slots
from resources.helper_responses import HELPER_RESPONSES
from contextlib import closing
import boto3
import logging
import random
from botocore.exceptions import BotoCoreError, ClientError


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3 = boto3.resource('s3', region_name='us-east-1')
polly = boto3.client('polly', 'us-east-1')
bucket = s3.Bucket('shakirachatbot')
secure_random = random.SystemRandom()

""" --- Intents --- """


def about_album(intent_request):
    logger.info(intent_request)

    slots = get_slots(intent_request)
    album_slot = slots['album']

    if album_slot is None:
        return elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           slots, 'album', 'Ok, of what album do you want me to enlighten you?')
    albums = [s for s in fetch_albums() if album_slot.lower() in s.lower()]

    if len(albums) == 0:
        response = secure_random.choice(HELPER_RESPONSES)
    else:
        album_name = albums[0]
        album = find_album_by_name(album_name)
        response = album_name + ' was released on ' + album['release_date'].strftime('%A %d of %B of %Y') + '. It\'s songs are: \n* ' + '\n* '.join(album['songs'])
    print(response)
    return close(intent_request['sessionAttributes'], 'Fulfilled', response)


def about_song(intent_request):
    logger.info(intent_request)

    slots = get_slots(intent_request)
    song_slot = slots['song']
    # create_audio_file()
    close_with_response_card(intent_request['sessionAttributes'], 'Fulfilled', None, None, None, 'https://s3.amazonaws.com/shakirachatbot/singing_files/nanxxx.mp3', None)


def create_audio_file():
    try:
        response = polly.synthesize_speech(
            Text='And I\'m on tonight you know my hips don\'t lie and I\'m starting to feel it\'s right. All the attraction, the tension, Don\'t you see baby, this is perfection',
            OutputFormat="mp3",
            VoiceId="Joanna")
        with closing(response["AudioStream"]) as stream:
            bucket.put_object(Key='singing_files/{}.mp3'.format('nanxxx'), Body=stream.read())
    except BotoCoreError as error:
        logging.error(error)


def helper(intent_request):
    logger.info(intent_request)

    return close(intent_request['sessionAttributes'], 'Fulfilled', secure_random.choice(HELPER_RESPONSES))


def random_gif(intent_request):
    logger.info(intent_request)

    s3_client = boto3.client('s3', region_name='us-east-1')
    gif = secure_random.choice(list(bucket.objects.filter(Prefix='gifs/')))
    url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, gif.bucket_name, gif.key)

    return close_with_response_card(intent_request['sessionAttributes'],
                                    'Fulfilled', None, None, None, url, url)


def social_media(intent_request):
    logger.info(intent_request)

    return {'sessionAttributes': intent_request['sessionAttributes'],
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {'contentType': 'PlainText',
                            'content': 'Here are her social networks, keep in touch! ;)'},
                'responseCard': {'version': '0',
                                 'contentType': 'application/vnd.amazonaws.card.generic',
                                 'genericAttachments': [{
                                     'title': 'www.shakira.com',
                                     'subTitle': 'https://twitter.com/shakira\nhttps://www.facebook.com/shakira'
                                 }]}}}


def when_concert(intent_request):
    logger.info(intent_request)

    slots = get_slots(intent_request)
    location_slot = slots['location']

    if location_slot is None:
        return elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           slots, 'location', 'In which city / venue?')

    locations = [s for s in fetch_concert_locations() if location_slot.lower() in s.lower()]
    response = format_concerts(location_slot, locations)
    if 'ElicitSlot' in response:
        return elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           slots, 'location', response['ElicitSlot'])
    elif 'Close' in response:
        return close(intent_request['sessionAttributes'], 'Fulfilled', response['Close'])


""" --- Intents Handling --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'AboutAlbum':
        return about_album(intent_request)
    elif intent_name == 'AboutSong':
        return about_song(intent_request)
    elif intent_name == 'Helper':
        return helper(intent_request)
    elif intent_name == 'RandomGif':
        return random_gif(intent_request)
    elif intent_name == 'SocialMedia':
        return social_media(intent_request)
    elif intent_name == 'WhenConcert':
        return when_concert(intent_request)

    raise Exception('Intent ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    logger.debug('event = {}'.format(event))

    return dispatch(event)
