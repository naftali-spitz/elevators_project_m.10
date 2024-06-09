import pygame
from Elevator1 import Elevator
import Building1
from Building1 import Building as build_test
from Floor import Floor
import sys

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


class ScreenBox:
    def __init__(self, initialX, initialY, width, height, background):
        self.x = initialX
        self.y = initialY
        self.width = width
        self.height = height


class ElevatorCall:

    def is_on_button(self, button_center_coordinates, point):
        return eucledian_distance(button_center_coordinates, point) < BUTTON_RADIUS


class RunGame:

    def __init__(self):

        building = build_test(1, 9)

        pygame.init()

        # Icon = pygame.image.load(ELEVATOR_IMAGE)
        color1 = (255, 255, 255)
        box_len = 800
        box_hight = 600
        FONT = pygame.font.Font("ArialRoundedMTBold.ttf", 25)

        screen = pygame.display.set_mode((box_len, box_hight))
        background = pygame.Surface((box_len, box_hight))
        background.fill((255, 255, 255))
        screen.fill(color1)
        pygame.display.set_caption("ELOVATOR PROJECT")
        # pygame.display.set_icon(Icon)

        floor_image = pygame.image.load(BRICK_TEXTURE).convert()
        building.cunsruct_floors(10, floor_image, screen)
        # for i in building.floors:
        #     a = pygame.draw.circle(i.image, GRAY, (i.rect.centerx, i.rect.centery), BUTTON_RADIUS)
        #     screen.blit(a)

        elevator_image = pygame.image.load(ELEVATOR_IMAGE).convert_alpha()
        building.cunstruct_elevators(1, elevator_image)

        exit = False

        current_seconds = 0
        # pygame.time.set_timer(pygame.USEREVENT, 1000)
        clock = pygame.time.Clock()

        while not exit:
            clock.tick(80)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                else:
                    # building.test_elv_call()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        current_x, current_y = pygame.mouse.get_pos()
                        for i in range(len(Building1.FLOOR_POS)):
                            # if FLOOR_POS[i] <= current_y <= FLOOR_POS[i] + 50 and 10 <= current_x <= 160:
                            current_x_button, current_y_button = Building1.FLOOR_POS[i]
                            if building.is_on_button((current_x_button, current_y_button), (current_x, current_y)):
                                font = pygame.font.Font(None, 25)
                                floor_num_text = font.render(f"{i}", True, (0, 255, 0))
                                screen.blit(floor_num_text, (81, Building1.FLOOR_POS[i][1] - 7))
                                building.call_some_elevator(i)
                                # current_floor_sprite = building.floors.sprites()[i]
                                # current_floor_sprite.time_pending = min_time


            building.elevator_group.clear(screen, background)
            building.elevator_group.update(screen)
            building.elevator_group.draw(screen)
            pygame.display.update()


RunGame()