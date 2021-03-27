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
        if response.status_code == 200 and 'error' not in response.json():
            real_count = response.json()['response']['count']
            print(f'В выбранном альбоме {real_count} фотографий')
            sizes_dict = {}
            urls_dict = {}
            if photos_count <= real_count:
                while getphotos_params['offset'] <= photos_count - 1:
                    for items in response.json()['response']['items']:
                        time.sleep(0.33)
                        if str(items['likes']['count']) + '.jpg' not in sizes_dict and str(
                                items['likes']['count']) + ' ' + str(datetime.datetime.fromtimestamp(items['date'])) + '.jpg' not in sizes_dict:
                            height = 0
                            max_size_type = ''
                            max_size_url = ''
                            for size in items['sizes']:
                                if size['height'] == 0:
                                    max_size_type = size['type']
                                    max_size_url = size['url']
                                elif height < size['height']:
                                    height = size['height']
                                    max_size_type = size['type']
                                    max_size_url = size['url']
                            sizes_dict[str(items['likes']['count']) + '.jpg'] = max_size_type
                            urls_dict[str(items['likes']['count']) + '.jpg'] = max_size_url
                        elif str(items['likes']['count']) + '.jpg' in sizes_dict:
                            height = 0
                            max_size_type = ''
                            max_size_url = ''
                            for size in items['sizes']:
                                if size['height'] == 0:
                                    max_size_type = size['type']
                                    max_size_url = size['url']
                                if height < size['height']:
                                    height = size['height']
                                    max_size_type = size['type']
                                    max_size_url = size['url']
                            sizes_dict[str(items['likes']['count']) + ' ' + str(datetime.datetime.fromtimestamp(items['date'])) + '.jpg'] = max_size_type
                            urls_dict[str(items['likes']['count']) + ' ' + str(datetime.datetime.fromtimestamp(items['date'])) + '.jpg'] = max_size_url
                    getphotos_params['offset'] += 1
                    response = requests.get(getphotos_url, params={**self.params, **getphotos_params})
            else:
                print('Вы хотите сохранить больше фотографий, чем есть в альбоме!')
            print(sizes_dict)
            print(urls_dict)
        elif 'error' in response.json():
            print(f'Ошибка! {response.json()["error"]["error_msg"]}! Код ошибки: {response.json()["error"]["error_code"]}.')
        else:
            print('Произошла ошибка! Попробуйте ещё раз!')
