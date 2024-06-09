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


# class ElevatorCall:
#
#     def is_on_button(self, button_center_coordinates, point):
#         return eucledian_distance(button_center_coordinates, point) < BUTTON_RADIUS


class RunGame:

    def __init__(self):

        building = build_test(1, 10)

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

        elevator_image = pygame.image.load(ELEVATOR_IMAGE).convert_alpha()
        building.cunstruct_elevators(1, elevator_image)

        exit = False

        current_seconds = 0
        # pygame.time.set_timer(pygame.USEREVENT, 1000)
        clock = pygame.time.Clock()

        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        last_time = pygame.time.get_ticks()

        while not exit:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == TIMEREVENT:
                    current_time = pygame.time.get_ticks()
                    time_elapsed = current_seconds - last_time
                    last_time = current_time

                    for floor in range(len(building.timers)):
                        if building.timers[floor] > 0:
                            building.timers[floor] -= 0.6

                            # if building.timers[floor] < 0:
                            #     building.timers[floor] = 0

                    for floor in range(len(building.timers)):
                        screen.fill(WHITE, (190, 550 - floor *58, 200, 25))
                        font = pygame.font.Font(None, 25)
                        time_text = font.render(f'{building.timers[floor]:.1f}', True, BLACK)
                        screen.blit(time_text, (190, 550 - (floor * 58) + 10))

                    # for floor in range(len(building.timers)):
                    #     if building.timers[floor] > 0:
                    #         building.timers[floor] -= 0.50
                    #
                    #         if building.timers[floor] < 0.5:
                    #             building.timers[floor] = 0
                    #
                    #         current_timer = round(building.timers[floor], 2)
                    #         print(current_timer)
                    #
                    #         screen.fill((255, 255, 255), (190, 550 - floor * 58, 200, 25))
                    #         # current_timer = building.timers[floor]
                    #         font = pygame.font.Font(None, 25)
                    #
                    #         time_text = font.render(f'{current_timer}', True, BLACK)
                    #         screen.blit(time_text, (190, 550 - (floor * 58) + 10))
                            # screen.blit(timer_cover, timer_cover.get_rect(center=(400, 550 - floor * 58)))

                        # current_seconds = building.timers[floor]
                        # pygame.time.set_timer(pygame.USEREVENT, 1000)
                        #
                        # while True:
                        #     for event_t in pygame.event.get():
                        #         if event_t.type == pygame.QUIT:
                        #             pygame.quit()
                        #             sys.exit()
                        #         if event.type == pygame.USEREVENT:
                        #             current_seconds -= 1
                        #     # screen.blit(timer_cover, timer_cover.get_rect(center=(400, 550 - floor * 58)))
                        #
                        #     timer_text = FONT.render(f"{current_seconds}", True, [255, 255, 255])
                        #     screen.blit(timer_text, (400, 550 - floor * 58))
                else:
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

            pygame.display.flip()
            building.elevator_group.clear(screen, background)
            building.elevator_group.update(screen)
            building.elevator_group.draw(screen)
            pygame.display.update()


RunGame()
