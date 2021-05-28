import pygame


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
DISPLAY = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Character(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 100
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.image.fill(WHITE)
        self.radius = 0

    def update(self):
        if self.health <= 0:
            self.kill()



class Enemy(Character):

    def __init__(self):
        super().__init__()
        self.image.fill(RED)
        self.rect.x = 650
        self.rect.y = 400



class Spell(pygame.sprite.Sprite):

    def __init__(self, name, radius, colour, speed, damage, opponent, similar_words=None):
        super().__init__()
        self.name = name
        self.radius = radius
        self.image = pygame.Surface([self.radius, self.radius])
        self.rect = self.image.get_rect()
        self.rect.x = 140
        self.rect.y = 420
        self.image.fill(colour)
        self.colour = colour
        self.speed = speed
        self.damage = damage
        self.opponent = opponent
        self.direction = 'right'
        self.collided = False


        if similar_words == None:
            self.similar_words = []
        else:
            self.similar_words = similar_words


    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        self.collide_check()


    def collide_check(self):
        if self.rect.colliderect(self.opponent.rect):
            self.collided = True
            self.opponent.health -= self.damage
            self.kill()


class Enemy_Spell(Spell):

    def __init__(self, name, radius, colour, speed, damage, opponent):
        super().__init__(name, radius, colour, speed, damage, opponent)
        self.rect.x = 650
        self.rect.y = 425
        self.direction = 'left'





class Explosion(pygame.sprite.Sprite):

    def __init__(self, radius, spell, exploding=False):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface([self.radius, self.radius])
        self.rect = self.image.get_rect()
        self.rect.y = 420
        self.colour = spell.colour
        self.image.fill(spell.colour)
        self.exploding = exploding

        if spell.direction == 'right':
            self.rect.x = 635
        else:
            self.rect.x = 155


    def update(self):

        if self.exploding:
            if self.radius < 60:
                self.radius += 10
                self.rect.x -= 5
                self.rect.y -= 5
            else:
                self.kill()

            pygame.draw.rect(DISPLAY, self.colour, pygame.Rect(self.rect.x, self.rect.y, self.radius, self.radius))

