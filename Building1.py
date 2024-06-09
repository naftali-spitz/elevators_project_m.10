import pygame
from queue import Queue
from itertools import pairwise
from collections import deque

import Elevator1
from Floor import Floor
from Elevator1 import Elevator
from bisect import bisect_left
import numpy as np

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


def eucledian_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Building:
    def __init__(self, elevator_count, floor_count):
        # self.floors = [Floor for floor in range(floor_count)]
        self.floors = pygame.sprite.Group()
        self.elevator_group = pygame.sprite.Group()
        self.timers = [0] * floor_count

    def floor_pos(self, y):
        floor_pos_x = 10
        FLOOR_POS.append((floor_pos_x + 75, y + 25))

    def cunsruct_floors(self, num_of_floors, image, screen):

        for i in range(num_of_floors):

            brick_y = 550 - i * 58
            line_y = 547 - i * 58

            brick_texture = pygame.image.load(BRICK_TEXTURE).convert()
            brick_texture_width, brick_texture_height = brick_texture.get_size()

            brick_texture_center_x = brick_texture_width // 2
            brick_texture_center_y = brick_texture_height // 2

            pygame.draw.circle(brick_texture, GRAY, (brick_texture_center_x, brick_texture_center_y), BUTTON_RADIUS)

            floor_num_text = Floor.floor_panel(self, 10, i)

            if i != num_of_floors - 1:
                pygame.draw.line(screen, BLACK, (10, line_y), (159, line_y), 7)

            self.floor_pos(brick_y)

            screen.blit(brick_texture, (10, brick_y))
            screen.blit(floor_num_text, (brick_texture_center_x + 6, brick_y + brick_texture_center_y - 7))

            floor_sprite = Floor(i, brick_texture, brick_y)
            self.floors.add(floor_sprite)

    # def reached_floor(self, floor_reached):
    #     Floor.

    # def cunstruct_floors1(self,screen, number_of_floors, image):
    #     init_y = 10

    #     for i in range(number_of_floors):
    #         floor = Floor(i, image, init_y, screen)
    #         # pygame.draw.circle(image, GRAY, (floor.rect.centerx+80, floor.rect.centery), BUTTON_RADIUS)
    #         if i != number_of_floors - 1:
    #             line_y = 546 - i * 58
    #             pygame.draw.line(screen, BLACK, (10, line_y), (159, line_y), 7)

    # self.elevator_group.add(floor)
    # print(self.elevator_group)

    def cunstruct_elevators(self, number_of_elevators, image):
        init_x = 220
        for i in range(number_of_elevators):
            elevator = Elevator(i, image, (init_x + i * 55))
            self.elevator_group.add(elevator)

    def call_some_elevator(self, current_floor):
        selected_elevator = None
        min_time = float('inf')
        for elevator in self.elevator_group:
            test_min_time = elevator.total_travel_length(current_floor)
            if test_min_time < min_time:
                selected_elevator = elevator
                min_time = test_min_time

        selected_elevator.add_destination(current_floor)
        self.timers[current_floor] = min_time
        return selected_elevator

    # def elevator(self, floor):
    #     arrival_time = floor * FLOOR_TRANSIT_TIME
    #     elv_calls_queue.put((floor, arrival_time))

    def current_floor(self, elevator_num):
        if not self.elv_calls_queue.empty:
            current_floor = self.elv_calls_queue.queue[self.elv_calls_queue.qsize() - 1]
            return current_floor[elevator_num][1]
        else:
            return 0

    def is_on_button(self, button_center_coordinates, point):
        return eucledian_distance(button_center_coordinates, point) < BUTTON_RADIUS
