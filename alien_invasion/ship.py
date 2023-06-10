# Created by Aaron Larkin, 09/06/2023
# Influenced by "Python Crash Course - A Hands On, Project-Based Introduction to Programming" By Eric Matthes

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        # Initialise ship 
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load('images\\ship2.png')
        self.rect = self.image.get_rect()

        # Starts ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store dec value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_left = False
        self.moving_right = False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        # Update the ship's position based on the movement flag
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        # Draw ship at its current location
        self.screen.blit(self.image, self.rect)

