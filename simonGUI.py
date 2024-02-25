import pygame
from pygame.mixer import Sound
from random import choice
import os
import sys
from button import Button





TITLE = 'Simon Game!'
NUMBER_OF_BLINKS = 4 #The number of time the leds blink when the payer loses
INIT_STARTUP_FRAMEBUFFER = 200 #The number of frames the game runs before starting 
FPS = 100 # The frames per second the game is run at
SCREEN_SIZE = (720, 540)
class Simon:
    
    
    def __init__(self) -> None:
        self.sequence: list[Button] = [] 
        self.sequence_index = 0
        self.running = True
        self.is_playback = True
        self.counter = 200
        self.lost = False
        self.blink_count = NUMBER_OF_BLINKS
        pygame.init()
        
        self.buttons = [
            Button(x=100, y=200, x_size=100, y_size=100,
                   image_file_on=os.path.join('images', 'red_button_on.png'),
                   image_file_off=os.path.join('images', 'red_button_off.png'),
                   sound_file=os.path.join('Sounds', 'one.wav'),
                   color='red'),

            Button(x=250, y=200, x_size=100, y_size=100,
                   image_file_on=os.path.join('images', 'blue_button_on.png'),
                   image_file_off=os.path.join('images', 'blue_button_off.png'),
                   sound_file=os.path.join('Sounds', 'two.wav'),
                   color='blue'),

            Button(x=400, y=200, x_size=100, y_size=100,
                   image_file_on=os.path.join('images', 'yellow_button_on.png'),
                   image_file_off=os.path.join('images', 'yellow_button_off.png'),
                   sound_file=os.path.join('Sounds', 'three.wav'),
                   color='yellow'),

            Button(x=550, y=200, x_size=100, y_size=100,
                   image_file_on=os.path.join('images', 'green_button_on.png'),
                   image_file_off=os.path.join('images', 'green_button_off.png'),
                   sound_file=os.path.join('Sounds', 'four.wav'),
                   color='green')
        ]

        self.add_to_sequence()
        self.add_to_sequence()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(TITLE)

    def add_to_sequence(self):
        random_button = choice(self.buttons)
        self.sequence.append(random_button)

    def lose(self):
        if self.counter<=0:
            self.blink_leds()
            self.counter = 110
            
        if self.blink_count <= 0:
            return False
        return True
            
    
    def blink_leds(self):
        for button in self.buttons:
            button.respond(100)
        
        
    def wait_for_press(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.respond(100)
                return button
        return None

    def playback(self):
        if self.sequence_index >= len(self.sequence):
            self.sequence_index = 0
            self.is_playback = False
        else:
            self.sequence[self.sequence_index].respond(100)
            self.counter = 100
            self.sequence_index += 1

    def check_input(self, pressed_button):
        correct_button = self.sequence[self.sequence_index]
        if pressed_button.color != correct_button.color:
            self.lost = True
        else:
            if self.sequence_index + 1 < len(self.sequence):
                self.sequence_index += 1
            else:
                self.reset_playback()
                
    def reset_playback(self):
        self.sequence_index = 0
        self.add_to_sequence()
        self.counter = 100
        self.is_playback = True
        
    def game_handler(self):
                pos = pygame.mouse.get_pos()
                pressed_button = None
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.is_playback:
                        pressed_button = self.wait_for_press(pos)
                
                if not self.lost:
                    if self.is_playback:
                        self.playback()
                    elif pressed_button is not None:
                        self.check_input(pressed_button=pressed_button)
                else:
                    
                    if self.lose():
                        self.blink_count-=1
                    else:
                        pygame.quit()
                        
    def run(self):
        while self.running:
            if self.counter > 0:
                self.counter-=1 
            else:
                self.game_handler()
                
            self.screen.fill('gray')
            for button in self.buttons:
                button.draw_button(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


s1 = Simon()
s1.run()
