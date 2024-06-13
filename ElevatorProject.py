import pygame
from Elevator1 import Elevator
from Building1 import Building

ELEVATOR_IMAGE = 'resources/elv-small.png'
BRICK_TEXTURE = 'resources/brick-texture.png'
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [180, 180, 180]
# BUTTON_RADIUS = 20
FLOOR_TRANSIT_TIME = 0.5


# BUILDING_INIT_X = 10


class ScreenBox:
    def __init__(self, initialX, initialY, width, height, background):
        self.x = initialX
        self.y = initialY
        self.width = width
        self.height = height


class RunGame:
    """Class responsible for running the elevator project game."""

    def __init__(self):
        """Initialize the RunGame object and set up the game environment."""

        pygame.init()

        number_of_floors = int(input('how many floor do you want to initialise:'))
        number_of_elevators = int(input('How many elevators do you want to initialise:'))

        Icon = pygame.image.load('resources/134185_elevator_icon.png')
        box_len = 800
        box_hight = 600
        FONT = pygame.font.Font("resources/ArialRoundedMTBold.ttf", 25)

        screen = pygame.display.set_mode((box_len, box_hight))
        background = pygame.Surface((box_len, box_hight))
        background.fill(WHITE)
        screen.fill(WHITE)
        pygame.display.set_caption("MEFATCHIM ELEVATOR PROJECT")
        pygame.display.set_icon(Icon)

        building = Building(number_of_floors)

        floor_image = pygame.image.load(BRICK_TEXTURE).convert()
        building.construct_floors(number_of_floors, floor_image, screen)

        elevator_image = pygame.image.load(ELEVATOR_IMAGE).convert_alpha()
        building.construct_elevators(number_of_elevators, elevator_image)

        current_seconds1 = building.timers

        current_seconds = 0
        clock = pygame.time.Clock()
        TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMEREVENT, 1000)
        last_time = pygame.time.get_ticks()

        exit = False
        while not exit:
            clock.tick(60)
            elv = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True

                # elif event.type == TIMEREVENT:
                    # current_time = pygame.time.get_ticks()
                    # time_elapsed = current_seconds - last_time
                    # last_time = current_time
                    # # print(time_elapsed)
                    # # last_time = pygame.time.get_ticks()
                    # for floor in range(len(building.timers)):
                    #     if building.timers[floor] > 0:
                    #         building.timers[floor] -= FLOOR_TRANSIT_TIME
                    #
                    #     if building.timers[floor] < FLOOR_TRANSIT_TIME:
                    #         building.timers[floor] = 0
                    #
                    #         # Building.set_floor_panel_color(building.floors.sprites()[floor], True)
                    #
                    #     for floor in range(len(building.timers)):
                    #         screen.fill(WHITE, (190, 550 - floor * 58, 200, 25))
                    #         font = pygame.font.Font(None, 25)
                    #         time_text = font.render(f'{building.timers[floor]:.1f}', True, BLACK)
                    #         screen.blit(time_text, (190, 550 - (floor * 58) + 10))

                    # for floor in range(len(building.timers)):
                    #     if building.timers[floor] > 0:
                    #         building.timers[floor] -= 0.50
                    #
                    #         if building.timers[floor] < 0.5:
                    #             building.timers[floor] = 0

                            # current_timer = building.timers[floor]

                            # screen.fill((255, 255, 255), (190, 550 - floor * 58, 200, 25))
                            # # current_timer = building.timers[floor]
                            # font = pygame.font.Font(None, 25)
                            #
                            # time_text = font.render(f'{current_timer}', True, BLACK)
                            # screen.blit(time_text, (190, 550 - (floor * 58) + 10))
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
                        for floor in building.floors:
                            current_x_button, current_y_button = floor.rect.center
                            if building.is_on_button((current_x_button, current_y_button), (current_x, current_y)):
                                font = pygame.font.Font(None, 25)
                                floor_num_text = font.render(f"{floor.id}", False, (0, 255, 0))
                                screen.blit(floor_num_text, (floor.rect.centerx - 4, floor.rect.centery - 7))
                                elv = building.call_some_elevator(floor)

            building.elevator_group.clear(screen, background)
            building.update(screen)
            building.elevator_group.draw(screen)
            pygame.display.update()


RunGame()
