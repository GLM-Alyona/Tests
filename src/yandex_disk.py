import requests

API_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
SUCCESS_CODES = {200, 201}


class YandexDisk:
    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {'Authorization': f'OAuth {self.token}'}

    def create_folder(self, path):
        return requests.put(API_URL, headers=self._headers(), params={'path': path}, timeout=20)

    def get_resource(self, path):
        return requests.get(API_URL, headers=self._headers(), params={'path': path}, timeout=20)

    def list_files(self, path='/'):
        return self.get_resource(path)

    def folder_exists(self, path):
        response = self.get_resource(path)
        return response.status_code in SUCCESS_CODES and response.json().get('type') == 'dir'

    def folder_in_file_list(self, folder_name, parent_path='/'):
        response = self.list_files(parent_path)
        if response.status_code not in SUCCESS_CODES:
            return False

        items = response.json().get('_embedded', {}).get('items', [])
        return any(
            item.get('type') == 'dir' and item.get('name') == folder_name
            for item in items
        )
