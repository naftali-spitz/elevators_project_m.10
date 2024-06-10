import pygame

from Floor import Floor
from Elevator1 import Elevator

ELEVATOR_IMAGE = 'elv-small.png'
BRICK_TEXTURE = 'brick-texture.png'
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [180, 180, 180]
BUTTON_RADIUS = 20


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

    #
    # def floor_pos(self, y):
    #     """Calculate the position of a floor based on the y-coordinate
    #
    #     Arg:
    #         y (init): The y-coordinate of the floor.
    #     Returns:
    #         tuple: The position of the floor.
    #         """
    #     floor_pos_x = 10
    #     FLOOR_POS.append((floor_pos_x + 75, y + 25))

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
        min_time = float('inf')
        for elevator in self.elevator_group:
            test_min_time = elevator.total_travel_length(current_floor)

            if test_min_time < min_time:
                selected_elevator = elevator
                min_time = test_min_time

        selected_elevator.add_destination(current_floor)

        self.timers[current_floor] = min_time / 232
        # print(self.timers)
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
