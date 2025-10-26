from configuration import *
from weapons import *
import pygame
import random
import math


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCKS_LAYER
        # self.groups = self.game.all_sprites, self.game.blocks
        self.groups = super().__init__(game.all_sprites, game.blocks)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.terrain_spritesheet.get_image(642, 608, self.width, self.height)  # coordinents for the terrain.png file for the rocks. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        # self.groups = self.game.all_sprites
        self.groups = super().__init__(game.all_sprites)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_image(447, 353, self.width, self.height)  # coordinents for the terrain.png file for the grass. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        # self.groups = self.game.all_sprites, self.game.water
        self.groups = super().__init__(game.all_sprites, game.water)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_image(579, 160, self.width, self.height)  # coordinents for the terrain.png file for the grass. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animationCounter = 1

    def animation(self):
        animate = [self.game.terrain_spritesheet.get_image(579, 160, self.width, self.height),
                   self.game.terrain_spritesheet.get_image(610, 160, self.width, self.height),
                   self.game.terrain_spritesheet.get_image(640, 160, self.width, self.height),]

        self.image = animate[math.floor(self.animationCounter)]   # basically floor will round down each time
        self.animationCounter += 0.01  # So that the pictures don't transition at 60 FPS.
        if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
            self.animationCounter = 0

    def update(self):
        self.animation()


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.healthbar = Player_Healthbar(game, x, y)
        # self.groups = self.game.all_sprites, self.game.mainPlayer
        self.groups = super().__init__(game.all_sprites, game.mainPlayer)
        
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.animationCounter = 0

        self.image = self.game.player_spritesheet.get_image(21, 16, self.width, self.height)  # coordinents for the terrain.png file for the rocks. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = "right"
        self.swordEquipped = "False"

        self.counter = 0
        self.waitTime = 10
        self.shootState = "shoot"

        self.health = PLAYER_HEALTH

    def move(self):
        pressed = pygame.key.get_pressed()
        Particle(self.game, self.rect.x, self.rect.y)

        if pressed[pygame.K_LEFT]:  # Set dictionary value = 1

            self.x_change = self.x_change - PLAYER_STEPS
            self.direction = 'left'

        elif pressed[pygame.K_RIGHT]:  # Set dictionary value = 1

            self.x_change = self.x_change + PLAYER_STEPS
            self.direction = 'right'

        elif pressed[pygame.K_UP]:

            self.y_change = self.y_change - PLAYER_STEPS
            self.direction = 'up'

        elif pressed[pygame.K_DOWN]:

            self.y_change = self.y_change + PLAYER_STEPS
            self.direction = 'down'

    def update(self):
        self.move()
        self.animation()

        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change

        self.collide_block()
        self.collide_enemy()
        self.collide_weapon()
        self.shoot_sword()
        self.waitAfterShoot()

        self.x_change = 0
        self.y_change = 0

    def animation(self):

        downAnimation = [self.game.player_spritesheet.get_image(85, 15, self.width, self.height),
                         self.game.player_spritesheet.get_image(20, 15, self.width, self.height),
                         self.game.player_spritesheet.get_image(213, 15, self.width, self.height), ]

        leftAnimation = [self.game.player_spritesheet.get_image(211, 145, self.width, self.height),
                         self.game.player_spritesheet.get_image(280, 145, self.width, self.height),
                         self.game.player_spritesheet.get_image(84, 145, self.width, self.height), ]

        rightAnimation = [self.game.player_spritesheet.get_image(211, 209, self.width, self.height),
                          self.game.player_spritesheet.get_image(276, 209, self.width, self.height),
                          self.game.player_spritesheet.get_image(82, 209, self.width, self.height), ]

        upAnimation = [self.game.player_spritesheet.get_image(149, 81, self.width, self.height),
                       self.game.player_spritesheet.get_image(21, 81, self.width, self.height),
                       self.game.player_spritesheet.get_image(278, 81, self.width, self.height), ]

        if self.direction == "down":
            if self.y_change == 0:
                self.image = self.game.player_spritesheet.get_image(20, 15, self.width, self.height)
            else:
                self.image = downAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

        if self.direction == "up":
            if self.y_change == 0:
                self.image = self.game.player_spritesheet.get_image(21, 81, self.width, self.height)
            else:
                self.image = upAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

        if self.direction == "left":
            if self.x_change == 0:
                self.image = self.game.player_spritesheet.get_image(280, 145, self.width, self.height)
            else:
                self.image = leftAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

        if self.direction == "right":
            if self.x_change == 0:
                self.image = self.game.player_spritesheet.get_image(276, 209, self.width, self.height)
            else:
                self.image = rightAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

    def collide_block(self):
        pressed = pygame.key.get_pressed()
        #  Check for collision; False is so the sprite does not disappear
        #  pygame.sprite.collide_rect_ratio(.05)) --> will allow for partial collision so blocks that re 32 x 32
        #  in pixels, but the rock is not that large, it will still allow the player to pass through.
        #  So a slight overlap
        collideBlock = pygame.sprite.spritecollide(self, self.game.blocks, False, pygame.sprite.collide_rect_ratio(.6))
        collideWater = pygame.sprite.spritecollide(self, self.game.water, False, pygame.sprite.collide_rect_ratio(.7))

        # collide will return a true/false
        if collideBlock or collideWater:
            self.game.block_collided = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += PLAYER_STEPS

            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_STEPS

            elif pressed[pygame.K_UP]:
                self.rect.y += PLAYER_STEPS

            elif pressed[pygame.K_DOWN]:
                self.rect.y -= PLAYER_STEPS
        else:
            self.game.block_collided = False

    def collide_enemy(self):
        pressed = pygame.key.get_pressed()
        collide = pygame.sprite.spritecollide(self, self.game.enemies, False, pygame.sprite.collide_rect_ratio(.85))

        if collide:
            self.game.enemy_collided = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += PLAYER_STEPS

            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_STEPS

            elif pressed[pygame.K_UP]:
                self.rect.y += PLAYER_STEPS

            elif pressed[pygame.K_DOWN]:
                self.rect.y -= PLAYER_STEPS
        else:
            self.game.enemy_collided = False

    def collide_weapon(self):
        collide = pygame.sprite.spritecollide(self, self.game.weapons, True)
        if collide:
            self.swordEquipped = True

    def shoot_sword(self):
        pressed = pygame.key.get_pressed()
        if self.shootState == 'shoot':
            if self.swordEquipped == True:
                if pressed[pygame.K_z]:
                    Bullet(self.game, self.rect.x, self.rect.y)
                    self.shootState = "wait"

    def waitAfterShoot(self):
        if self.shootState == "wait":
            self.counter += 1
            if self.counter >= self.waitTime:
                self.counter = 0
                self.shootState = "shoot"

    def damage(self, amount):
        self.health = self.health - amount
        self.healthbar.damage()

        if self.health <= 0:
            self.kill()
            self.healthbar.kill_healthbar()
            self.game.game_over = True
            self.game.running = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.healthbar = Enemy_Healthbar(game, self, x, y)
        # self.groups = self.game.all_sprites, self.game.enemies
        self.groups = super().__init__(game.all_sprites, game.enemies)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.enemy_spritesheet.get_image(17, 3, self.width, self.height)  # coordinents for the terrain.png file for the rocks. found this using paint
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.numberSteps = random.choice([30, 40, 50, 60, 70, 80, 90])
        self.stallSteps = 120
        self.currentSteps = 0

        self.state = 'moving'
        self.animationCounter = 1

        self.health = ENEMY_HEALTH

        self.shootCounter = 0
        self.waitShoot = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90])
        self.shootState = "halt"

    def shoot(self):

        self.shootCounter += 1
        if self.shootCounter >= self.waitShoot:
            self.shootState = "shoot"
            self.shootCounter = 0

    def move(self):
        if self.state == 'moving':
            if self.direction == 'left':
                self.x_change = self.x_change - ENEMY_STEPS
                self.currentSteps += 1

                if self.shootState == "shoot":
                    Enemy_Bullet(self.game, self.rect.x, self.rect.y)
                    self.shootState = "halt"

            elif self.direction == 'right':
                self.x_change = self.x_change + ENEMY_STEPS
                self.currentSteps += 1

                if self.shootState == "shoot":
                    Enemy_Bullet(self.game, self.rect.x, self.rect.y)
                    self.shootState = "halt"

            elif self.direction == 'up':
                self.y_change = self.y_change - ENEMY_STEPS
                self.currentSteps += 1

                if self.shootState == "shoot":
                    Enemy_Bullet(self.game, self.rect.x, self.rect.y)
                    self.shootState = "halt"

            elif self.direction == 'down':
                self.y_change = self.y_change + ENEMY_STEPS
                self.currentSteps += 1

                if self.shootState == "shoot":
                    Enemy_Bullet(self.game, self.rect.x, self.rect.y)
                    self.shootState = "halt"

        elif self.state == 'stalling':
            self.currentSteps += 1
            if self.currentSteps == self.stallSteps:
                self.state = 'moving'
                self.currentSteps = 0
                self.direction = random.choice(['left', 'right', 'up', 'down'])

    def animation(self):

        downAnimation = [self.game.enemy_spritesheet.get_image(277, 1, self.width, self.height),
                         self.game.enemy_spritesheet.get_image(407, 1, self.width, self.height),
                         self.game.enemy_spritesheet.get_image(147, 1, self.width, self.height), ]

        leftAnimation = [self.game.enemy_spritesheet.get_image(282, 200, self.width, self.height),
                         self.game.enemy_spritesheet.get_image(26, 200, self.width, self.height),
                         self.game.enemy_spritesheet.get_image(87, 200, self.width, self.height), ]

        rightAnimation = [self.game.enemy_spritesheet.get_image(10, 70, self.width, self.height),
                          self.game.enemy_spritesheet.get_image(335, 70, self.width, self.height),
                          self.game.enemy_spritesheet.get_image(600, 70, self.width, self.height), ]

        upAnimation = [self.game.enemy_spritesheet.get_image(16, 140, self.width, self.height),
                       self.game.enemy_spritesheet.get_image(404, 140, self.width, self.height),
                       self.game.enemy_spritesheet.get_image(208, 140, self.width, self.height), ]

        if self.direction == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(407, 1, self.width, self.height)
            else:
                self.image = downAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

        if self.direction == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(404, 140, self.width, self.height)
            else:
                self.image = upAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

        if self.direction == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(26, 200, self.width, self.height)
            else:
                self.image = leftAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

        if self.direction == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_image(335, 70, self.width, self.height)
            else:
                self.image = rightAnimation[math.floor(self.animationCounter)]   # basically floor will round down each time
                self.animationCounter += 0.2  # So that the pictures don't transition at 60 FPS.
                if self.animationCounter >= 3:  # once you have 3 frames, go back to 0
                    self.animationCounter = 0

    def update(self):
        self.move()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change

        self.x_change = 0
        self.y_change = 0
        if self.currentSteps == self.numberSteps:
            if self.state != 'stalling':
                self.currentSteps = 0
            self.numberSteps = random.choice([30, 40, 50, 60, 70, 80, 90])
            self.state = 'stalling'
        self.collide_block()
        self.collide_player()
        self.shoot()

    def collide_block(self):
        collideBlock = pygame.sprite.spritecollide(self, self.game.blocks, False)
        collideWater = pygame.sprite.spritecollide(self, self.game.water, False)
        if collideBlock or collideWater:
            if self.direction == 'left':
                self.rect.x += PLAYER_STEPS
                self.direction = 'right'

            elif self.direction == 'right':
                self.rect.x -= PLAYER_STEPS
                self.direction = 'left'

            elif self.direction == 'up':
                self.rect.y += PLAYER_STEPS
                self.direction = 'down'

            elif self.direction == 'down':
                self.rect.y -= PLAYER_STEPS
                self.direction = 'up'

    def collide_player(self):
        collide = pygame.sprite.spritecollide(self, self.game.mainPlayer, True)
        if collide:
            self.game.game_over = True
            self.game.running = False

    def damage(self, amount):
        self.health = self.health - amount
        self.healthbar.damage(ENEMY_HEALTH, self.health)

        if self.health <= 0:
            self.kill()
            self.healthbar.kill()


