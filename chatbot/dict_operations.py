from resources.concerts import CONCERTS
from resources.albums import ALBUMS


def fetch_albums():
    return set(ALBUMS.keys())


def fetch_songs():
    response = []
    for album in ALBUMS:
        response.extend(ALBUMS[album]['songs'])
    return set(response)


def find_album_by_name(album_name):
    return ALBUMS[album_name]


def fetch_concert_locations():
    return fetch_concert_cities() | fetch_concert_countries() | fetch_concert_areas() | fetch_concert_venues()


def fetch_concert_cities():
    return set(CONCERTS.keys())


def fetch_concert_countries():
    response = []
    for concert in CONCERTS:
        response.append(CONCERTS[concert]['country'])
    return set(response)


def fetch_concert_areas():
    response = []
    for concert in CONCERTS:
        response.append(CONCERTS[concert]['area'])
    return set(response)


def fetch_concert_venues():
    response = []
    for concert in CONCERTS:
        response.append(CONCERTS[concert]['venue'])
    return set(response)


def find_concerts_by_country(country):
    response = []
    for concert in CONCERTS:
        if CONCERTS[concert]['country'] == country:
            response.append(concert)
    return list(set(response))


def find_concerts_by_area(area):
    response = []
    for concert in CONCERTS:
        if CONCERTS[concert]['area'] == area:
            response.append(concert)
    return list(set(response))


def find_concerts_by_venue(venue):
    response = []
    for concert in CONCERTS:
        if CONCERTS[concert]['venue'] == venue:
            response.append(concert)
    return list(set(response))


def is_city(location):
    return location in fetch_concert_cities()


def is_country(location):
    return location in fetch_concert_countries()


def is_venue(location):
    return location in fetch_concert_venues()


def is_area(location):
    return location in fetch_concert_areas()


def format_concerts(location_slot, location_name):
    if len(location_name) == 0:
        return {'Close': 'I\'m so sorry :( There are no concerts scheduled in ' + location_slot + '. #PrayForShakConcerts'}
    else:
        location_name = location_name[0]
        if is_city(location_name):
            return format_single_location(location_name)
        elif is_country(location_name):
            locations = find_concerts_by_country(location_name)
            if len(locations) == 1:
                return format_single_location(locations[0])
            else:
                return format_multiple_locations(location_name, locations)
        elif is_venue(location_name):
            location = find_concerts_by_venue(location_name)
            return format_single_location(location[0])
        elif is_area(location_name):
            location = find_concerts_by_area(location_name)
            return format_multiple_locations(location_name, location)


def format_single_location(location_name):
    location = CONCERTS[location_name]
    return {'Close': 'She\'ll perform in ' + location_name + ', ' + location['country'] + ' in ' + location['venue'] + ' on ' + location['date'].strftime('%A %d of %B') + '. You can look for tickets at ' + location['tickets'] + ' #LetsPlayAGame'}


def format_multiple_locations(location_name, locations):
    return {'ElicitSlot': 'She\'ll perform in ' + str(len(locations)) + ' cities of ' + location_name + ' (' + ', '.join(locations) + '). Please tell me a city and I\'ll tell you more about that concert :) '}
