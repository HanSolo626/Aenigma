import pygame
import sys
import pygame.font

class AreaLeft():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.area_width, self.area_height = 250, 800
        self.area_color = (127,127,127)

        self.area_rect = pygame.Rect(0, 0, self.area_width, self.area_height)
        self.area_rect.x = 0
        self.area_rect.y = 0


    def draw_main(self):
        self.screen.fill(self.area_color, self.area_rect)



class AreaRight():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.area_width, self.area_height = 250, 800
        self.area_color = (127,127,127)

        self.area_rect = pygame.Rect(0, 0, self.area_width, self.area_height)
        self.area_rect.x = 950
        self.area_rect.y = 0


    def draw_main(self):
        self.screen.fill(self.area_color, self.area_rect)

class AreaUp():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.area_width, self.area_height = 700, 50
        self.area_color = (127,127,127)

        self.area_rect = pygame.Rect(0, 0, self.area_width, self.area_height)
        self.area_rect.x = 250
        self.area_rect.y = 750


    def draw_main(self):
        self.screen.fill(self.area_color, self.area_rect)

class AreaDown():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.area_width, self.area_height = 700, 50
        self.area_color = (127,127,127)

        self.area_rect = pygame.Rect(0, 0, self.area_width, self.area_height)
        self.area_rect.x = 250
        self.area_rect.y = 0


    def draw_main(self):
        self.screen.fill(self.area_color, self.area_rect)