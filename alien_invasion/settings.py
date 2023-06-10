# Created by Aaron Larkin, 09/06/2023
# Influenced by "Python Crash Course - A Hands On, Project-Based Introduction to Programming" By Eric Matthes

class Settings:

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.2
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.1        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 2
        self.fleet_drop_speed = 4
        self.fleet_direction = 1          # 1 = right, -1 = left