import time
import pygame
from collections import deque
from itertools import pairwise

FLOOR_TRANSIT_TIME = 0.5
PIXELS_PER_SECOND = 116
FLOOR_HEIGHT = 58
INITIAL_FLOOR_Y = 550
SPEED_STOP = 0
SPEED_NORMAL = 2
SPEED_FINAL = 1
DELAY_AT_ARRIVAL = 2


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
        self._destination = []
        self._destinations = deque(maxlen=20)
        self._last_destination_time = 0
        self._current_destination_index = 0

    def move_stop_elevator(self, speed):
        """Set the speed of the elevator.
        Arg:
            speed (int): The speed at witch the elevator should move.
        """
        self._speed = speed

    def update(self):
        """Update the elevator's position based on its destinations."""

        if len(self._destinations) == 0:
            return
        current_time = time.time()
        if current_time - self._last_destination_time >= DELAY_AT_ARRIVAL:

            target_y = self._destinations[0]

            if self.rect.y != target_y:
                des_to_target = abs(self.rect.y - target_y)
                if des_to_target > 40:
                    self.move_stop_elevator(SPEED_NORMAL)
                    if self.rect.y > target_y:
                        self.rect.y -= self._speed
                    else:
                        self.rect.y += self._speed
                else:
                    self.move_stop_elevator(SPEED_FINAL)
                    if self.rect.y > target_y:
                        self.rect.y -= 1
                    else:
                        self.rect.y += 1

            else:
                self._destinations.popleft()
                self.move_stop_elevator(SPEED_STOP)

                ding_sound = pygame.mixer.Sound('ding.mp3')
                # ding_sound.play()

                self._last_destination_time = current_time
                self._current_destination_index += 1

                if self._current_destination_index >= len(self._destinations):
                    self._current_destination_index = 0

    def floor_to_y(self, floor):
        """Converts a floor number to the y-coordinate.
        Arg:
            floor (int): The floor number.
        Returns:
            int: The y-coordinate corresponding to the floor.
            """
        return INITIAL_FLOOR_Y - (floor * FLOOR_HEIGHT)

    def total_travel_length(self, destination_floor):
        """Calculate the total travel length to a destination floor.
        Args:
            destination_floor (int): The destination floor number.
        Returns:
            int: The total travel length in pixels.
            """
        destination = Elevator.floor_to_y(0, destination_floor)

        length = 0
        des_copy = list(self._destinations)
        des_copy.insert(0, self.rect.y)
        if destination in des_copy:
            des_copy = des_copy[0:des_copy.index(destination)]
        des_copy.append(destination)

        for [current, next] in pairwise(des_copy):
            length += abs(current - next)

        count_of_floors = len(des_copy) - 2  # excluding the 2 floors that were added for testing

        return length + (count_of_floors * DELAY_AT_ARRIVAL * PIXELS_PER_SECOND)

    def add_destination(self, destination_floor):
        """Add a destination floor to the elevator's queue.
        Args:
            destination_floor (int): The destination floor number to add.
            """
        self._destinations.append(Elevator.floor_to_y(0, destination_floor))