class Player_Healthbar(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = HEALTH_LAYER
        # self.groups = self.game.all_sprites, self.game.healthbar
        self.groups = super().__init__(game.all_sprites, game.healthbar)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = 40
        self.height = 5

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - TILESIZE/2

    def move(self):
        self.rect.x = self.game.player.rect.x  # follows above the player's head
        self.rect.y = self.game.player.rect.y - TILESIZE/2

    def kill_healthbar(self):
        self.kill()


    def damage(self):
        self.image.fill(RED)
        width = self.rect.width * self.game.player.health / PLAYER_HEALTH
        pygame.draw.rect(self.image, GREEN, (0, 0, width, self.height), 0)

    def update(self):
        self.move()


class Enemy_Healthbar(pygame.sprite.Sprite):
    def __init__(self, game, enemy, x, y):
        self.enemy = enemy
        self.game = game
        self._layer = HEALTH_LAYER
        # self.groups = self.game.all_sprites, self.game.healthbar
        self.groups = super().__init__(game.all_sprites, game.healthbar)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = 40
        self.height = 5

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - TILESIZE/2

    def move(self):
        self.rect.x = self.enemy.rect.x  # follows above the player's head
        self.rect.y = self.enemy.rect.y - TILESIZE / 2

    def damage(self, totalHealth, health):
        self.image.fill(RED)
        width = self.rect.width * health/totalHealth

        pygame.draw.rect(self.image, GREEN, (0, 0, width, self.height), 0)

    # def kill_bar(self):   # Removed the kill bar because it will always kill the bar. It works without this method
    #     self.kill()

    def update(self):
        self.move()
        # self.kill_bar() # Removed the kill bar because it will always kill the bar. It works without this method


class Particle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = HEALTH_LAYER
        self.game = game
        # self.groups = self.game.all_sprites
        self.groups = super().__init__(game.all_sprites)
        # pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x + random.choice([-4, -3, -1, 0, 1, 5, 10, 20])  # create random particals from player
        self.rect.y = y + TILESIZE  # so all particles start below the feed of the player

        self.lifetime = 6
        self.counter = 0

    def move(self):
        self.rect.y += 1  # to give the illusion of an aura
        self.counter += 1

        if self.counter == self.lifetime:  # so the particles are removed from memory.Otherwise, it's a resource issue
            self.counter = 0
            self.kill()

    def update(self):
        self.move()






