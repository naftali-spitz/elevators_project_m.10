import pygame

ELEVATOR_IMAGE = 'resources/elv-small.png'
BRICK_TEXTURE = 'resources/brick-texture.png'
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [180, 180, 180]
FLOOR_POS = []
BUTTON_RADIUS = 20
FLOOR_TRANSIT_TIME = 0.5
ID_N = 0
BUILDING_X = 10


class Floor(pygame.sprite.Sprite):

    def __init__(self, id, image, x):
        super().__init__()

        self.id = id
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 550 - id * 58)
        self.button_center_coordinates = self.rect.center
        self.timer = 0

    def floor_panel(self, test, i=None):
        font = pygame.font.Font(None, 25)
        if i == None:
            if test > 5:
                return font.render(f"{self.id}", True, BLACK)
            else:
                return font.render(f"{self.id}", True, (0, 255, 0))
        else:
            if test > 5:
                return font.render(f"{i}", True, BLACK)
            else:
                return font.render(f"{i}", True, (0, 255, 0))

    def timer(self, floor, time):
        self.time_pending = time
