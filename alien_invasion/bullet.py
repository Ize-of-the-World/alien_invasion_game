# Created by Aaron Larkin, 09/06/2023
# Influenced by "Python Crash Course - A Hands On, Project-Based Introduction to Programming" By Eric Matthes

import pygame
from pygame.sprite import Sprite

# Inherit from pygame Sprite class - to allow grouping of related elements
class Bullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        # Update the decimal position of the bullet, and then update the rect position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw the bullet to the screen
        pygame.draw.rect(self.screen, self.colour, self.rect)
    
