# coding=utf-8
import chatbot.botcontrol as botcontrol


def test_about_album_unspecified_album():
    response = botcontrol.about_album(intent_request_mock('AboutAlbum', {u'album': None}))
    assert response['dialogAction']['type'] == 'ElicitSlot'


def test_about_album():
    response = botcontrol.about_album(intent_request_mock('AboutAlbum', {u'album': 'Pies Descalzos'}))
    assert response['dialogAction']['type'] == 'Close'


def test_about_album_partial_name():
    response = botcontrol.about_album(intent_request_mock('AboutAlbum', {u'album': 'Oral Fixation'}))
    assert response['dialogAction']['type'] == 'Close'


def test_about_album_with_accent():
    response = botcontrol.about_album(intent_request_mock('AboutAlbum', {u'album': 'Dónde Están los Ladrones?'}))
    assert response['dialogAction']['type'] == 'Close'


def test_about_song_unspecified_song():
    response = botcontrol.about_song(intent_request_mock('AboutSong', {u'song': None}))
    assert response['dialogAction']['type'] == 'ElicitSlot'


def test_about_song():
    response = botcontrol.about_song(intent_request_mock('AboutSong', {u'song': 'Chantaje'}))
    assert response['dialogAction']['type'] == 'Close'


def test_deal_with_it_negative():
    response = botcontrol.deal_with_it(intent_request_mock('DealWithIt', None, 'Agh, you suck!'))
    assert response['dialogAction']['message']['content'] == 'That\'s a pity :/ ...nah, I KNOW I\'m pretty amazing!'


def test_deal_with_it_neutral():
    response = botcontrol.deal_with_it(intent_request_mock('DealWithIt', None, 'bah'))
    assert response['dialogAction']['message']['content'] == 'Bah, ok, whatever ;)'


def test_deal_with_it_positive():
    response = botcontrol.deal_with_it(intent_request_mock('DealWithIt', None, 'I love you'))
    assert response['dialogAction']['message']['content'] == 'And, you, YOU are amazing!'


def test_greeting():
    botcontrol.greeting(intent_request_mock('Greeting', None))


def test_helper():
    botcontrol.helper(intent_request_mock('Helper', None))


def test_random_gif():
    botcontrol.random_gif(intent_request_mock('RandomGif', None))


def test_social_media():
    botcontrol.social_media(intent_request_mock('SocialMedia', None))


def test_sing_a_song_from_session_attribute():
    response = botcontrol.sing_a_song(intent_request_mock('Sing', {u'song': None}))
    assert response['dialogAction']['message']['content'] == 'I still don\'t know {}, but I can sing another one ;)'.format(response['sessionAttributes']['song'])


def test_sing_a_song_from_slot():
    response = botcontrol.sing_a_song(intent_request_mock('Sing', {u'song': 'Hips don\'t lie'}))
    assert response['dialogAction']['message']['content'] == 'This is your lucky day! I can sing that one :)'


def test_thanks():
    botcontrol.thanks(intent_request_mock('Thanks', None))


def test_when_concert_unspecified_location():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': None}))
    assert response['dialogAction']['type'] == 'ElicitSlot'


def test_when_concert_with_city_without_concert():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': 'Bogota'}))
    assert response['dialogAction']['type'] == 'Close'


def test_when_concert_with_city():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': 'Miami'}))
    assert response['dialogAction']['type'] == 'Close'


def test_when_concert_with_multiple_concerts_country():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': 'United States'}))
    assert response['dialogAction']['type'] == 'ElicitSlot'


def test_when_concert_with_single_concert_country():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': 'Switzerland'}))
    assert response['dialogAction']['type'] == 'Close'


def test_when_concert_by_venue():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': 'Olympiahalle'}))
    assert response['dialogAction']['type'] == 'Close'


def test_when_concert_by_area():
    response = botcontrol.when_concert(intent_request_mock('WhenConcert', {u'location': 'Europe'}))
    assert response['dialogAction']['type'] == 'ElicitSlot'


def intent_request_mock(intent_name, slot, input_transcript='anything'):
    return {u'currentIntent': {u'slots': slot, u'name': intent_name, u'confirmationStatus': u'None'},
            u'bot': {u'alias': None, u'version': u'$LATEST', u'name': u'ShakiraChatbot'},
            u'userId': u'dq64axgllu3znz8j663b23rh7nohadni', u'inputTranscript': input_transcript,
            u'invocationSource': u'DialogCodeHook', u'outputDialogMode': u'Text', u'messageVersion': u'1.0',
            u'sessionAttributes': {u'song': u'Chantaje'}}
