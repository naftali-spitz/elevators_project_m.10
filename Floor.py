import pygame
import Data


class Floor(pygame.sprite.Sprite):

    def __init__(self, id, image, x):
        super().__init__()

        self.id = id
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (Data.BUILDING_X, Data.INITIAL_FLOOR_Y - id * Data.FLOOR_HEIGHT)
        self.button_center_coordinates = self.rect.center
        self.timer = 0

    def floor_panel(self, test, i=None):
        font = pygame.font.Font(None, 25)
        if i is None:
            if test:
                return font.render(f"{self.id}", True, 'YELLOW')
            else:
                return font.render(f"{self.id}", True, 'BLACK')
        else:
            if test:
                return font.render(f"{i}", True, 'BLACK')
            else:
                return font.render(f"{i}", True, 'YELLOW')

    def update_floor_call(self, min_pixels_to_travel, call_status, screen):
        if min_pixels_to_travel <= 0:
            self.timer = 0
        else:
            self.timer = min_pixels_to_travel / Data.PIXELS_PER_SECOND
        floor_num_text_update = self.floor_panel(call_status)
        screen.blit(floor_num_text_update, (self.rect.centerx - 4, self.rect.centery - 7))
