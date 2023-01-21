
from pygame import *
from random import randint
mixer.init()
font.init()
font2 = font.Font(None, 36)
win = font2.render('COOL BRO!', True, (255, 255, 255))
lose = font2.render('GAME OVER', True, (180, 0, 0))
mixer.music.load('space.ogg')
mixer.music.play()
st = mixer.Sound('fire.ogg')

 
w = 1000
h = 700
fps = 60
score = 0
lost = 0
goal = 10
max_lost = 3

mw = display.set_mode((w, h))
back = transform.scale(image.load('galaxy.jpg'), (w, h))
display.set_caption('шутер игра космос')

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        self.rect = self.image.get_rect()
        self.rect.x =player_x
        self.rect.y = player_y


    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, hp):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.hp = hp
    
    
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < w - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > h:
            self.rect.x = randint(80, w - 80)
            self.rect.y = 0
            lost = lost + 1





class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = direction
    def update(self):
        self.rect.y += self.speed
        if self.direction == 0:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    
        if self.rect.y > h or self.rect.x > w or self.rect.x < 0:
            self.rect.x = randint(80, w - 80)
            self.rect.y = 0
            self.direction = randint(0, 1)
            



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()





ship = Player('rocket.png', 5, h - 100, 80, 100, 10, 5)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, w - 80), -40, 80, 50, randint(1, 5)) 
    monsters.add(monster)


asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid('asteroid.png', randint(80, w - 80), -40, 80, 50, randint(1, 5), randint(0, 1))
    asteroids.add(asteroid)

hp = GameSprite('health.png', randint(80, w-80), randint(80, h-120), 30, 30, 0)


  


bullets = sprite.Group()

finish = False



cec = True
while cec:
    for e in event.get():
        if e.type == QUIT:
            cec = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                st.play()
                ship.fire()


    if not finish:
        mw.blit(back, (0, 0))


        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        mw.blit(text, (10, 20))

        lose_text = font2.render('пропущено:' + str(score), 1, (255, 255, 255))
        mw.blit(lose_text, (10, 50))


        hp_score = font2.render('жизнь:' + str(ship.hp), 1, (255, 255, 255))
        mw.blit(hp_score, (10, 80))

        ship.update()
        hp.reset()
        ship.reset()
        monsters.draw(mw)
        monsters.update()
        bullets.draw(mw)
        bullets.update()
        asteroids.update()
        asteroids.draw(mw)



        collides = sprite.groupcollide(monsters, bullets, True, True)
        for e in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, w - 80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster)


        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            mw.blit(lose, (200, 200))

        if sprite.spritecollide(ship, asteroids, True):
            if hp > 3:
                asteroid = Asteroid('asteroid.png', randint(80, w - 80), -40, 80, 50, randint(1, 5), randint(0, 1))
                asteroids.add(asteroid)
                ship.hp -= 3
            else:
                finish = True
                bm.blit(lose_text, (200, 200))


        if sprite.spritecollide(hp, bullets, True):
            ship.hp + 1
            hp.rect.x = randint(80, w-80)
            hp.rect.y = randint(80, h-120)


        

        if sprite.spritecollide(ship, monsters, True):
            if ship.hp > 1:
                monster = Enemy('ufo.png', randint(80, w - 80), -40, 80, 50, randint(1, 5)) 
                monsters.add(monster)
                ship.hp -= 1
            else:
                finish = True
                mw.blit(lose_text, (200, 200))

        if score >= goal:
            finish = True
            mw.blit(win, (200, 200))    





        clock.tick(fps)
        display.update()

    time.delay(50)
    