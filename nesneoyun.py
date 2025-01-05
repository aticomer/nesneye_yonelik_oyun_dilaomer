import pygame
from sys import exit
from random import randint, choice

# Ana oyun objesi için temel sınıf
class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        # Görseli yükler ve pozisyonunu ayarlar
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self):
        pass  # Alt sınıflar için üzerine yazılabilir bir metod

# Oyuncu karakteri sınıfı
class Player(GameObject):
    def __init__(self):
        # Oyuncu görseli ve başlangıç pozisyonu
        super().__init__('graphics/kedi.png', 80, 300)
        self.gravity = 0  # Yerçekimi etkisi

    # Oyuncunun tuş girdilerini kontrol eder
    def player_input(self):
        keys = pygame.key.get_pressed()
        # Boşluk tuşuna basıldığında zıplama
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    # Yerçekimi etkisini uygular
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        # Oyuncunun yere düşmesini engeller
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    # Oyuncu güncelleme fonksiyonu
    def update(self):
        self.player_input()
        self.apply_gravity()

# Engel sınıfı
class Obstacle(GameObject):
    def __init__(self, type):
        # Engelin türüne göre görsel ve pozisyon ayarları
        if type == 'kus':
            image_path = 'graphics/kus.png'
            y_pos = 210
        elif type == 'kaya':
            image_path = 'graphics/tas.png'
            y_pos = 300
        super().__init__(image_path, randint(900, 1100), y_pos)

    # Engelin hareketini sağlar ve ekrandan çıktıysa yok eder
    def update(self):
        self.rect.x -= 6  # Sola doğru hareket
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:  # Ekrandan çıktıysa
            self.kill()  # Obje yok edilir

# Skor ekranını günceller

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)  # Skor ekranına yazdırılır
    return current_time

# Oyuncu ve engel çarpışmasını kontrol eder
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()  # Çarpışma durumunda engeller temizlenir
        return False  # Oyun sona erer
    else:
        return True

# Pygame modülünü başlat
pygame.init()
screen = pygame.display.set_mode((800, 400))  # Ekran boyutları
pygame.display.set_caption('Dila Kurnaz')  # Pencere başlığı
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 50)  # Yazı tipi

game_active = True  # Oyun durumu
start_time = int(pygame.time.get_ticks() / 1000)  # Oyun başlangıç zamanı
score = 0  # Skor başlangıç değeri

# Oyuncu objesi oluşturulur
player = pygame.sprite.GroupSingle()
player.add(Player())

# Engel grubu oluşturulur
obstacle_group = pygame.sprite.Group()

# Arkaplan ve zemin görselleri yüklenir
sky_surface = pygame.image.load('graphics/background.gif').convert()
ground_surface = pygame.image.load('graphics/ground2.png').convert()

# Engel oluşturma zamanlayıcısı
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)  # 1500 milisaniyede bir çalışır

# Oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Çıkış isteği
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                # Rastgele engel ekler
                obstacle_group.add(Obstacle(choice(['kus', 'kaya', 'kaya', 'kaya', 'kus', 'kaya'])))

    if game_active:
        # Arkaplan ve zemin çizimi
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Skor güncelleme ve gösterme
        score = display_score()

        # Oyuncu çizimi ve güncellenmesi
        player.draw(screen)
        player.update()

        # Engellerin çizimi ve güncellenmesi
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Çarpışma kontrolü
        game_active = collision_sprite()
    else:
        # Oyun bitti ekranı
        screen.fill((0, 0, 0))

        # "Oyun bitti" yazısı
        game_over_text = game_font.render("YOU'RE DEAD!", False, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(400, 200))
        screen.blit(game_over_text, game_over_rect)

        # Final skorunun gösterimi
        score_text = game_font.render(f'Final Score: {score}', False, (255, 255, 255))
        score_rect = score_text.get_rect(center=(400, 250))
        screen.blit(score_text, score_rect)

    pygame.display.update()  # Ekranı günceller
    clock.tick(60)  # FPS (Saniyedeki kare sayısı)
