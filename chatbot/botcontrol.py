# coding=utf-8
from __future__ import print_function
from chatbot.dict_operations import fetch_concert_locations, fetch_albums, fetch_songs, find_album_by_name, find_album_by_song, format_concerts
from chatbot.lex_handler import close, close_with_response_card, delegate, elicit_slot, get_slots
from resources.helper_responses import HELPER_RESPONSES
from contextlib import closing
import boto3
import logging
import os
import random
import unirest
import urllib
from botocore.exceptions import BotoCoreError, ClientError


SENTIMENT_ANALYSIS_API = 'https://twinword-sentiment-analysis.p.mashape.com/analyze/?text={}'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3 = boto3.resource('s3', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
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
        response = 'I\'m so sorry, I don\'t think she has an album ' + str(album_slot) + '.'
    else:
        album_name = albums[0]
        album = find_album_by_name(album_name)
        response = album_name + ' was released on ' + album['release_date'].strftime('%A %d of %B of %Y') + '. Its songs are: \n* ' + '\n* '.join(album['songs'])
    return close(intent_request['sessionAttributes'], 'Fulfilled', response)


def about_song(intent_request):
    logger.info(intent_request)

    slots = get_slots(intent_request)
    song_slot = slots['song']

    if song_slot is None:
        return elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           slots, 'song', 'About what song do you want to know?')

    song = [s for s in fetch_songs() if song_slot.lower() in s.lower()][0]
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    album_name = find_album_by_song(song)
    album = find_album_by_name(album_name)
    response = song + ' is part of the album ' + album_name + ' which was released on ' + album['release_date'].strftime('%A %d of %B of %Y') + '.'
    output_session_attributes['song'] = song
    return close(output_session_attributes, 'Fulfilled', response)


def deal_with_it(intent_request):
    logger.info(intent_request)

    response = unirest.get(
        SENTIMENT_ANALYSIS_API.format(urllib.quote_plus(intent_request['inputTranscript'])),
        headers={
            'X-Mashape-Key': os.environ['MASHAPE_API_KEY'],
            'Accept': 'application/json'
        }
        )
    sentiment_type = response.body['type']
    if sentiment_type == 'positive':
        return close_with_response_card(intent_request['sessionAttributes'], 'Fulfilled', 'And, you, YOU are amazing!', '<3 <3 <3', None,
                                        'https://s3.amazonaws.com/shakirachatbot/gifs/dealwithit_p.gif', 'https://s3.amazonaws.com/shakirachatbot/gifs/dealwithit_p.gif')
    elif sentiment_type == 'neutral':
        return close(intent_request['sessionAttributes'], 'Fulfilled', 'Bah, ok, whatever ;)')
    elif sentiment_type == 'negative':
        return close_with_response_card(intent_request['sessionAttributes'], 'Fulfilled', 'That\'s a pity :/ ...nah, I KNOW I\'m pretty amazing!', '#DealWithIt', None,
                                        'https://s3.amazonaws.com/shakirachatbot/gifs/dealwithit_n.gif', 'https://s3.amazonaws.com/shakirachatbot/gifs/dealwithit_n.gif')


def greeting(intent_request):
    logger.info(intent_request)

    return close(intent_request['sessionAttributes'], 'Fulfilled', 'Hello! :D, if in doubt on what to ask, type: examples')


def helper(intent_request):
    logger.info(intent_request)

    return close(intent_request['sessionAttributes'], 'Fulfilled', secure_random.choice(HELPER_RESPONSES))


def random_gif(intent_request):
    logger.info(intent_request)

    gif = secure_random.choice(list(bucket.objects.filter(Prefix='gifs/')))
    url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, gif.bucket_name, gif.key)
    return close_with_response_card(intent_request['sessionAttributes'], 'Fulfilled', 'You can always ask for more gifs!', 'A gif :)', None, url, url)


def sing_a_song(intent_request):
    logger.info(intent_request)

    slots = get_slots(intent_request)
    song_slot = slots['song']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    song_from_session = output_session_attributes.get('song')
    if song_from_session is None and song_slot is None:
        return elicit_slot(output_session_attributes,
                           intent_request['currentIntent']['name'],
                           slots, 'song', 'What song do you want me to sing?')
    if song_slot is not None:
        song = song_slot
    else:
        song = song_from_session
    if str(song).lower() == 'Hips don\'t lie'.lower():
        response = 'This is your lucky day! I can sing that one :)'
    else:
        response = 'I still don\'t know {}, but I can sing another one ;)'.format(song)
    filename = 'singing_files/shak_{}.mp3'.format(secure_random.random())
    try:
        audio_stream = polly.synthesize_speech(
            Text='And I\'m on tonight, you know my hips don\'t lie and I\'m starting to feel it\'s right. All the attraction, the tension, don\'t you see baby, this is perfection.',
            OutputFormat='mp3',
            VoiceId='Joanna')
        with closing(audio_stream['AudioStream']) as stream:
            bucket.put_object(Key=filename, Body=stream.read(), ACL='public-read')
    except BotoCoreError as error:
        logging.error(error)

    return close_with_response_card(intent_request['sessionAttributes'], 'Fulfilled', response, 'Click it, that\'s me singing', None, '{}/{}/{}'.format(s3_client.meta.endpoint_url, bucket.name, filename), 'https://s3.amazonaws.com/shakirachatbot/play_icon.png')


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


def thanks(intent_request):
    logger.info(intent_request)

    return close(intent_request['sessionAttributes'], 'Fulfilled', 'Anytime gorgeous! :3')


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

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'AboutAlbum':
        return about_album(intent_request)
    elif intent_name == 'AboutSong':
        return about_song(intent_request)
    elif intent_name == 'DealWithIt':
        return deal_with_it(intent_request)
    elif intent_name == 'Greeting':
        return greeting(intent_request)
    elif intent_name == 'Helper':
        return helper(intent_request)
    elif intent_name == 'RandomGif':
        return random_gif(intent_request)
    elif intent_name == 'Sing':
        return sing_a_song(intent_request)
    elif intent_name == 'SocialMedia':
        return social_media(intent_request)
    elif intent_name == 'Thanks':
        return thanks(intent_request)
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
