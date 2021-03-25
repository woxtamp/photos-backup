import datetime
import time

import requests


class VkApiUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        if self.token == '':
            print('Ошибка! Не указан Вконтакте!')

        self.version = version
        if self.version == '':
            print('Ошибка! Не указана версия API Вконтакте!')
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_photos(self, owner_id, album_id, photos_count=5):
        getphotos_url = self.url + 'photos.get'
        getphotos_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': 1,
            'feed_type': 'photo',
            'photo_sizes': 1,
            'offset': 0,
            'count': 1
        }
        response = requests.get(getphotos_url, params={**self.params, **getphotos_params})
        if response.status_code == 200:
            real_count = response.json()['response']['count']
            print(f'В выбранном альбоме {real_count} фотографий')
            sizes_dict = {}
            if photos_count <= real_count:
                while getphotos_params['offset'] <= photos_count - 1:
                    for items in response.json()['response']['items']:
                        time.sleep(0.33)
                        if str(items['likes']['count']) + '.jpg' not in sizes_dict and str(
                                items['likes']['count']) + ' ' + str(datetime.datetime.fromtimestamp(items['date'])) + '.jpg' not in sizes_dict:
                            height = 0
                            max_size_type = ''
                            for size in items['sizes']:
                                if height < size['height']:
                                    height = size['height']
                                    max_size_type = size['type']
                            sizes_dict[str(items['likes']['count']) + '.jpg'] = max_size_type
                        elif str(items['likes']['count']) + '.jpg' in sizes_dict:
                            height = 0
                            max_size_type = ''
                            for size in items['sizes']:
                                if height < size['height']:
                                    height = size['height']
                                    max_size_type = size['type']
                            sizes_dict[str(items['likes']['count']) + ' ' + str(datetime.datetime.fromtimestamp(items['date'])) + '.jpg'] = max_size_type
                    getphotos_params['offset'] += 1
                    response = requests.get(getphotos_url, params={**self.params, **getphotos_params})
            else:
                print('Вы хотите сохранить больше фотографий, чем есть в альбоме!')
            print(sizes_dict)
        else:
            print('Ошибка!')
