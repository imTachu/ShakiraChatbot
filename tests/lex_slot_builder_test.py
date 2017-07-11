import chatbot.lex_slot_builder as lex_slot_builder
import chatbot.botcontrol as botcontrol


def test_build_songs_dict():
    assert len(lex_slot_builder.build_songs_slot()) == len(botcontrol.fetch_songs())


def test_build_albums_dict():
    assert len(lex_slot_builder.build_albums_slot()) == len(botcontrol.fetch_albums())


def test_build_concert_locations_dict():
    assert len(lex_slot_builder.build_concert_locations_slot()) == len(botcontrol.fetch_concert_locations())
