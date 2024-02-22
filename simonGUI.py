import pygame
from pygame.mixer import Sound
from random import choice
import os
import sys

FPS = 100
SCREEN_SIZE = (720, 540)


class Button:
    def __init__(self, x: int, y: int, x_size: int, y_size: int, image_file_on: str, image_file_off: str,
                 sound_file: str, color: str) -> None:
        self.x, self.y = x, y
        self.x_size, self.y_size = x_size, y_size

        self.image_file_on: pygame.image = pygame.transform.scale(pygame.image.load(image_file_on),
                                                                   (self.x_size, self.y_size))
        self.image_file_off: pygame.image = pygame.transform.scale(pygame.image.load(image_file_off),
                                                                    (self.x_size, self.y_size))

        self.current_image = self.image_file_off
        self.sound: Sound = Sound(sound_file)

        self.counter = 0
        self.color = color

    def draw_button(self, display):
        if self.counter > 0:
            self.on()
            self.counter -= 1
        else:
            self.off()

        display.blit(self.current_image, (self.x, self.y))

    def on(self):
        self.current_image = self.image_file_on

    def off(self):
        self.current_image = self.image_file_off

    def respond(self, count):
        self.counter = count
        self.sound.play()

    def is_on(self):
        return self.current_image == self.image_file_on

    def switch_state(self):
        if self.is_on():
            self.current_image = self.image_file_off
        else:
            self.current_image = self.image_file_on

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.x_size and self.y <= mouse_pos[1] <= self.y + self.y_size


class Simon:
    TITLE = 'Simon Game!'

    def __init__(self) -> None:
        self.sequence: list[Button] = []
        self.sequence_index = 0
        self.running = True
        self.is_playback = True
        self.counter = 200
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
        pygame.display.set_caption("Simon Game")

    def add_to_sequence(self):
        random_button = choice(self.buttons)
        self.sequence.append(random_button)

    def lose(self):
        pygame.quit()
        
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
            self.lose()
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
        
    def user_input(self):
                pos = pygame.mouse.get_pos()
                pressed_button = None
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pressed_button = self.wait_for_press(pos)

                if pressed_button is not None:
                    self.check_input(pressed_button=pressed_button)
                    
    def run(self):
        while self.running:
            if self.counter > 0:
                self.counter-=1
            else:
                if not self.is_playback:
                    self.user_input()
                else:
                    self.playback()

            self.screen.fill('gray')
            for button in self.buttons:
                button.draw_button(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


s1 = Simon()
s1.run()
