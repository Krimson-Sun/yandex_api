import sys
from io import BytesIO
import pygame
import os
import requests
from PIL import Image
import math


LAT_STEP = 0.008
LON_STEP = 0.002
coord_to_geo_x = 0.0000428
coord_to_geo_y = 0.0000428
z = 17





toponym_to_find = ''
lon = '37.530887'
lat = '55.703118'
params = {
    "ll": ",".join([lon, lat]),
    "z": z,
    "l": "map"
}
api_server = "http://static-maps.yandex.ru/1.x"
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()


def new_image():
    global api_server, map_file, params
    response = requests.get(api_server, params=params)
    os.remove(map_file)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP and z < 17:
                z += 1
                params['z'] = z
                new_image()
            if event.key == pygame.K_PAGEDOWN and z > 0:
                z -= 1
                params['z'] = z
                new_image()
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()


pygame.quit()
os.remove(map_file)