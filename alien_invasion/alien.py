# Created by Aaron Larkin, 09/06/2023
# Influenced by "Python Crash Course - A Hands On, Project-Based Introduction to Programming" By Eric Matthes

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set the rect attribute
        self.image = pygame.image.load('images\\alien_ship.png')
        self.rect = self.image.get_rect()

        # Each alien starts near the top left of screen (the image's height and width away)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        # True if alien is at screen's edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        # Move alien to the right
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

        

