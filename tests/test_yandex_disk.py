import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))

from yandex_disk import YandexDisk


class TestYandexDisk(unittest.TestCase):
    def setUp(self):
        self.disk = YandexDisk('test-token')

    @patch('yandex_disk.requests.put')
    def test_create_folder_success(self, mocked_put):
        mocked_put.return_value = Mock(status_code=201)
        response = self.disk.create_folder('netology_test_folder')
        self.assertIn(response.status_code, (200, 201))
        mocked_put.assert_called_once()

    @patch('yandex_disk.requests.get')
    def test_folder_appears_in_file_list(self, mocked_get):
        mocked_get.return_value = Mock(
            status_code=200,
            json=lambda: {'type': 'dir', 'name': 'netology_test_folder'},
        )
        self.assertTrue(self.disk.folder_exists('netology_test_folder'))

    @patch('yandex_disk.requests.put')
    def test_create_folder_unauthorized(self, mocked_put):
        mocked_put.return_value = Mock(status_code=401)
        response = self.disk.create_folder('netology_test_folder')
        self.assertEqual(response.status_code, 401)

    @patch('yandex_disk.requests.put')
    def test_create_folder_already_exists(self, mocked_put):
        mocked_put.return_value = Mock(status_code=409)
        response = self.disk.create_folder('netology_test_folder')
        self.assertEqual(response.status_code, 409)

    @patch('yandex_disk.requests.get')
    def test_folder_not_found(self, mocked_get):
        mocked_get.return_value = Mock(status_code=404, json=lambda: {})
        self.assertFalse(self.disk.folder_exists('missing_folder'))


if __name__ == '__main__':
    unittest.main()
