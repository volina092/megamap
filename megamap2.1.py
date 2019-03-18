import sys
import requests
import pygame
import os


toponym_to_find = 'Москва, ул. Тверская, д. 8'
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {"geocode": toponym_to_find, "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)


json_response = response.json()
#print(json_response)

toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]

# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta_x = 0.1
delta_y = 0.1

#print(str(delta_x), str(delta_y)) 

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([str(delta_x), str(delta_y)]),
    "l": "map"
}
 
map_api_server = "http://static-maps.yandex.ru/1.x/"
#и выполняем запрос
response = requests.get(map_api_server, params=map_params)

map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(response.content)
#ВСЁ, КАРТИНКУ МЫ СКАЧАЛИ!!!

except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)
 
# тут pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #скроллим вверх
                delta_x = min(delta_x * 1.1, 75)
                delta_y = min(delta_y * 1.1, 75)
            if event.button == 5: #скроллим вниз
                delta_x = max(delta_x * 0.9, 0.0001)
                delta_y = max(delta_y * 0.9, 0.0001)
            
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            #smth
            pass       
        if keystate[pygame.K_RIGHT]:
            #smth
            pass
        if keystate[pygame.K_UP]:
            #smth
            pass
        if keystate[pygame.K_DOWN]:
            #smth
            pass
        
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(delta_x), str(delta_y)]),
        "l": "map"
    }
     
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)
pygame.quit()