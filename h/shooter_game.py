from pygame import *
from random import *
SpaceY = 0
finish = False
bullet_amount = 10
SpaceY1 = -450
game = True
FPS = 60
count = 0
lose_count = 0
font.init()
font1 = font.Font(None, 50)
fontWin = font.Font(None, 60)  
mixer.init()
fire_s = mixer.Sound('fire.ogg')
window = display.set_mode((700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, image_x, image_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (image_x, image_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        else:
            self.rect.y += self.speed

            

bullet_group = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 640:
            self.rect.x += self.speed   
    def fire(self):
        bullet_group.add(Bullet('bullet.png', self.rect.x + 10, self.rect.y + 10, -10, 30, 30))

class Enemy(GameSprite):
    def update(self):
        global lose_count     
        if self.rect.y > 500:
            lose_count += 1
            self.rect.y = randint(0, 50)
            self.rect.x = randint(10, 570)
        else:
            self.rect.y += self.speed

enemy_group = sprite.Group()
for i in range(5):
    enemy_group.add(Enemy('ufo.png', randint(0, 700), 10, randint(1, 2), 70, 70))


clock = time.Clock()

mixer.music.load('space.ogg')
display.set_caption('game')
music = mixer.Sound('space.ogg')
hero = Player(('rocket.png'), 350, 350, 12, 50, 50)
background = transform.scale(image.load('galaxy.jpg'), (700,450))
background1 = transform.scale(image.load('galaxy.jpg'), (700,450))
while game == True:
        clock.tick(FPS)
        text = font1.render(f'Очки: {count}  Пропущено: {lose_count}', True, (100, 200, 100))
        mixer.Sound.play(music)
        window.blit((background), (0,SpaceY))
        window.blit((background1), (0, SpaceY1))
        window.blit((text), (30, 30))
        colision = sprite.groupcollide(enemy_group, bullet_group, True, True)
        for _ in colision:
            enemy = Enemy('ufo.png', randint(0, 700), 10, randint(2, 5), 70, 70)
            enemy_group.add(enemy)
            count += 1
            if count == 100:
                game = False
            if lose_count == 30:
                game = False
        hero.reset()
        enemy_group.update()
        enemy_group.draw(window)
        hero.update()
        bullet_group.update()
        bullet_group.draw(window)
        display.update()   
        SpaceY += 2
        SpaceY1 += 2
        if SpaceY1 == 0:
            SpaceY1  = -450
            SpaceY = 0
        events = event.get()
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    hero.fire()
                    fire_s.play()
            if e.type == QUIT:
                game = False
        else:
            text_win = fontWin.render('ВЫ ПОБЕДИЛИ', True, (0,255,0))