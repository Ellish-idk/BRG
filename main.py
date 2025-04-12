from pygame import *
from time import sleep
import math as mathh
import random

init()
font.init()
mixer.init()

FONT = 'Fonts/Ubuntu-Bold.ttf'

FPS = 60

scr_info = display.Info()
WIDTH, HEIGHT = scr_info.current_w,  scr_info.current_h

window = display.set_mode((WIDTH,HEIGHT), flags=FULLSCREEN)
display.set_caption("Boring Rhythm Game (BRG)")
clock = time.Clock()

hitsound = mixer.Sound("Sounds/hitsound.ogg")

noimg = image.load("Sprite/void.png")

note_img = image.load("Sprite/square.png")
key_active_img = image.load("Sprite/square_outline.png")
key_inactive_img = image.load("Sprite/square_outline_inactive.png")

perfect_img = image.load("Sprite/Ratings/perfect.png")
great_img = image.load("Sprite/Ratings/great.png")
good_img = image.load("Sprite/Ratings/good.png")
meh_img = image.load("Sprite/Ratings/meh.png")
miss_img = image.load("Sprite/Ratings/miss.png")

rank_SP_img = image.load("Sprite/Ranks/SP.png")
rank_S_img = image.load("Sprite/Ranks/S.png")
rank_A_img = image.load("Sprite/Ranks/A.png")
rank_B_img = image.load("Sprite/Ranks/B.png")
rank_C_img = image.load("Sprite/Ranks/C.png")
rank_D_img = image.load("Sprite/Ranks/D.png")
rank_F_img = image.load("Sprite/Ranks/F.png")
rank_0_img = image.load("Sprite/Ranks/0.png")

notes = sprite.Group()
keys = sprite.Group()
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
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text, color=(255, 255, 255)):
        self.image = self.font.render(new_text, True, color) 

