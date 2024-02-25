
import pygame
from pygame.mixer import Sound
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
            self.led_on()
            self.counter -= 1
        else:
            self.led_off()

        display.blit(self.current_image, (self.x, self.y))

    def led_on(self):
        self.current_image = self.image_file_on

    def led_off(self):
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