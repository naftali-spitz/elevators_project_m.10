import json
import pygame
import time
from Elevator import Elevator
from Floor import Floor

with open('Data.json','r') as file:
    Data = json.load(file)


def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Building:
    """Class representing a building in a game."""

    def __init__(self, number_of_floors, floor_image, number_of_elevators, elevator_image, screen):
        """Initialize the Building object.

        Arg:
            floor_count (int): The number of floors in the building.
            """
        self._floors = pygame.sprite.Group()
        self.elevator_group = pygame.sprite.Group()
        self.timers = [0] * (number_of_floors + 1)
        self.construct_floors(number_of_floors, floor_image, screen)
        self.construct_elevators(number_of_elevators, elevator_image)
        self.last_tick = 0

    def construct_floors(self, num_of_floors, image, screen):
        """construct the floors of the building.

        Arg:
            num_of_floors (int): The number of floors to construct.
            image (Surface): The image of the floor.
            screen (Surface): The game screen surface.
            """

        for i in range(num_of_floors):

            brick_y = Data["INITIAL_FLOOR_Y"] - i * Data["FLOOR_HEIGHT"]
            line_y = brick_y - 3

            brick_texture = image
            brick_texture_width, brick_texture_height = brick_texture.get_size()

            brick_texture_center_x = brick_texture_width // 2
            brick_texture_center_y = brick_texture_height // 2

            pygame.draw.circle(brick_texture, 'GRAY', (brick_texture_center_x, brick_texture_center_y),
                               Data["BUTTON_RADIUS"])

            floor_num_text = Floor.floor_panel(self, 10, i)

            if i != num_of_floors - 1:
                pygame.draw.line(screen, 'BLACK', (10, line_y), (159, line_y), 7)

            screen.blit(brick_texture, (10, brick_y))
            screen.blit(floor_num_text, (brick_texture_center_x + 6, brick_y + brick_texture_center_y - 7))

            floor = Floor(i, brick_texture, brick_y)
            self._floors.add(floor)

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

    def call_some_elevator(self, current_floor, screen, background):
        """Call an elevator to the specified floor.

        Args:
            current_floor: The current floor to call the elevator.

        Returns:
            Elevator: The selected elevator to respond to the call.
            :param current_floor:
            :param screen:
        """
        if current_floor.get_timer() > 0:
            return
        selected_elevator = None
        min_pixels_to_travel = float('inf')
        for elevator in self.elevator_group:
            test_pixels_to_travel = elevator.total_travel_length(current_floor)

            if test_pixels_to_travel < min_pixels_to_travel:
                selected_elevator = elevator
                min_pixels_to_travel = test_pixels_to_travel

        selected_elevator.add_destination(current_floor)
        call_status = True
        current_floor.update_floor_call(min_pixels_to_travel, call_status, screen)

        # self.elevator_group.clear(screen, background)
        # self.update(screen)
        # self.draw(screen)

    def is_on_button(self, button_center_coordinates, point):
        """Check if a point is within the range of a button on the screen.

            Args:
                button_center_coordinates (tuple): The center coordinates of the button.
                point (tuple): The coordinates of the point to check.
            Returns:
                bool: True if the point is within the range of the button, False otherwise.
            """
        return euclidean_distance(button_center_coordinates, point) < Data["BUTTON_RADIUS"]

    def update(self, screen):
        self.elevator_group.update(screen, self.timers)

        current_tick = pygame.time.get_ticks()
        time_delta = current_tick - self.last_tick  # Calculate time difference since last frame
        self.last_tick = current_tick  # Update last_tick for next frame

        for floor in self._floors:
            if floor.get_timer() > 0:
                timer = time_delta / 1000
                floor.update_timer(timer)

            if floor.get_timer() <= 0:
                call_status = False
                min_pixels_to_travel = 0
                floor.update_floor_call(min_pixels_to_travel, call_status, screen)

                for floors in self._floors:
                    floor_num = floors.get_id()
                    screen.fill('WHITE', (190, 550 - floor_num * 58, 70, 25))
                    font = pygame.font.Font(None, 25)
                    time_text = font.render(f'{floors.get_timer():.01f}', True, 'BLACK')
                    screen.blit(time_text, (190, 550 - (floor_num * 58) + 10))
