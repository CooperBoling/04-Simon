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
INPUT_FRAMEBUFFER = 100
FRAME_DELAY = 200
class Simon:
    
    
    def __init__(self) -> None:
        self.sequence: list[Button] = [] 
        self.sequence_index = 0
        self.running = True
        self.current_gamestate = 'playback'
        self.counter = INIT_STARTUP_FRAMEBUFFER
        self.blink_count = NUMBER_OF_BLINKS
        self.score = -2
        
        pygame.init()
        self.text = pygame.font.SysFont("monospace", 15)
        self.frame_delay = FRAME_DELAY
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
        self.score+=1
        random_button = choice(self.buttons)
        self.sequence.append(random_button)
        if self.frame_delay>50:
            self.frame_delay-=10

    def lose(self):
        if self.blink_count <= 0:
            return False
        elif self.counter<=0:
            self.buttons[self.blink_count-1].respond(70)
            self.counter = 70
        return True
            
    
   
        
    #Resets variables needed for playback  
    def reset_playback(self):
        self.sequence_index = 0
        self.add_to_sequence()
        self.counter = INIT_STARTUP_FRAMEBUFFER
        self.current_gamestate = 'playback'

    def playback(self):
        if self.sequence_index >= len(self.sequence):
            self.sequence_index = 0
            self.current_gamestate = 'game'
        else:
            self.sequence[self.sequence_index].respond(self.frame_delay)
            self.counter = self.frame_delay
            self.sequence_index += 1




    #Checks the players input with what is next in the sequence. If the input doesn't match, the function changes the gamestate to end
    def wait_for_press(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.respond(INPUT_FRAMEBUFFER)
                return button
        
        return None
    
    def check_input(self, pressed_button):
        correct_button = self.sequence[self.sequence_index]
        if pressed_button.color != correct_button.color:
            self.current_gamestate = 'loss'
            self.counter = 100
        else:
            self.counter = 0
            if self.sequence_index + 1 < len(self.sequence):
                self.sequence_index += 1
            else:
                self.reset_playback()
                
        
                
            
    
        
    def game_handler(self):
        pos = pygame.mouse.get_pos()
        pressed_button = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and self.current_gamestate == 'game':
                pressed_button = self.wait_for_press(pos)
        if self.current_gamestate == 'playback':
                self.playback()
               
                
        elif self.current_gamestate == 'game':
            if pressed_button is not None:
                self.check_input(pressed_button=pressed_button)
        elif self.current_gamestate == 'loss':
            if self.lose():
                self.blink_count-=1
            else:
                self.running = False
        else:
            print("error: gamestate doesnot exist")
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
            label = self.text.render(f"Score: {self.score}",1,(0,0,0))
            self.screen.blit(label, (340, 50))
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


s1 = Simon()
s1.run()
