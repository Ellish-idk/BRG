from pygame import *
from time import sleep
import math as mathh
import random

init()
font.init()
mixer.init()

# CHANGE_sound = mixer.Sound('CHANGETHIS.wav')
# CHANGE_sound.set_volume(0.5)

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
        self.rect.y  = y
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
        self.rect.y = ((self.actualY * 4000 / BPM * 0.911 / stepsInBeat) + curstep - self.keyAttached.rect.y) * scrollSpeed + songOffset * 100 + globalSongOffset * 100 + scrollSpeed * 800 + self.keyAttached.rect.y

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
            if closest_note and closest_distance <= 25.0 * scrollSpeed and self.activeFor == 1:
                if offset < -15.0 * scrollSpeed or offset > 15.0 * scrollSpeed:
                    score[0] -= score[2] / 2
                    ratings.append(0)

                    rpp_timer = 0
                    rating_popup.image = miss_img
                    rating_popup.rect.x = WIDTH /2 - 131
                    misses_txt.set_text(f"Misses: {ratings.count(0)}")
                elif abs(offset) > 10.0 * scrollSpeed:
                    score[0] += score[2] / 3
                    ratings.append(0.3)

                    rpp_timer = 0
                    rating_popup.image = meh_img
                    rating_popup.rect.x = WIDTH /2 - 152
                elif abs(offset) > 5.0 * scrollSpeed:
                    score[0] += score[2] / 2
                    ratings.append(0.6)

                    rpp_timer = 0
                    rating_popup.image = good_img
                    rating_popup.rect.x = WIDTH /2 - 149
                elif abs(offset) > 3.5 * scrollSpeed:
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
                hitsound.set_volume(0.2)
                hitsound.play(loops=0)
                score_txt.set_text(f"Score: {mathh.trunc(score[0])}")
                closest_note.kill()
        else:
            self.image = transform.scale(key_inactive_img, self.size)
            self.activeFor = 0
            if closest_note and offset > 250:
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

ghost_tapping = bool(open("settings.txt").readlines()[2].split(":")[1].replace(" ", "").replace("\n", ""))
globalSongOffset = float(open("settings.txt").readlines()[3].split(":")[1].replace(" ", "").replace("\n", ""))
controls = str(open("settings.txt").readlines()[4].split(":")[1].replace(" ", "").replace("\n", ""))

score = [0, 0, 0] # current score, note count, how many points do you get for getting a "Perfect!"
ratings = [] # 1 = "Perfect!", 0.9 = "Great!", 0.6 = "Good!", 0.3 = "Meh...", 0 = "Miss."
accuracy = 100.00

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

startAfter = None
playSong = True
validChart = None

timer = 0
rpp_timer = 0

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
    if validChart:
        curstep += 1

        timer += 1
        rpp_timer += 1

        if rpp_timer > 30:
            rating_popup.image = noimg

        if timer > startAfter and playSong:
            currentSong.set_volume(0.2)
            currentSong.play(loops=0)
            playSong = False
        
        if len(ratings) > 0:
            for i in ratings:
                accuracy = mathh.trunc(((1 * ratings.count(1) + 0.9 * ratings.count(0.9) + 0.6 *  ratings.count(0.6) + 0.3 * ratings.count(0.3) + 0 * ratings.count(0)) / len(ratings)) * 10000) / 100
            accuracy_txt.set_text(f"Accuracy: {accuracy}%")
        else:
            accuracy_txt.set_text(f"Accuracy: 100.00%")


        notes.update() 
        keys.update()

        keys.draw(window)
        notes.draw(window)

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
    all_sprites.draw(window)
    all_labels.draw(window)
    
    display.update()
    clock.tick(FPS)