class BaseSprite(sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y,width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Note(sprite.Sprite):
    def __init__(self, image, x, y, width, height, actualY, keyAttached):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.mask = mask.from_surface(self.image)
        self.actualY = actualY
        self.keyAttached = keyAttached
        notes.add(self)

    def update(self):
        # Оновлення позиції ноти по Y

        self.rect.x = self.keyAttached.rect.x
        self.rect.y = (((self.actualY * 4000 / BPM * 0.8834 / stepsInBeat) + curstep) * scrollSpeed + (songOffset + globalSongOffset) * 100 + scrollSpeed * 800) + self.keyAttached.rect.centery - (869 * scrollSpeed) # Мене бісить ця строчка
        # BPM * 0.911

class Key(sprite.Sprite):
    def __init__(self, image, x, y, width, height, keycode):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.mask = mask.from_surface(self.image)
        self.activeFor = 0
        self.size = (width, height)
        self.keycode = keycode
        keys.add(self)

    def update(self):
        keys_pressed = key.get_pressed()
        global rpp_timer
        global rating_popup

        # Знаходимо найближчу ноту що прив’язана до цієї клавіші
        closest_note = None
        closest_distance = 10000
        for note in notes:
            if note.keyAttached == self:
                distance = abs(note.rect.centery - self.rect.centery)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_note = note
                    offset = closest_note.rect.centery - self.rect.centery

        if keys_pressed[key.key_code(self.keycode)]:
            self.image = transform.scale(key_active_img, self.size)
            self.activeFor += 1

            # Якщо така нота знайдена і вона достатньо близько — обробляємо її
            if closest_note and closest_distance <= 15.0 * scrollSpeed and self.activeFor == 1:
                if offset < -10 * scrollSpeed or offset > 10 * scrollSpeed:
                    score[0] -= score[2] / 2
                    ratings.append(0)

                    rpp_timer = 0
                    rating_popup.image = miss_img
                    rating_popup.rect.x = WIDTH /2 - 131
                    misses_txt.set_text(f"Misses: {ratings.count(0)}")
                elif abs(offset) > 5 * scrollSpeed:
                    score[0] += score[2] / 3
                    ratings.append(0.3)

                    rpp_timer = 0
                    rating_popup.image = meh_img
                    rating_popup.rect.x = WIDTH /2 - 152
                elif abs(offset) > 3.5 * scrollSpeed:
                    score[0] += score[2] / 2
                    ratings.append(0.6)

                    rpp_timer = 0
                    rating_popup.image = good_img
                    rating_popup.rect.x = WIDTH /2 - 149
                elif abs(offset) > 2 * scrollSpeed:
                    score[0] += score[2] / 1.5
                    ratings.append(0.9)

                    rpp_timer = 0
                    rating_popup.image = great_img
                    rating_popup.rect.x = WIDTH /2 - 160
                else:
                    score[0] += score[2]
                    ratings.append(1)
                    
                    rpp_timer = 0
                    rating_popup.image = perfect_img
                    rating_popup.rect.x = WIDTH /2 - 256
                hitsound.set_volume(hitsoundVolume)
                hitsound.play(loops=0)
                score_txt.set_text(f"Score: {mathh.trunc(score[0])}")
                closest_note.kill()
        else:
            self.image = transform.scale(key_inactive_img, self.size)
            self.activeFor = 0
            if closest_note and offset > 9.0 * scrollSpeed:
                score[0] -= score[2] / 2
                ratings.append(0)

                rpp_timer = 0
                rating_popup.image = miss_img
                rating_popup.rect.x = WIDTH /2 - 131
                
                score_txt.set_text(f"Score: {mathh.trunc(score[0])}")
                misses_txt.set_text(f"Misses: {ratings.count(0)}")
                closest_note.kill()

def loadChart(chartName):
    chartSteps = open(f"Maps\{chartName}\chart.txt")
    chartInfo = open(f"Maps\{chartName}\chart_info.txt").readlines()

    global currentSong
    global currentSongName
    global song_name
    global song_author
    global song_charter

    global BPM
    global songOffset
    global scrollSpeed
    global stepsInBeat
    global validChart

    global startAfter
    global chartLoaded

    song_name = chartInfo[0].split(":")[1].replace("\n", "")
    song_author = chartInfo[1].split(":")[1].replace("\n", "")
    song_charter = chartInfo[2].split(":")[1].replace("\n", "")

    BPM = int(chartInfo[3].split(":")[1].replace("\n", ""))
    songOffset = int(chartInfo[4].split(":")[1].replace("\n", ""))
    stepsInBeat = int(chartInfo[5].split(":")[1].replace("\n", ""))
    scrollSpeed = int(chartInfo[6].split(":")[1].replace("\n", ""))
    startAfter = int(chartInfo[7].split(":")[1].replace("\n", ""))

    currentSong = mixer.Sound(f"Maps/{chartName}/Song.ogg")
    currentSongName = chartName
    chartLoaded = True
    localActualY = 0

    validChart = scrollSpeed > 0 and stepsInBeat > 0 and BPM > 0 and startAfter >= 0

    if validChart:
        for step in chartSteps:
            newStep = step.replace("\n", "")
            localActualY -= 1
            i = 0
            for key in newStep:
                if key == "O":
                    score[1] += 1
                    score[2] = 1000000 / mathh.ceil(score[1])
                    match i:
                        case 0: notes.add(Note(note_img, k1.rect.x, -500, 128, 128, localActualY, k1))
                        case 1: notes.add(Note(note_img, k2.rect.x, -500, 128, 128, localActualY, k2))
                        case 2: notes.add(Note(note_img, k3.rect.x, -500, 128, 128, localActualY, k3))
                        case 3: notes.add(Note(note_img, k4.rect.x, -500, 128, 128, localActualY, k4))
                i += 1
rating_popup = BaseSprite(noimg, WIDTH /2 - 256, HEIGHT - 350, 512, 128)
rank_sprite = BaseSprite(noimg, 200, 200, 1, 1)

globalSongOffset = float(open("settings.txt").readlines()[2].split(":")[1].replace(" ", "").replace("\n", ""))
controls = str(open("settings.txt").readlines()[3].split(":")[1].replace(" ", "").replace("\n", ""))
musicVolume = int(open("settings.txt").readlines()[4].split(":")[1].replace(" ", "").replace("\n", "")) / 100
hitsoundVolume = int(open("settings.txt").readlines()[5].split(":")[1].replace(" ", "").replace("\n", "")) / 100

score = [0, 0, 0] # current score, note count, how many points do you get for getting a "Perfect!"
ratings = [] # 1 = "Perfect!", 0.9 = "Great!", 0.6 = "Good!", 0.3 = "Meh...", 0 = "Miss."
accuracy = 100.00

currentSong = None
currentSongName = None
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

startAfter = None
playSong = True
validChart = None

dt = 0
timer = 0
rpp_timer = 0
fadeOutVol = 1

k1 = Key(key_inactive_img, WIDTH /2 -210 -64, HEIGHT - 200, 128, 128, controls[0])
k2 = Key(key_inactive_img, WIDTH /2 -70 -64, HEIGHT - 200, 128, 128, controls[1])
k3 = Key(key_inactive_img, WIDTH /2 +70 -64, HEIGHT - 200, 128, 128, controls[2])
k4 = Key(key_inactive_img, WIDTH /2 +210 -64, HEIGHT - 200, 128, 128, controls[3])

run = True
loadChart("fridaytheme-ex")

if not validChart:
    invalidChart_txt = Label("Invalid chart: make sure scroll speed, steps in beat, BPM and start song after are above 0.", 20, HEIGHT - 40, 20)
    k1.kill()
    k2.kill()
    k3.kill()
    k4.kill()
else:
    score_txt = Label(f"Score: 0", 20, 20, 50)
    accuracy_txt = Label(f"Accuracy: 100.00%", 20, 70, 50)
    misses_txt = Label(f"Misses: 0", 20, 120, 50)

while run:
    window.fill((0, 0, 0))

    if mathh.trunc(curstep * (60 / BPM)/(48.8/stepsInBeat/2)) <= len(open(f"Maps\{currentSongName}\chart.txt").readlines()) + 3 * stepsInBeat:
        rank_sprite.image = noimg
        if validChart:
            score_txt.rect.topleft = (20, 20)
            accuracy_txt.rect.topleft = (20, 70)
            misses_txt.rect.topleft = (20, 120)

            curstep += dt/0.017

            timer += dt/0.017
            rpp_timer += dt/0.017

            if rpp_timer > 30:
                rating_popup.image = noimg

            if timer > startAfter and playSong:
                currentSong.set_volume(musicVolume)
                currentSong.play(loops=0)
                playSong = False
            
            if len(ratings) > 0:
                for i in ratings:
                    accuracy = mathh.trunc(((1 * ratings.count(1) + 0.9 * ratings.count(0.9) + 0.6 *  ratings.count(0.6) + 0.3 * ratings.count(0.3) + 0 * ratings.count(0)) / len(ratings)) * 10000) / 100
                accuracy_txt.set_text(f"Accuracy: {accuracy}%")
                # accuracy_txt.set_text(f"Current frame: {curstep}") #
            else:
                accuracy_txt.set_text(f"Accuracy: 100.00%")

            # модчарт
            if currentSongName == "fridaytheme-ex":
                if curstep < 2528:
                    k1.rect.y = HEIGHT - 200 + (mathh.sin(curstep/80 +0) * 25)
                    k2.rect.y = HEIGHT - 200 + (mathh.sin(curstep/80 +1) * 25)
                    k3.rect.y = HEIGHT - 200 + (mathh.sin(curstep/80 +2) * 25)
                    k4.rect.y = HEIGHT - 200 + (mathh.sin(curstep/80 +3) * 25)
                else:
                    k1.rect.y = HEIGHT - 200 + (mathh.sin(curstep/7 +0) * 15)
                    k2.rect.y = HEIGHT - 200 + (mathh.sin(curstep/7 +1) * 15)
                    k3.rect.y = HEIGHT - 200 + (mathh.sin(curstep/7 +2) * 15)
                    k4.rect.y = HEIGHT - 200 + (mathh.sin(curstep/7 +3) * 15)

                    k1.rect.centerx = WIDTH /2 -210 + (mathh.cos(curstep/10 +0) * 25)
                    k2.rect.centerx = WIDTH /2 -70 + (mathh.cos(curstep/10 +1) * 25)
                    k3.rect.centerx = WIDTH /2 +70 + (mathh.cos(curstep/10 +2) * 25)
                    k4.rect.centerx = WIDTH /2 +210 + (mathh.cos(curstep/10 +3) * 25)

            notes.update() 
            keys.update()

            keys.draw(window)
            notes.draw(window)
    else:
        rating_popup.image = noimg
        if accuracy == 100: rank_sprite.image = rank_SP_img
        elif accuracy >= 95: rank_sprite.image = rank_S_img
        elif accuracy >= 90: rank_sprite.image = rank_A_img
        elif accuracy >= 85: rank_sprite.image = rank_B_img
        elif accuracy >= 75: rank_sprite.image = rank_C_img
        elif accuracy >= 65: rank_sprite.image = rank_D_img
        elif accuracy >= 1: rank_sprite.image = rank_F_img
        else: rank_sprite.image = rank_0_img

        score_txt.rect.topleft = (200, 480)
        accuracy_txt.rect.topleft = (200, 550)
        misses_txt.rect.topleft = (200, 620)

        if fadeOutVol > 0:
            fadeOutVol -= 0.005
            currentSong.set_volume(fadeOutVol * musicVolume)
        else:
            currentSong.stop()

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
    all_sprites.draw(window)
    all_labels.draw(window)
    
    display.update()
    dt = clock.tick(FPS)/1000
