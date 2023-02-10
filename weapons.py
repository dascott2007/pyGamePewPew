from sprites import *
from configuration import *
import pygame


class Weapons(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.weapons
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.weapons_spritesheet.get_image(447, 353, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animationCounter = 1

    def animate(self):
        animation = [self.game.weapons_spritesheet.get_image(0, 0, self.width, self.height),
                     self.game.weapons_spritesheet.get_image(45, 0, self.width, self.height),
                     self.game.weapons_spritesheet.get_image(0, 0, self.width, self.height),]

        self.image = animation[math.floor(self.animationCounter)]
        self.animationCounter += 0.1
        if self.animationCounter >= 3:
            self.animationCounter = 0

    def update(self):
        self.animate()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.bullet_spritesheet.get_image(129, 152, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = self.game.player.direction

        self.damage = 1

    def move(self):
        if self.direction == 'right':
            self.rect.x += BULLET_STEPS
        if self.direction == 'left':
            self.rect.x -= BULLET_STEPS
        if self.direction == 'up':
            self.rect.y -= BULLET_STEPS
        if self.direction == 'down':
            self.rect.y += BULLET_STEPS

    def collide_block(self):
        collide = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if collide:
            self.kill()

    def collide_enemy(self):
        collide = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if collide:
            collide[0].damage(self.damage)
            self.kill()

    def update(self):
        self.move()
        self.collide_block()
        self.collide_enemy()


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.bullet_spritesheet.get_image(129, 152, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = self.game.player.direction

        self.damage = 1

    def move(self):
        if self.direction == 'right':
            self.rect.x += BULLET_STEPS
        if self.direction == 'left':
            self.rect.x -= BULLET_STEPS
        if self.direction == 'up':
            self.rect.y -= BULLET_STEPS
        if self.direction == 'down':
            self.rect.y += BULLET_STEPS

    def collide_block(self):
        collide = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if collide:
            self.kill()

    def collide_player(self):
        collide = pygame.sprite.spritecollide(self, self.game.mainPlayer, False)
        if collide:
            #collide[0].damage(self.damage) # don't need because we only have one player
            self.game.player.damage(self.damage)
            self.kill()

    def update(self):
        self.move()
        self.collide_block()
        self.collide_player()
