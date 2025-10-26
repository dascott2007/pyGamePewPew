from configuration import *
from weapons import *
from sprites import *
import sys
import pygame
import os




class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert_alpha()

    def get_image(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK) # so the rocks are transparent and you can see the grass behind
        return sprite


class Game:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # passed as a tuple, hense double parathsis
        self.clock = pygame.time.Clock()
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.terrain_spritesheet = Spritesheet(os.path.join(base_path, 'assets/images/terrain/terrain.png'))
        self.player_spritesheet = Spritesheet(os.path.join(base_path, 'assets/images/player/rarthothcooking.png'))
        self.enemy_spritesheet = Spritesheet(os.path.join(base_path, 'assets/images/enemy/goblin.png'))
        self.weapons_spritesheet = Spritesheet(os.path.join(base_path, 'assets/images/Weapons/evolving_swords.png'))
        self.bullet_spritesheet = Spritesheet(os.path.join(base_path, 'assets/images/bullets/morebullets.png'))
        self.running = True
        self.collided = False
        self.enemy_collided = False
        self.block_collided = False
        self.game_over = False
        pygame.font.init()

    def createTileMap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'R':
                    Water(self, j, i)
                if column == 'W':
                    Weapons(self, j, i)

    def create(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.mainPlayer = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.healthbar = pygame.sprite.LayeredUpdates()
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

    def check_game_over(self):
        # Check if player is dead
        if not hasattr(self, 'player') or len(self.mainPlayer) == 0:
            self.game_over = True
            self.running = False

    def show_game_over_screen(self):
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Options text
        restart_text = font_medium.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
        
        exit_text = font_medium.render("Press Q to Quit", True, RED)
        exit_rect = exit_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 80))
        self.screen.blit(exit_text, exit_rect)
        
        pygame.display.update()

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_q:
                    return 'quit'
        return None

    def camera(self):
        if self.enemy_collided == False and self.block_collided == False:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.x += PLAYER_STEPS

            elif pressed[pygame.K_RIGHT]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.x -= PLAYER_STEPS

            elif pressed[pygame.K_UP]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.y += PLAYER_STEPS

            elif pressed[pygame.K_DOWN]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.y -= PLAYER_STEPS

    def main(self):
        while self.running:
            self.events()
            self.check_game_over()
            self.camera()
            self.update()
            self.draw()


pygame.init()

# Main game loop with restart functionality
while True:
    game = Game()
    game.create()
    
    while game.running:
        game.main()
    
    # Show game over screen and handle restart
    if game.game_over:
        game.show_game_over_screen()
        
        while True:
            action = game.handle_game_over_events()
            if action == 'quit':
                pygame.quit()
                sys.exit()
            elif action == 'restart':
                break
            game.clock.tick(FPS)
    else:
        # Normal exit
        break
    
pygame.quit()
sys.exit()
