import dict_operations


def build_songs_slot():
    return build_enum_dictionary(dict_operations.fetch_songs())


def build_albums_slot():
    return build_enum_dictionary(dict_operations.fetch_albums())


def build_concert_locations_slot():
    return build_enum_dictionary(dict_operations.fetch_concert_locations())


def build_enum_dictionary(value_list):
    content = []
    for i in value_list:
        d = {unicode('value'): unicode(i, 'utf-8')}
        content.append(d)
    return content
