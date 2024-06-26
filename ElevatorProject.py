import json
import pygame
from Building import Building

with open('Data.json','r') as file:
    Data = json.load(file)


class RunGame:
    """Class responsible for running the elevator project game."""

    def __init__(self):
        """Initialize the RunGame object and set up the game environment."""

        pygame.init()

        number_of_floors = int(input('how many floor do you want to initialise:'))
        number_of_elevators = int(input('How many elevators do you want to initialise:'))

        icon = pygame.image.load('resources/134185_elevator_icon.png')

        screen = pygame.display.set_mode((Data["BOX_LEN"], Data["BOX_HEIGHT"]))
        background = pygame.Surface((Data["BOX_LEN"], Data["BOX_HEIGHT"]))
        background.fill('WHITE')
        screen.fill('WHITE')
        pygame.display.set_caption("MEFATCHIM ELEVATOR PROJECT")
        pygame.display.set_icon(icon)

        floor_image = pygame.image.load(Data["BRICK_TEXTURE"]).convert()
        elevator_image = pygame.image.load(Data["ELEVATOR_IMAGE"]).convert_alpha()
        building = Building(number_of_floors, floor_image, number_of_elevators, elevator_image, screen)
        clock = pygame.time.Clock()

        exit = False
        while not exit:
            clock.tick(60)
            elv = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        current_x, current_y = pygame.mouse.get_pos()
                        for floor in building._floors:
                            current_x_button, current_y_button = floor.get_rect().center
                            if building.is_on_button((current_x_button, current_y_button), (current_x, current_y)):
                                building.call_some_elevator(floor, screen, background)

            building.elevator_group.clear(screen, background)
            building.update(screen)
            building.elevator_group.draw(screen)
            pygame.display.update()


RunGame()
