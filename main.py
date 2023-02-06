from configuration import *
import sys
import pygame
from sprites import *


class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()

    def get_image(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        
        return sprite


class Game:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # passed as a tuple, hense double parathsis #TODO remove hard code variable s/b from configuration
        self.clock = pygame.time.Clock()
        self.terrain_spritsheet = Spritesheet('/Users/damaris/Library/Mobile Documents/com~apple~CloudDocs/GitHub/pyGamePractice/assets/images/terrain/terrain.png')
        self.running = True

    def createTileMap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)


    def create(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.createTileMap()

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()


    def main(self):
        while self.running:
            self.event()
            self.update()
            self.draw()


game = Game()
game.create()

while game.running:
    game.main()
    
pygame.quit()
sys.exit
