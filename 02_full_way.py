import sys
import requests
import pygame
import os

# Пусть наше приложение предполагает запуск:
#python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:



toponym_to_find = 'Москва, ул. Тверская'
 
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
 
geocoder_params = {"geocode": toponym_to_find, "format": "json"}
 
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    # обработка ошибочной ситуации
    pass
 
# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
print(json_response)

toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")



toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']

print(toponym)
# Координаты центра топонима:
toponym_coodrinates = toponym['boundedBy']['Envelope']
print(toponym_coodrinates)
# Долгота и широта:
t1, t2 = toponym_coodrinates['lowerCorner'], toponym_coodrinates['upperCorner']

xs = []
ys = []
xs.append(float(t1.split()[0])) 
xs.append(float(t2.split()[0])) 
ys.append(float(t1.split()[1])) 
ys.append(float(t2.split()[1])) 


 
delta_x = max(xs) - min(xs)
delta_y = max(ys) - min(ys)

print(str(delta_x), str(delta_y)) 
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([str(delta_x), str(delta_y)]),
    "l": "map"
}
 
map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(response.content)
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)
 
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
 
# Удаляем за собой файл с изображением.
os.remove(map_file)