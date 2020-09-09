import requests, json, os, pprint


class get_photo_VK():
    def get_photo(self):
        Token_VK = ''
        api = requests.get('https://api.vk.com/method/photos.get', params={
            'owner_id': 1,
            'access_token': Token_VK,
            'photo_size': 1,
            'v': 5.122,
            'album_id': 'profile',
            'extended': 1
        })

        items = json.loads((api.text))['response']['items']
        name_list = []
        for name in items:
            file_name = name['likes']['count']
            data = name['date']
            sizes = name['sizes']
            if file_name in name_list:
                file_name = str(file_name) + str(data)
            name_list.append(file_name)
            for url_dict in sizes:
                url = url_dict['url']

                with open(os.path.join('image', f'{file_name}.jpg'), 'wb') as f:
                    image_response = requests.get(url)
                    f.write(image_response.content)

class load_photo_ya():
    def write_files(self):
        Token_YA = ''
        api_ya = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
        headers={'Authorization': Token_YA},
        params = {'path': file_name})
        url_yandex1 = json.loads((api_ya.text))
        url_yandex = url_yandex1["href"]

        with open(f'image/{file_name}, 'rb') as file_ya:
            api_yandex = requests.put(url_yandex, data=file_ya)

# get_photo_VK().get_photo()
load_photo_ya().write_files()
