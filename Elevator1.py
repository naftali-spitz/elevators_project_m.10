import time

import pygame
from collections import deque
from itertools import pairwise

ELEVATOR_IMAGE = 'elv-small.png'
BRICK_TEXTURE = 'brick-texture.png'
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [180, 180, 180]
FLOOR_POS = []
BUTTON_RADIUS = 20
FLOOR_TRANSIT_TIME = 0.5
ID_N = 0
BUILDING_X = 10
DEST = -1
PIXELS_PER_SECOND = 116

class Elevator(pygame.sprite.Sprite):

    def __init__(self, id, image, x):
        super().__init__()
        self.id = id
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 550)
        self.speed = 0
        self.destination = []
        self.destinations = deque(maxlen=20)
        self.last_destination_time = 0
        self.current_destination_index = 0
        # self.current_floor = 0
        # self.current_des_floor = None

    def move_stop_elevator(self, speed):
        self.speed = speed

    def update(self, screen):

        if len(self.destinations) == 0:
            return
        current_time = time.time()
        if current_time - self.last_destination_time >= 2:

            target_y = self.destinations[0]
            # print(self.destinations[0])

            if self.rect.y != target_y:
                dis_to_target = abs(self.rect.y - target_y)
                if dis_to_target > 50:
                    self.move_stop_elevator(2)
                    if self.rect.y > target_y:
                        self.rect.y -= self.speed
                    else:
                        self.rect.y += self.speed
                else:
                    self.move_stop_elevator(1)
                    if self.rect.y > target_y:
                        self.rect.y -= 1
                    else:
                        self.rect.y += 1
            else:
                self.destinations.popleft()
                self.move_stop_elevator(0)

                ding_sound = pygame.mixer.Sound('ding.mp3')
                # ding_sound.play()

                self.last_destination_time = current_time
                self.current_destination_index += 1

                if self.current_destination_index >= len(self.destinations):
                    self.current_destination_index = 0

    def floor_to_y(floor):
        return 550 - (floor * 58)

    def total_travel_length(self, destination_floor):
        destination = Elevator.floor_to_y(destination_floor)

        length = 0
        des_copy = list(self.destinations)
        des_copy.insert(0, self.rect.y)
        if destination in des_copy:
            des_copy = des_copy[0:des_copy.index(destination)]
        des_copy.append(destination)

        for [current, next] in pairwise(des_copy):
            length += abs(current - next)

        count_of_floors = len(des_copy) - 2

        return length + (count_of_floors * 2 * PIXELS_PER_SECOND)

    def add_destination(self, destination_floor):
        self.destinations.append(Elevator.floor_to_y(destination_floor))
