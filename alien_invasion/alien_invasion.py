# Created by Aaron Larkin, 09/06/2023
# Influenced by "Python Crash Course - A Hands On, Project-Based Introduction to Programming" By Eric Matthes
# Goal: Improve OOP skill, become familiar with Pygame

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        # Initialise the game, and create game resources
        pygame.init()
        self.settings = Settings()

        #(Comment the full screen section OR Comment out the windowed version section)
        # Windowed:
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Full screen:
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
                
        pygame.display.set_caption("Alien Invasion")

        # Create game statistics instance
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Play button
        self.play_button = Button(self, "Start")

    def _create_fleet(self):
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)   # Magins on each side, width of ships
        number_aliens_x = available_space_x // (2 * alien_width) # // = floor division

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        # Subtract ship height and two aliens from bottom, and one alien height from the top
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        # Spacing of one alien height between each alien row
        number_rows = available_space_y // (2 * alien_height)


        # Create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)    


    def _create_alien(self, alien_number, row_number):
         # Create an alien , place it in the row
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size
         alien.x = alien_width + 2 * alien_width * alien_number     # Margin + (2 x alien width, per alien created)
         alien.rect.x = alien.x
         alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
         self.aliens.add(alien)
         

    def run_game(self):
        # Start the main loop for the game
        while True:
            self._check_events() # Even when game inactive, need to check for Q or Close window

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()    # Allow changes to screen while waiting for player to start game

    def _update_aliens(self):
         # Update the aliens' positions
         # Check if fleet at edge
        self._check_fleet_edges()
        self.aliens.update()

        # Check for collisions between ship and aliens (Lose condition)
        # spritecollideany functions arguments: a sprite and a group. Returns first alien that collides
        if pygame.sprite.spritecollideany(self.ship, self.aliens): 
            self._ship_hit()

        # Check if an alien is at bottom of screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
            

    def _fire_bullet(self):  # Create a bullet, add it to the bullets sprite group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)  # Similar to append but specifically for pygame groups

    def _update_bullets(self):
         # Update bullet positions and delete bullets offscreen  
        self.bullets.update()
         # Delete bullets that have disappeared above the top of the screen
            # Create copy first, because we need to modify the list (its length is being used for for loop)
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)  

        self._check_bullet_alien_collisions()      

    def _check_bullet_alien_collisions(self): 
        # Check for bullets that have hit aliens. If so, delete it
        # Pygame method group collide compares groups of elements. Assigns collisions to a dictionary.
        # The true arguments tell Pygame to delete the bullets and aliens that collided
        # Can set first boolean to false to allow the bullet to continue after destroying alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    

    def _ship_hit(self):
        if self.stats.ships_left > 0:  
            # Decrement number of ship lives
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause the ship
            sleep(1)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


    def _check_events(self):
        # Responds to keypresses and mouse events 
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()        # Identify position of mouse during mouse click
                    self._check_play_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:    # Each keypress is a KEYDOWN event 
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:          # Release of a pressed key
                     self._check_keyup_events(event)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True

            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

    
    # Respond to keypresses
    def _check_keydown_events(self, event):       # K_LEFT = left key, K_RIGHT, right key
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:  
            self.ship.moving_right = True
        elif event.key == pygame.K_q:              # K_q = 'q' letter key, 
             sys.exit()                            # Exit the game
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()

    # Respond to key releases
    def _check_keyup_events(self, event):    
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    

    def _update_screen(self):
         # Redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_colour)
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                 bullet.draw_bullet()
            
            self.aliens.draw(self.screen)

            # Draw score information
            self.sb.show_score()

            # Draw the play button if the game is inactive.
            if not self.stats.game_active:
                self.play_button.draw_button()
            
            # Make the most recently drawn screen visible
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
