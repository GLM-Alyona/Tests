import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))

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


class TestSecretary(unittest.TestCase):
    def setUp(self):
        app.documents[:] = copy.deepcopy(INITIAL_DOCUMENTS)
        app.directories.clear()
        app.directories.update(copy.deepcopy(INITIAL_DIRECTORIES))

    def test_check_document_existance_true(self):
        self.assertTrue(app.check_document_existance('11-2'))

    def test_check_document_existance_false(self):
        self.assertFalse(app.check_document_existance('0000'))

    def test_get_doc_owner_name(self):
        self.assertEqual(app.get_doc_owner_name('10006'), 'Аристарх Павлов')

    def test_get_doc_owner_name_unknown(self):
        self.assertIsNone(app.get_doc_owner_name('unknown'))

    @patch('builtins.input', return_value='11-2')
    def test_get_doc_owner_name_from_input(self, _mocked_input):
        self.assertEqual(app.get_doc_owner_name(), 'Геннадий Покемонов')

    def test_get_all_doc_owners_names(self):
        self.assertEqual(
            app.get_all_doc_owners_names(),
            {'Василий Гупкин', 'Геннадий Покемонов', 'Аристарх Павлов'},
        )

    def test_get_doc_shelf(self):
        self.assertEqual(app.get_doc_shelf('10006'), '2')

    def test_add_new_shelf(self):
        shelf_number, created = app.add_new_shelf('4')
        self.assertEqual(shelf_number, '4')
        self.assertTrue(created)
        self.assertIn('4', app.directories)
        self.assertEqual(app.directories['4'], [])

    def test_add_existing_shelf(self):
        shelf_number, created = app.add_new_shelf('1')
        self.assertEqual(shelf_number, '1')
        self.assertFalse(created)

    def test_add_new_doc(self):
        shelf = app.add_new_doc('42', 'passport', 'Иван Иванов', '3')
        self.assertEqual(shelf, '3')
        self.assertTrue(app.check_document_existance('42'))
        self.assertEqual(app.get_doc_owner_name('42'), 'Иван Иванов')
        self.assertIn('42', app.directories['3'])

    def test_delete_doc(self):
        doc_number, deleted = app.delete_doc('11-2')
        self.assertEqual(doc_number, '11-2')
        self.assertTrue(deleted)
        self.assertFalse(app.check_document_existance('11-2'))
        self.assertNotIn('11-2', app.directories['1'])

    def test_delete_unknown_doc(self):
        doc_number, deleted = app.delete_doc('missing')
        self.assertEqual(doc_number, 'missing')
        self.assertFalse(deleted)

    def test_show_document_info(self):
        info = app.show_document_info(app.documents[0])
        self.assertEqual(info, 'passport "2207 876234" "Василий Гупкин"')

    def test_move_doc_to_shelf(self):
        message = app.move_doc_to_shelf('10006', '3')
        self.assertIn('10006', message)
        self.assertEqual(app.get_doc_shelf('10006'), '3')
        self.assertNotIn('10006', app.directories['2'])


if __name__ == '__main__':
    unittest.main()
