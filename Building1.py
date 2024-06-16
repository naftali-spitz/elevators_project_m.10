import pygame

from Floor import Floor
from Elevator1 import Elevator

ELEVATOR_IMAGE = 'resources/elv-small.png'
BRICK_TEXTURE = 'resources/brick-texture.png'
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [180, 180, 180]
BUTTON_RADIUS = 20
FLOOR_TRANSIT_TIME = 0.5



def eucledian_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Building:
    """Class representing a building in a game."""

    def __init__(self, floor_count):
        """Initialize the Building object.

        Arg:
            floor_count (int): The number of floors in the building.
            """
        self.floors = pygame.sprite.Group()
        self.elevator_group = pygame.sprite.Group()
        self.timers = [0] * (floor_count + 1)

    def construct_floors(self, num_of_floors, image, screen):
        """construct the floors of the building.

        Arg:
            num_of_floors (int): The number of floors to construct.
            image (Surface): The image of the floor.
            screen (Surface): The game screen surface.
            """

        for i in range(num_of_floors):

            brick_y = 550 - i * 58
            line_y = brick_y - 3

            brick_texture = image
            brick_texture_width, brick_texture_height = brick_texture.get_size()

            brick_texture_center_x = brick_texture_width // 2
            brick_texture_center_y = brick_texture_height // 2

            pygame.draw.circle(brick_texture, GRAY, (brick_texture_center_x, brick_texture_center_y), BUTTON_RADIUS)

            floor_num_text = Floor.floor_panel(self, 10, i)

            if i != num_of_floors - 1:
                pygame.draw.line(screen, BLACK, (10, line_y), (159, line_y), 7)

            screen.blit(brick_texture, (10, brick_y))
            screen.blit(floor_num_text, (brick_texture_center_x + 6, brick_y + brick_texture_center_y - 7))

            floor = Floor(i, brick_texture, brick_y)
            self.floors.add(floor)

    def construct_elevators(self, number_of_elevators, image):
        """Construct the elevators in the building.

        Arg:
            number_of_elevators (int): The number of elevators to construct.
            image (Surface): The image of the elevator.
            """
        init_elevator_x_position = 250
        for i in range(number_of_elevators):
            elevator = Elevator(i, image, (init_elevator_x_position + i * 55))
            self.elevator_group.add(elevator)

    def call_some_elevator(self, current_floor):
        """Call an elevator to the specified floor.

        Args:
            current_floor (int): The current floor to call the elevator.

        Returns:
            Elevator: The selected elevator to respond to the call.
        """
        selected_elevator = None
        min_pixels_to_travel = float('inf')
        for elevator in self.elevator_group:
            test_pixels_to_travel = elevator.total_travel_length(current_floor)

            if test_pixels_to_travel < min_pixels_to_travel:
                selected_elevator = elevator
                min_pixels_to_travel = test_pixels_to_travel

        selected_elevator.add_destination(current_floor)

        self.timers[current_floor.id] = min_pixels_to_travel / 116

        return selected_elevator

    def is_on_button(self, button_center_coordinates, point):
        """Check if a point is within the range of a button on the screen.

            Args:
                button_center_coordinates (tuple): The center coordinates of the button.
                point (tuple): The coordinates of the point to check.
            Returns:
                bool: True if the point is within the range of the button, False otherwise.
            """
        return eucledian_distance(button_center_coordinates, point) < BUTTON_RADIUS

    def update(self, screen):
        self.elevator_group.update(screen, self.timers)
        # for floor in self.floors:
        #
        #     travel_time = self.timers[floor.id] / speed
        #
        #     screen.fill((255, 255, 255), (190, 500, 200, 25))
        #
        #     font = pygame.font.Font(None, 25)
        #
        #     time_text = font.render(f'{round((travel_time - 1) / 100, 2)}', True, BLACK)
        #     screen.blit(time_text, (190, 500 + 10))
        current_seconds = 0
        # current_time = pygame.time.get_ticks()
        # last_time = current_time
        # time_elapsed = current_seconds - last_time
        clock = 60/15
        # TEAL_TO_REAL_TIME_RATIO = 0.8
        # last_time = pygame.time.get_ticks()
        for time in range(len(self.timers)):
            if self.timers[time] > 0:
                self.timers[time] -= ((1 * clock) / 116)

            if self.timers[time] < FLOOR_TRANSIT_TIME:
                self.timers[time] = 0

                # Building.set_floor_panel_color(building.floors.sprites()[floor], True)

                for floor in range(len(self.timers)):
                    screen.fill(WHITE, (190, 550 - floor * 58, 200, 25))
                    font = pygame.font.Font(None, 25)
                    time_text = font.render(f'00:{self.timers[floor]:.02f}', True, BLACK)
                    screen.blit(time_text, (190, 550 - (floor * 58) + 10))

