import pygame
from sys import exit
from random import randint, choice

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def update(self):
        pass


class Player(GameObject):
    def __init__(self):
        
        super().__init__('graphics/kedi.png', 80, 300)
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        
        self.player_input()
        self.apply_gravity()

class Obstacle(GameObject):
    def __init__(self, type):
        
        if type == 'kus':
            image_path = 'graphics/kus.png'
            y_pos = 210
        elif type == 'kaya':
            image_path = 'graphics/tas.png'
            y_pos = 300
        super().__init__(image_path, randint(900, 1100), y_pos)

    def update(self):
        
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Dila Kurnaz')
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 50) 
game_active = True  
start_time = int(pygame.time.get_ticks() / 1000)
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/background.gif').convert()
ground_surface = pygame.image.load('graphics/ground2.png').convert()

# her 1500 milisaniyede bir kere obstacle ekler.
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['kus', 'kaya', 'kaya', 'kaya', 'kus', 'kaya'])))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
    else:
        
        screen.fill((0, 0, 0))
        
        
        game_over_text = game_font.render("YOU'RE DEAD!", False, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(400, 200))
        screen.blit(game_over_text, game_over_rect)

        
        score_text = game_font.render(f'Final Score: {score}', False, (255, 255, 255))
        score_rect = score_text.get_rect(center=(400, 250))
        screen.blit(score_text, score_rect)

    pygame.display.update()
    clock.tick(60)
