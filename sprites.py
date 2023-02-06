from configuration import *
import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer = BLOCKS_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_image(991,541, self.width, self.height)  # coordinents for the terrain.png file for the rocks. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game=game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_image(447,353, self.width, self.height)  # coordinents for the terrain.png file for the grass. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
