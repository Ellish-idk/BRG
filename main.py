from pygame import *
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
display.set_caption("CHANGETHIS")
clock = time.Clock()

# CHANGETHIS_img = image.load("CHANGETHIS.png")

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
                
    def draw(self, window):
        window.blit(self.image, self.rect)
        
run = True
while run:
    window.fill((0, 0, 0))

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