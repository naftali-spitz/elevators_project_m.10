import json
import pygame

# import Data

with open('Data.json', 'r') as file:
    Data = json.load(file)


class Floor(pygame.sprite.Sprite):

    def __init__(self, id, image, x):
        super().__init__()

        self._id = id
        self._image = image
        self._rect = self._image.get_rect()
        self._rect.topleft = (Data["BUILDING_X"], Data["INITIAL_FLOOR_Y"] - id * Data["FLOOR_HEIGHT"])
        self._button_center_coordinates = self._rect.center
        self._timer = 0

    def floor_panel(self, test, i=None):
        font = pygame.font.Font(None, 25)
        if i is None:
            if test:
                return font.render(f"{self._id}", True, 'YELLOW')
            else:
                return font.render(f"{self._id}", True, 'BLACK')
        else:
            if test:
                return font.render(f"{i}", True, 'BLACK')
            else:
                return font.render(f"{i}", True, 'YELLOW')

    def update_floor_call(self, min_pixels_to_travel, call_status, screen):
        # if min_pixels_to_travel <= 0:
        #     self._timer = 0
        # else:
        self._timer = min_pixels_to_travel / Data["PIXELS_PER_SECOND"]
        floor_num_text_update = self.floor_panel(call_status)
        screen.blit(floor_num_text_update, (self._rect.centerx - 4, self._rect.centery - 7))

    def get_id(self):
        return self._id

    def get_rect(self):
        return self._rect

    def get_timer(self):
        return self._timer

    def update_timer(self, time):
        self._timer -= time
