""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {'contentType': 'PlainText', 'content': message}
        }
    }
    return response


def close_with_response_card(session_attributes, fulfillment_state, message, title, subtitle, attachment, image_url):
    response = {'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': fulfillment_state,
                    'message': {'contentType': 'PlainText', 'content': message},
                    'responseCard': {'version': '0',
                                     'contentType': 'application/vnd.amazonaws.card.generic',
                                     'genericAttachments': [{
                                         'title': title,
                                         'subTitle': subtitle,
                                         'attachmentLinkUrl': attachment,
                                         'imageUrl': image_url}]}}}
    return response


# def close_with_voice(session_attributes, audio_stream):
#     response = {'sessionAttributes': session_attributes,
#                 # 'contentType': audio_stream['ContentType'],
#                 'contentType': 'audio/mpeg',
#                 'dialogState': 'Fulfilled',
#                 'contentType': 'audio/x-l16; sample-rate=16000',
#                 'inputTranscript': 'Good Morning',
#                 'audioStream': audio_stream}
#     return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {'contentType': 'PlainText', 'content': message}
        }
    }


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']
