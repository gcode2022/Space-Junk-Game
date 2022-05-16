import pygame as pg
from sys import exit
from random import randint, choice


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Graphics/Player/Player_Ship.png').convert_alpha()
        self.image = pg.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect(midbottom=(250, 400))
        self.speed = 3

    def player_input(self, speed):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.rect.x -= speed
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.rect.x += speed
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.rect.y -= speed
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.rect.y += speed

    def player_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 500:
            self.rect.bottom = 500

    def update(self):
        self.player_input(self.speed)
        self.player_boundaries()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, ob_type):
        super().__init__()
        self.speed = randint(1, 10)
        if 'meteor' in ob_type:
            self.image = pg.image.load(f'Graphics/Meteors/{ob_type}.png').convert_alpha()
        self.rect = self.image.get_rect(midtop=(randint(10, 490), -1 * randint(50, 150)))

    def update(self):
        self.rect.y += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.top > 550:
            self.kill()


# Scoring
def display_score():
    current_time = int((pg.time.get_ticks() - start_time) / 100)
    score_surf = font2.render(f'Score: {current_time}', False, "White")
    score_rect = score_surf.get_rect(center=(250, 80))
    screen.blit(score_surf, score_rect)
    return current_time


def sprite_collision():
    if pg.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        explosion_sound.play()
        return False
    else:
        return True


# Initialising Game
pg.init()
screen = pg.display.set_mode((500, 500))
pg.display.set_caption("Space Junk")
clock = pg.time.Clock()
font1 = pg.font.Font("Font/future.ttf", 50)
font2 = pg.font.Font("Font/future_thin.ttf", 25)
game_active = False
start_time = 0
score = 0
bg_music = pg.mixer.Sound('audio/Background_Music.wav')
bg_music.play(loops=-1)
explosion_sound = pg.mixer.Sound('Audio/Explosion.ogg')

background = pg.image.load("Graphics/Background.png").convert()

# Groups
player = pg.sprite.GroupSingle()
player.add(Player())

obstacle_group = pg.sprite.Group()

# Intro Screen
intro_surf = pg.image.load('Graphics/Player/Player_Ship.png').convert_alpha()
intro_logo = pg.transform.rotozoom(intro_surf, 0, 0.75)
intro_logo_rect = intro_logo.get_rect(center=(250, 250))
game_name = font1.render("Space Junk", False, "White")
game_name_rect = game_name.get_rect(center=(250, 150))
start_message = font2.render("Press any key to start...", False, "White")
start_message_rect = start_message.get_rect(center=(250, 350))

# Timer
obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer, 1000)

# Game Loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice([
                    'meteor_1', 'meteor_2', 'meteor_3', 'meteor_4', 'meteor_5', 'meteor_6'
                ])))
        else:
            if event.type == pg.KEYDOWN:
                game_active = True
                start_time = pg.time.get_ticks()

    if game_active:
        screen.blit(background, (0, 0))
        score = display_score()

        # Managing Player
        player.draw(screen)
        player.update()

        # Managing Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = sprite_collision()

    else:
        player.speed = 0
        screen.fill((37, 11, 56))
        screen.blit(game_name, game_name_rect)
        screen.blit(intro_logo, intro_logo_rect)
        score_message = font2.render(f'Your score: {score}', False, "White")
        score_message_rect = score_message.get_rect(center=(250, 350))
        if not score:
            screen.blit(start_message, start_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pg.display.update()
    clock.tick(60)
