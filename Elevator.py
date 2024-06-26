import json
import time
import pygame
from collections import deque
from itertools import pairwise

with open('Data.json', 'r') as file:
    Data = json.load(file)


def convert_floor_num_to_y_coordinate(floor):
    """Converts a floor number to the y-coordinate."""
    return Data["INITIAL_FLOOR_Y"] - (floor.get_id() * Data["FLOOR_HEIGHT"])


def convert_y_coordinate_to_floor_num(y):
    """Converts a y-coordinate to the floor number."""
    return abs((Data["INITIAL_FLOOR_Y"] - y) / - Data["FLOOR_HEIGHT"])


class Elevator(pygame.sprite.Sprite):
    """Class representing an elevator in a game."""

    def __init__(self, id, image, x):
        """Initialize the Elevator object.
        Arg:
            id (int): The unique identifier of the elevator.
            image (Surface): The image representation of the elevator
            x (int): The x-coordinate of the elevator's initial position.
        """
        super().__init__()
        self._id = id
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 550)
        self._speed = 0
        self._destinations = deque(maxlen=20)
        self._last_destination_time = 0
        self._current_destination_index = 0
        self._travel_time = 0
        self._last_time = 0
        self._delay = 0


    def set_elevator_speed(self, speed):
        """Set the speed of the elevator."""
        self._speed = speed


    def update(self, screen, timers):
        """Update the elevator's position based on its destinations."""

        if len(self._destinations) == 0:
            return
        current_time = pygame.time.get_ticks()

        if current_time - self._last_destination_time >= Data["DELAY_AT_ARRIVAL"] * 1000:
            target_y = self._destinations[0]

            if self.rect.y != target_y:

                self.move_elev(target_y, screen, timers)
            else:
                ding_sound = pygame.mixer.Sound(Data["DING"])
                ding_sound.play()

                self._destinations.popleft()
                self.set_elevator_speed(Data["SPEED_STOP"])

                self._last_destination_time = current_time
                self._current_destination_index += 1

                if self._current_destination_index >= len(self._destinations):
                    self._current_destination_index = 0


    def total_travel_length(self, destination_floor):
        """Calculate the total travel length to a destination floor.
        Args:
            destination_floor (int): The destination floor number.
        Returns:
            int: The total travel length in pixels.
            """
        destination = convert_floor_num_to_y_coordinate(destination_floor)
        length = 0
        des_copy = list(self._destinations)

        des_copy.insert(0, self.rect.y)
        if destination in des_copy:
            des_copy = des_copy[0:des_copy.index(destination)]
        des_copy.append(destination)

        for [current, next] in pairwise(des_copy):
            length += abs(current - next)

        add_delay = 0
        if pygame.time.get_ticks() - self._last_destination_time <= Data["DELAY_AT_ARRIVAL"] * 1000:
            add_delay = (Data["DELAY_AT_ARRIVAL"] * 1000) - (pygame.time.get_ticks() - self._last_destination_time)
            add_delay = (add_delay / 1000) * Data["PIXELS_PER_SECOND"]
        count_of_floors = len(des_copy) - 2  # excluding the 2 floor that was added for testing travel time and the
        return length + add_delay + (count_of_floors * Data["DELAY_AT_ARRIVAL"]) * Data["PIXELS_PER_SECOND"]


    def add_destination(self, destination_floor):
        """Add a destination floor to the elevator's queue."""
        self._destinations.append(convert_floor_num_to_y_coordinate(destination_floor))


    def move_elev(self, target_y, screen, timers):
        dest_to_target = abs(self.rect.y - target_y)
        current_time = time.time()
        elapsed_time = current_time - self._last_time

        speed = elapsed_time * Data["PIXELS_PER_SECOND"]
        if elapsed_time > 1:
            speed = 2
        if dest_to_target > 5:

            self.set_elevator_speed(speed)
            if self.rect.y > target_y:
                self.rect.y -= self._speed
            else:
                self.rect.y += self._speed
        else:
            self.set_elevator_speed(Data["SPEED_FINAL"])
            if self.rect.y > target_y:
                self.rect.y -= 1
            else:
                self.rect.y += 1

        self._last_time = time.time()
