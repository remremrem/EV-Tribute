import pygame.mixer
       
class Sounds:
    def __init__(self):
        #pygame.mixer.pre_init(11025, -16, 2, 256)
        #pygame.init()
        self.menu1 = pygame.mixer.Sound('data/sounds/menu1.wav')
        self.menu1.set_volume(0.6)
        self.menu1.get_buffer()
        self.jump = pygame.mixer.Sound('data/sounds/superbzzt.wav')
        self.jump.get_buffer()
        self.weapon1 = pygame.mixer.Sound('data/sounds/bew1.wav')
        self.weapon1.set_volume(0.4)
        self.weapon1.get_buffer()
        self.weapon2 = pygame.mixer.Sound('data/sounds/ewb1.wav')
        self.weapon2.set_volume(0.4)
        self.weapon2.get_buffer()
        self.toggle1 = pygame.mixer.Sound('data/sounds/menu3.wav')
        self.toggle1.set_volume(0.4)
        self.toggle1.get_buffer()
