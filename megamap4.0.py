
import sys
import requests
import pygame
import os

FOR_L = ['map', 'sat', 'sat,skl']
INDEX = 0

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

delta_x = 0.001
delta_y = 0.001

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

class Button:
    def __init__(self):
        cir_y = os.path.join('but_cir_y.png')
        self.kind_pic = pygame.image.load(cir_y)
        self.kind_pic_x, self.kind_pic_y = (550, 10)
    def render(self):
        screen.blit(self.kind_pic, (self.kind_pic_x, self.kind_pic_y))
    def clicked(self, pos):
        global INDEX
        x, y = pos
        if (self.kind_pic_x < x < (self.kind_pic_x + 40) and
            self.kind_pic_y < y < (self.kind_pic_y + 41)):
            INDEX += 1
            print('an important click')
            self.render()
            pygame.display.flip()
            
        else:
            print('just a click')
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
button = Button()
pygame.display.flip()

running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #скроллим вверх
                delta_x *= 1.1
                delta_y *= 1.1
            if event.button == 5: #скроллим вниз
                delta_x *= 0.9
                delta_y *= 0.9
            button.clicked(event.pos)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            tl = float(toponym_longitude)
            tl -= 0.003
            toponym_lattitude = str(tl)
            
        if keystate[pygame.K_RIGHT]:
            tl = float(toponym_longitude)
            tl += 0.003
            toponym_lattitude = str(tl)
            
        if keystate[pygame.K_UP]:
            tl = float(toponym_lattitude)
            tl += 0.003
            toponym_lattitude = str(tl)
            
        if keystate[pygame.K_DOWN]:
            tl = float(toponym_lattitude)
            tl -= 0.003
            toponym_lattitude = str(tl)
        
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(delta_x), str(delta_y)]),
        "l": FOR_L[INDEX % 3]
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
    button.render()
    pygame.display.flip()
    os.remove(map_file)
pygame.quit()