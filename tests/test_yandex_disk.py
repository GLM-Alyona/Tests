from unittest.mock import Mock, patch

import pytest

from yandex_disk import YandexDisk


@pytest.fixture
def disk():
    return YandexDisk('test-token')


def test_create_folder_then_appears_in_file_list(disk):
    folder_name = 'netology_test_folder'

    with patch('yandex_disk.requests.put') as mocked_put, patch(
        'yandex_disk.requests.get'
    ) as mocked_get:
        mocked_put.return_value = Mock(status_code=201)
        mocked_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                '_embedded': {
                    'items': [
                        {'type': 'dir', 'name': folder_name},
                        {'type': 'file', 'name': 'readme.txt'},
                    ]
                }
            },
        )

        create_response = disk.create_folder(folder_name)

        assert create_response.status_code in (200, 201)
        assert disk.folder_in_file_list(folder_name)
        mocked_put.assert_called_once()
        mocked_get.assert_called_once()


@pytest.mark.parametrize('status_code', [400, 401, 403, 409])
def test_create_folder_error_codes(status_code, disk):
    with patch('yandex_disk.requests.put') as mocked_put:
        mocked_put.return_value = Mock(status_code=status_code)
        response = disk.create_folder('netology_test_folder')
        assert response.status_code == status_code


def test_folder_not_found(disk):
    with patch('yandex_disk.requests.get') as mocked_get:
        mocked_get.return_value = Mock(status_code=404, json=lambda: {})
        assert disk.folder_exists('missing_folder') is False
        assert disk.folder_in_file_list('missing_folder') is False
