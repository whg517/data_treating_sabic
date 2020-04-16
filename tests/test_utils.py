import os

from data_treating_sabic.utils import (duplicates, load_config,
                                       update_config_filename_to_path)


def test_load_config(fixture_data_dir):
    config_file = os.path.join(fixture_data_dir, 'demo.yml')
    configs = load_config(config_file)
    assert type(configs) is list
    assert len(configs) == 1
    assert configs[0].get('province') == 'beijing'
    assert configs[0].get('location') == 'beijing'


def test_update_word_bag_config_filename_to_path():
    word_config = {
        'raw': {
            'filename': '词典库_39012000_v7.xlsx',
        },
        'wordbag': {
            'filename': '词典库_39012000_v7.xlsx',
            'supplier': {
                'filename': '词典库_39012000_v7.xlsx'
            }
        }
    }
    word_bag_file_dir = '/data'
    updated_word = update_config_filename_to_path(word_config, word_bag_file_dir)
    assert updated_word == {
        'raw': {
            'filename': '/data/词典库_39012000_v7.xlsx',
        },
        'wordbag': {
            'filename': '/data/词典库_39012000_v7.xlsx',
            'supplier': {
                'filename': '/data/词典库_39012000_v7.xlsx'
            }
        }
    }


def test_duplicates_1():
    data = {
        'abc': 123,
        'bc': 456,
        'ad': 000,
        'bcd': 000
    }
    duplicated = duplicates(data)
    assert duplicated == {
        'abc': 123,
        'ad': 000,
        'bcd': 000
    }
