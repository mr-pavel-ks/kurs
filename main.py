import requests, json, os


class BackupClient:

    def __init__(self, vk_id, Token_vk, Token_YA):
        self.vk_id = vk_id
        self.Token_vk = Token_vk
        self.Token_ya = Token_YA

    def download_photos(self, count_photo=5):
        api = requests.get('https://api.vk.com/method/photos.get', params={
            'owner_id': self.vk_id,
            'access_token': self.Token_vk,
            'photo_sizes': 0,
            'v': 5.122,
            'album_id': 'profile',
            'extended': 1
        })
        items = api.json()['response']['items']
        self.name_list = []
        json_log_list = []
        i = 0
        for name in items:
            if i < count_photo:
                file_name = name['likes']['count']
                data = name['date']
                sizes = name['sizes']
                if file_name in self.name_list:
                    file_name = str(file_name) + str(data)
                self.name_list.append(file_name)
                url = sizes[-1:][0]['url']
                size = sizes[-1:][0]['type']
                with open(os.path.join('image/', f'{file_name}.jpg'), 'wb') as f:
                    image_response = requests.get(url)
                    f.write(image_response.content)
                    print(f'Файл {file_name} успешно скачан с ВК')
                    json_dict = {}
                    json_dict['file_name'] = file_name
                    json_dict['size'] = size
                    json_log_list.append(json_dict)
                    with open('log_vk.json', 'w') as w_f:
                        json.dump(json_log_list, w_f)
                    i += 1
        print('json файл создан')

    def upload_photos(self):
        for name_ya in self.name_list:
            api_ya = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                  headers={'Authorization': Token_YA},
                                  params={'path': f'image/{name_ya}', 'overwrite': True})
            url_yandex1 = api_ya.json()
            url_yandex = url_yandex1["href"]
            with open(f'image/{name_ya}.jpg', 'rb') as file_ya:
                api_yandex = requests.put(url_yandex, data=file_ya)
                print(f'Файл {name_ya} успешно загружен на Яндекс диск')


if __name__ == '__main__':
    vk_id = int(input('Введите ID пользователя ВК '))
    Token_vk = input('Введите Ваш токен ВК ')
    Token_YA = input('Введите Ваш токен с полигона Яндекс диска ')

    backup_client = BackupClient(vk_id, Token_vk, Token_YA)

    backup_client.download_photos()

    backup_client.upload_photos()