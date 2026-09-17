import copy
from unittest.mock import patch

import pytest

import app


INITIAL_DOCUMENTS = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
]

INITIAL_DIRECTORIES = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': [],
}


@pytest.fixture(autouse=True)
def reset_secretary_data():
    app.documents[:] = copy.deepcopy(INITIAL_DOCUMENTS)
    app.directories.clear()
    app.directories.update(copy.deepcopy(INITIAL_DIRECTORIES))


@pytest.mark.parametrize(
    'doc_number, expected',
    [
        ('2207 876234', True),
        ('11-2', True),
        ('10006', True),
        ('0000', False),
        ('unknown', False),
    ],
)
def test_check_document_existance(doc_number, expected):
    assert app.check_document_existance(doc_number) is expected


@pytest.mark.parametrize(
    'doc_number, expected_name',
    [
        ('2207 876234', 'Василий Гупкин'),
        ('11-2', 'Геннадий Покемонов'),
        ('10006', 'Аристарх Павлов'),
        ('unknown', None),
    ],
)
def test_get_doc_owner_name(doc_number, expected_name):
    assert app.get_doc_owner_name(doc_number) == expected_name


@pytest.mark.parametrize(
    'doc_number, expected_shelf',
    [
        ('2207 876234', '1'),
        ('11-2', '1'),
        ('10006', '2'),
        ('unknown', None),
    ],
)
def test_get_doc_shelf(doc_number, expected_shelf):
    assert app.get_doc_shelf(doc_number) == expected_shelf


@pytest.mark.parametrize(
    'shelf_number, expected_created',
    [
        ('4', True),
        ('1', False),
        ('2', False),
    ],
)
def test_add_new_shelf(shelf_number, expected_created):
    number, created = app.add_new_shelf(shelf_number)
    assert number == shelf_number
    assert created is expected_created
    assert shelf_number in app.directories


@pytest.mark.parametrize(
    'doc_number, expected_deleted',
    [
        ('11-2', True),
        ('10006', True),
        ('missing', False),
    ],
)
def test_delete_doc(doc_number, expected_deleted):
    number, deleted = app.delete_doc(doc_number)
    assert number == doc_number
    assert deleted is expected_deleted
    if expected_deleted:
        assert app.check_document_existance(doc_number) is False


def test_get_doc_owner_name_from_input():
    with patch('builtins.input', return_value='11-2'):
        assert app.get_doc_owner_name() == 'Геннадий Покемонов'


def test_get_all_doc_owners_names():
    assert app.get_all_doc_owners_names() == {
        'Василий Гупкин',
        'Геннадий Покемонов',
        'Аристарх Павлов',
    }


def test_add_new_doc():
    shelf = app.add_new_doc('42', 'passport', 'Иван Иванов', '3')
    assert shelf == '3'
    assert app.check_document_existance('42')
    assert app.get_doc_owner_name('42') == 'Иван Иванов'
    assert '42' in app.directories['3']


def test_show_document_info():
    info = app.show_document_info(app.documents[0])
    assert info == 'passport "2207 876234" "Василий Гупкин"'


def test_move_doc_to_shelf():
    message = app.move_doc_to_shelf('10006', '3')
    assert '10006' in message
    assert app.get_doc_shelf('10006') == '3'
    assert '10006' not in app.directories['2']
