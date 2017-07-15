import chatbot.lex_slot_builder as lex_slot_builder
import chatbot.dict_operations as dict_operations


def test_build_songs_dict():
    assert len(lex_slot_builder.build_songs_slot()) == len(dict_operations.fetch_songs())


def test_build_albums_dict():
    assert len(lex_slot_builder.build_albums_slot()) == len(dict_operations.fetch_albums())


def test_build_concert_locations_dict():
    assert len(lex_slot_builder.build_concert_locations_slot()) == len(dict_operations.fetch_concert_locations())
