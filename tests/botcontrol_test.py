import chatbot.botcontrol as botcontrol


def test_about_album_unspecified_album():
    response = botcontrol.about_album(intent_request_mock('AboutAlbum', {u'album': None}))
    assert response['dialogAction']['type'] == 'ElicitSlot'


def test_about_album():
    response = botcontrol.about_album(intent_request_mock('AboutAlbum', {u'album': 'Pies Descalzos'}))
    assert response['dialogAction']['type'] == 'Close'


def test_about_song():
    botcontrol.about_song(intent_request_mock('AboutSong', {u'song': None}))


def test_about_song():
    botcontrol.about_song(intent_request_mock('AboutSong', {u'song': 'Chantaje'}))


def test_random_gif():
    botcontrol.random_gif(intent_request_mock('RandomGif', None))


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


def intent_request_mock(intent_name, slot):
    return {u'currentIntent': {u'slots': slot, u'name': intent_name, u'confirmationStatus': u'None'},
            u'bot': {u'alias': None, u'version': u'$LATEST', u'name': u'ShakiraChatbot'},
            u'userId': u'dq64axgllu3znz8j663b23rh7nohadni', u'inputTranscript': u'about any',
            u'invocationSource': u'DialogCodeHook', u'outputDialogMode': u'Text', u'messageVersion': u'1.0',
            u'sessionAttributes': None}
