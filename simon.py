#Name: Cooper Boling, Jude Barcelona

import pineworkslabs.RPi as GPIO
from time import sleep
from random import choice
import pygame
from pygame.mixer import Sound 
import os

pygame.init()

GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

class Button:
    def __init__(self, switch:int, led:int, sound:str, color:str) -> None:
        self.switch = switch
        self.led = led
        self.sound: Sound = Sound(soundFile)
        self.color = color

        self.setupGPIO()
    
    def setupGPIO(self):
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.led, GPIO.OUT)

    def turnOnLight(self):
        GPIO.output(self.led, True)

    def turnOffLight(self):
        GPIO.output(self.led, False)

    def isPressed(self):
        result = GPIO.input(self.switch)
        return result

    def respond(self):
        self.turnOnLight()
        self.sound.play()
        sleep(1)
        self.turnOffLight()
        sleep(0.25)

    def __str__(self) -> str:
        return self.color

class Simon:
    WELCOMEMESSAGE = 'Welcome to Simon! Press crtl+c to exit at anytime'

    BUTTONS = [
        Button(switch=20, led=6, sound=os.path.join('Sounds', 'one.wav'), color='red'),
        Button(switch=16, led=13, sound=os.path.join('Sounds', 'two.wav'), color='blue'),
        Button(switch=12, led=19, sound=os.path.join('Sounds', 'three.wav'), color='yellow'),
        Button(switch=26, led=21, sound=os.path.join('Sounds', 'four.wav'), color='green')
    ]

    def __init__(self, debug=True) -> None:
        self.debug = debug
        self.sequence: list[Button] = []

    def debugOut(self, *args):
        if self.debug:
            print(*args)

    def blinkLEDS(self):
        leds = []
        for button in Simon.BUTTONS:
            leds.append(button.led)
        GPIO.output(leds, True)
        sleep(0.5)
        GPIO.output(leds, False)
        sleep(0.5)

        #if up top doesnt work
        #for button in Simon.BUTTONS:
            #button.turnOnLight()
            #sleep(0.5)
            #button.turnOffLight()
            #sleep(0.5)
        
    def addToSequence(self):
        randomButton = choice(Simon.BUTTONS)
        self.sequence.append(randomButton)

    def lose(self):
        for _ in range(4):
            self.blinkLEDS()
        GPIO.cleanup()
        exit()
    
    def waitForPress(self):
        while True:
            for button in Simon.BUTTONS:
                if button.isPressed():
                    self.debugOut(button.color)
                    button.respond()
                    return button

    def playback(self):
        for button in self.sequence:
            button.respond()

    def checkInput(self, pressedButton, correctButton):
        if pressedButton.switch != correctButton.button:
            self.lose()

    def run(self):
        print(Simon.WELCOMEMESSAGE)

        self.addToSequence()
        self.addToSequence()

        try:
            while True:
                self.addToSequence()
                self.playback()
                self.debugOut(*self.sequence)
                for button in self.sequence:
                    pressedButton = self.waitForPress()
                    self.checkInput(pressedButton, button)
        
        except KeyboardInterrupt:
            GPIO.cleanup()

s1 = Simon()
s1.run()
