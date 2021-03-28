import datetime
import os
import shutil
import sys
import time
import requests
from tqdm import tqdm


class YaDiskUser:
    def __init__(self, token):
        self.token = token
        if self.token == '':
            print('Ошибка! Не указан токен!')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, ya_disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': ya_disk_file_path, 'overwrite': 'false'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, urls_dict, user_id):
        create_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        date_now = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        folder_name = f'{user_id} {date_now}'
        params = {'path': folder_name}
        response = requests.put(url=create_folder_url, headers=headers, params=params)
        if response.status_code == 201:
            if os.path.exists('photos_temp'):
                shutil.rmtree('photos_temp')
            os.mkdir('photos_temp')
            print(f'Прогресс загрузки файлов на Яндекс.Диск в папку с именем "{folder_name}":')
            for filename in tqdm(urls_dict):
                time.sleep(0.1)
                with open(f'photos_temp/{filename}', 'wb'):
                    href = self.get_upload_link(ya_disk_file_path=f'{folder_name}/{filename}').get('href', '')
                    response = requests.put(href, data=requests.get(urls_dict[filename]).content)
                    response.raise_for_status()
                    if response.status_code != 201:
                        print('Произошла ошибка загрузки на Яндекс.Диск!')
                        sys.exit()
            shutil.rmtree('photos_temp')
            print('Все фотографии успешно загружены на Яндекс.Диск!')
        else:
            print('Произошла ошибка загрузки на Яндекс.Диск!')
            sys.exit()
