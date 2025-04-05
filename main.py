from pygame import *
from keys import keycodes
from time import sleep
import math as mathh
import random

init()
font.init()
mixer.init()
# mixer.music.load('CHANGETHIS.ogg')
# mixer.music.set_volume(0.1)
# mixer.music.play(loops=0)

# CHANGE_sound = mixer.Sound('CHANGETHIS.wav')
# CHANGE_sound.set_volume(0.5)

FONT = 'Fonts/Ubuntu-Bold.ttf'

FPS = 60

scr_info = display.Info()
WIDTH, HEIGHT = scr_info.current_w,  scr_info.current_h

window = display.set_mode((WIDTH,HEIGHT), flags=FULLSCREEN)
display.set_caption("Boring Rhythm Game (BRG)")
clock = time.Clock()

noimg = image.load("Sprite/void.png")

note_img = image.load("Sprite/square.png")
key_active_img = image.load("Sprite/square_outline.png")
key_inactive_img = image.load("Sprite/square_outline_inactive.png")

perfect_img = image.load("Sprite/Ratings/perfect.png")
great_img = image.load("Sprite/Ratings/great.png")
good_img = image.load("Sprite/Ratings/good.png")
meh_img = image.load("Sprite/Ratings/meh.png")
miss_img = image.load("Sprite/Ratings/miss.png")

notes = sprite.Group()
all_sprites = sprite.Group()
all_labels = sprite.Group()

class Label(sprite.Sprite):
    def __init__(self, text, x, y, fontsize=30, color=(255, 255, 255) , font_name=FONT):
        super().__init__()
        self.color = color
        self.font = font.Font(FONT, fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y  = y
        all_labels.add(self)
    
    def set_text(self, new_text, color=(225, 228, 232)):
        self.image = self.font.render(new_text, True, color) 

class BaseSprite(sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y,width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)
                
    # def draw(self, window):
    #     if self.rect.x > 0 - self.rect.width and self.rect.x < WIDTH: window.blit(self.image, self.rect)

class Note(sprite.Sprite):
    def __init__(self, image, x, y, width, height, actualY, keyAttached):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y,width, height)
        self.mask = mask.from_surface(self.image)
        self.actualY = actualY
        self.keyAttached = keyAttached
        notes.add(self)

        def draw(self, window):
            if self.rect.x > 0 - self.rect.width and self.rect.x < WIDTH: window.blit(self.image, self.rect)

    def update(self):
        if self.rect.y > self.keyAttached.rect.y +90 +(scrollSpeed/5 + BPM/64)*scrollSpeed*2:
            score[0] -= score[2]
            # Pop up "Missed!" sprite
        self.rect.x = self.keyAttached.rect.x
        self.rect.y = ((self.actualY * 4000 / BPM * 1.02 / stepsInBeat) + curstep - self.keyAttached.rect.y) * scrollSpeed + songOffset * 100 + globalSongOffset * 100 + scrollSpeed * 800 + self.keyAttached.rect.y

class Key(sprite.Sprite):
    def __init__(self, image, x, y, width, height, keynum):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y,width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

    def update(self):
        keys = key.get_pressed()

        if keys[K_d]:
            
                
    # def draw(self, window):
    #     if self.rect.x > 0 - self.rect.width and self.rect.x < WIDTH: window.blit(self.image, self.rect)

def cap(n, minn, maxn):
    return max(min(maxn, n), minn)

def loadChart(chartName):
    chartSteps = open(f"Maps\{chartName}\chart.txt")
    chartInfo = open(f"Maps\{chartName}\chart_info.txt").readlines()
    
    global song_name
    global song_author
    global song_charter

    global BPM
    global songOffset
    global scrollSpeed
    global stepsInBeat

    global chartLoaded

    song_name = chartInfo[0].replace("\n", "")
    song_author = chartInfo[1].replace("\n", "")
    song_charter = chartInfo[2].replace("\n", "")

    BPM = int(chartInfo[3].replace("\n", ""))
    songOffset = int(chartInfo[4].replace("\n", ""))
    stepsInBeat = int(chartInfo[5].replace("\n", ""))
    scrollSpeed = int(chartInfo[6].replace("\n", ""))

    chartLoaded = True
    localActualY = 0

    for step in chartSteps:
        newStep = step.replace("\n", "")
        localActualY -= 1
        i = 0
        for key in newStep:
            if key == "O":
                score[1] += 1
                score[2] = 1000000 / score[1]
                match i:
                    case 0: notes.add(Note(note_img, k1.rect.x, ((localActualY * 4000 / BPM * 1.02 / stepsInBeat) + curstep - k1.rect.y + songOffset + 1600) , 128, 128, localActualY, k1))
                    case 1: notes.add(Note(note_img, k2.rect.x, ((localActualY * 4000 / BPM * 1.02 / stepsInBeat) + curstep - k2.rect.y + songOffset + 1600) , 128, 128, localActualY, k2))
                    case 2: notes.add(Note(note_img, k3.rect.x, ((localActualY * 4000 / BPM * 1.02 / stepsInBeat) + curstep - k3.rect.y + songOffset + 1600) , 128, 128, localActualY, k3))
                    case 3: notes.add(Note(note_img, k4.rect.x, ((localActualY * 4000 / BPM * 1.02 / stepsInBeat) + curstep - k4.rect.y + songOffset + 1600) , 128, 128, localActualY, k4))
            i += 1

k1 = Key(key_inactive_img, WIDTH /2 -210 -64, HEIGHT - 200, 128, 128, 1)
k2 = Key(key_inactive_img, WIDTH /2 -70 -64, HEIGHT - 200, 128, 128, 2)
k3 = Key(key_inactive_img, WIDTH /2 +70 -64, HEIGHT - 200, 128, 128, 3)
k4 = Key(key_inactive_img, WIDTH /2 +210 -64, HEIGHT - 200, 128, 128, 4)

rating_popup = BaseSprite(noimg, WIDTH /2 - 256, HEIGHT - 350, 512, 128)

ghost_tapping = bool(open("settings.txt").readlines()[2].split(":")[1].replace(" ", "").replace("\n", ""))
globalSongOffset = float(open("settings.txt").readlines()[3].split(":")[1].replace(" ", "").replace("\n", ""))

inputs = [0, 0, 0, 0] #how much each key is held for
score = [0, 0, 0] # current score, note count, how many points do you get for getting a "Perfect!"
ratings = [0, 0, 0, 0, 0] # "Perfect!", "Great!", "Good!", "Meh...", "Miss."

currentSong = None
chartLoaded = False

song_name = None
song_author = None
song_charter = None
song_charter = None

BPM = None
scrollSpeed = None
curstep = 0
songOffset = None
stepsInBeat = None

loadChart("fridaytheme")
run = True
while run:
    window.fill((0, 0, 0))
    curstep += 1
    
    notes.update() 

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False

    all_sprites.draw(window)
    notes.draw(window)
    all_labels.draw(window)
    
    display.update()
    clock.tick(FPS)
