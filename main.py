import pygame
import random
from character import Character, Enemy, Spell, Enemy_Spell, Explosion
import pyaudio
import speech_recognition as sr
import gtts
from playsound import playsound


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Please start speaking...')
        audio = r.record(source, duration=3)
        try:
            audio = r.recognize_google(audio)
            print(audio)
            return audio
        except:
            print('Google Speech Recognition did not understand audio')
            return ''


def speak(response):

    filename = random.randint(0, 10000)
    text = gtts.gTTS(response)
    text.save('{}.mp3'.format(filename))
    playsound('{}.mp3'.format(filename))


pygame.init()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

DISPLAY = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
FPSCLOCK = pygame.time.Clock()
#pygame.display.set_caption('Show Text')

GREEN = (0, 255, 0)
LIME = (136, 240, 136)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 178, 102)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRASS = (61, 99, 58)    #(0, 153, 76) #(0, 204, 102)
SKY = (41, 41, 59)  #(134, 166, 239) #(134, 239, 239)


font = pygame.font.Font('freesansbold.ttf', 15)

     # pygame things


sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
harry_potter = Character()
sprites.add(harry_potter)
characters.add(harry_potter)
voldemort = Enemy()
sprites.add(voldemort)
characters.add(harry_potter)


expelliarmus = Spell('expelliarmus', 10, RED, 10, 30, voldemort, ['Thomas'])
avada_kedavra = Spell('avada kedavra', 7, GREEN, 15, 40, voldemort, ['avada', 'kedavra', 'abra', 'kadabra', 'Avada', 'Kedavra'])
wingardium_leviosa = Spell('wingardium leviosa', 12, WHITE, 10, 5, voldemort, ['wingardium', 'Leviosa'])
expecto_patronum = Spell('expecto patronum', 10, CYAN, 12, 20, voldemort, ['expecto', 'patronum'])
lumos = Spell('lumos', 15, WHITE, 15, 1, voldemort)
sectumsempra = Spell('sectumsempra', 10, LIME, 14, 40, voldemort)
stupefy = Spell('stupefy', 8, ORANGE, 14, 40, voldemort)

all_spells = [expelliarmus, avada_kedavra, wingardium_leviosa, expecto_patronum, lumos, sectumsempra, stupefy]

spells = pygame.sprite.Group()
my_spells = pygame.sprite.Group()     # spells and characters


responses = ['ow', 'ow', 'ow', 'ow', 'ouch']

move = False
spell = None
exploding = 0
my_turn = 1
wait = 20
fired = False
done = False

stars = []
for i in range(26):
    stars.append([random.randint(1, WINDOWWIDTH), random.randint(1, 450)])







while not done:

    DISPLAY.fill(SKY)
    pygame.draw.rect(DISPLAY, GRASS, pygame.Rect(0, 450, 800, 150))
    pygame.draw.circle(DISPLAY, WHITE, [660, 90], 50)  # moon
    pygame.draw.circle(DISPLAY, SKY, [635, 90], 50)
    for i in range(26):
        pygame.draw.circle(DISPLAY, WHITE, stars[i], 1)  # stars
    pygame.draw.rect(DISPLAY, WHITE, pygame.Rect(harry_potter.rect.x, harry_potter.rect.y + 75, harry_potter.health * 2, 10))   # health bar
    pygame.draw.rect(DISPLAY, RED, pygame.Rect(voldemort.rect.x + 50 - (voldemort.health * 2), voldemort.rect.y + 75, voldemort.health * 2, 10))

    try:
        DISPLAY.blit(text, textRect)
    except:
        pass

    # background

    audio = ''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN and my_turn:
            if event.key == pygame.K_SPACE:
                audio = listen()    # listens for a spell when space is pressed
                #audio = 'avada kedavra'



    if my_turn == 1:    # users turn
        for sp in all_spells:
            if sp.name in audio or audio in sp.similar_words:   # creates spell if its in the audio
                spell = Spell(sp.name, sp.radius, sp.colour, sp.speed, sp.damage, voldemort)
                sprites.add(spell)
                my_spells.add(spell)
                if spell.rect.x < WINDOWWIDTH and spell.rect.x > 0:
                    move = True
                else:
                    spell.kill()
        fired = False


    else:

        if not fired:

            spell = random.choice(all_spells)
            spell = Enemy_Spell(spell.name, spell.radius, spell.colour, spell.speed, spell.damage, harry_potter)
            sprites.add(spell)
            my_spells.add(spell)
            if spell.rect.x < WINDOWWIDTH and spell.rect.x > 0:
                move = True
            else:
                spell.kill()
            fired = True

            text = font.render(spell.name, True, WHITE, SKY)
            textRect = text.get_rect()
            textRect.center = (675, 380)
            DISPLAY.blit(text, textRect)
            speak(spell.name)



    if move:
        my_spells.update()      # moves all the spells forward/backward


    if spell:
        if spell.collided:
            speak(random.choice(responses))     # character responds if hit
            my_turn *= -1     # switches turns
            exploding = 5
            explosion = Explosion(10, spell, True)
            spell.collided = False


    if voldemort.health <= 0:
        voldemort.kill()
        done = True
    if harry_potter.health <= 0:
        harry_potter.kill()
        done = True

    sprites.draw(DISPLAY)

    if exploding:   # continues exploding for 5 loops
        explosion.update()
        exploding -= 1

    print('turn:', my_turn)
    print('fired =', fired)


    pygame.display.update()
    FPSCLOCK.tick(30)