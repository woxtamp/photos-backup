import sys
import requests
import time
import datetime
import json
from tqdm import tqdm



class VkApiUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        if self.token == '':
            print('Ошибка! Не указан токен Вконтакте!')

        self.version = version
        if self.version == '':
            print('Ошибка! Не указана версия API Вконтакте!')
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_albums(self, owner_id):
        getalbums_url = self.url + 'photos.getAlbums'
        getalbums_params = {
            'owner_id': owner_id,
            'need_system': 1
        }
        albums_ids = []
        albums_select_number = []
        albums_select_name = []
        count = 0
        response = requests.get(getalbums_url, params={**self.params, **getalbums_params})
        if response.status_code == 200 and 'error' not in response.json():
            for items in response.json()['response']['items']:
                count += 1
                albums_ids.append(items['id'])
                albums_select_number.append(count)
                albums_select_name.append(items['title'])
            print('Введите цифру соответствующую номеру альбома из которого нужно сохранить фотографии')
            for album in albums_select_number:
                print(f'{album} - "{albums_select_name[albums_select_number.index(album)]}"')
            album_number = input()
            if album_number.isdecimal():
                if int(album_number) in albums_select_number:
                    return albums_ids[int(album_number) - 1]
                else:
                    print('Вы ввели номер несуществующего альбома!')
            else:
                print('Ошибка! Введено не число')
        elif 'error' in response.json():
            print(f'Ошибка! {response.json()["error"]["error_msg"]}! Код ошибки: {response.json()["error"]["error_code"]}.')
            print('Будет выбран альбом "Фотографии со страницы".')
            return 'profile'
        else:
            print('Произошла ошибка! Попробуйте ещё раз!')
            sys.exit()

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
            print(f'В выбранном альбоме {real_count} фото.')
            sizes_dict = {}
            urls_dict = {}
            output_data = []
            if real_count == 0:
                print('Ошибка! В выбранном альбоме нет фотографий, сохранять нечего! Попробуйте выбрать другой альбом.')
                sys.exit()
            if photos_count >= real_count:
                print(f'Вы хотите сохранить больше фотографий, чем есть в альбоме. Будет сохранено только {real_count} фото.')
                photos_count = real_count
            while getphotos_params['offset'] <= photos_count - 1:
                for items in tqdm(response.json()['response']['items']):
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
            output_dict = {}
            with open('output.json', 'w') as file:
                for item in sizes_dict:
                    output_dict['file_name'] = item
                    output_dict['size'] = sizes_dict[item]
                    output_data.append(output_dict)
                    output_dict = {}
                json.dump(output_data, file, ensure_ascii=False, indent=2)
        elif 'error' in response.json():
            print(f'Ошибка! {response.json()["error"]["error_msg"]}! Код ошибки: {response.json()["error"]["error_code"]}.')
        else:
            print('Произошла ошибка! Попробуйте ещё раз!')
