import sys

import pygame
from settings import Settings


class Aenigma:
    
    def __init__(self) -> None:
        # initailize and draw screen
        pygame.init()
        self.settings = Settings()

        self.player_X = 3
        self.player_Y = 6

        self.MAIN_MAP = {
            1:[0,0,1,0,0,0,0,1,0,0],
            2:[0,0,0,0,0,0,0,0,0,0],
            3:[0,0,1,0,0,0,0,1,0,0],
            4:[0,0,0,0,0,0,0,0,0,0],
            5:[0,0,0,0,0,0,0,0,0,0],
            6:[0,0,1,0,0,0,0,1,0,0],
            7:[0,0,0,0,0,0,0,0,0,0],
            8:[0,0,1,0,0,0,0,1,0,0],
            9:[0,0,0,0,0,0,0,0,0,0],
            10:[0,0,1,0,0,0,0,1,0,0]
        }

        self.visable_map = {
            1:[self.MAIN_MAP[self.player_Y-1][self.player_X-1], self.MAIN_MAP[self.player_Y-1][self.player_X], self.MAIN_MAP[self.player_Y-1][self.player_X+1]],
            2:[self.MAIN_MAP[self.player_Y][self.player_X-1], self.MAIN_MAP[self.player_Y][self.player_X], self.MAIN_MAP[self.player_Y][self.player_X+1]],
            3:[self.MAIN_MAP[self.player_Y+1][self.player_X-1], self.MAIN_MAP[self.player_Y+1][self.player_X], self.MAIN_MAP[self.player_Y+1][self.player_X+1]]
        }

        self.OBJECTS = {
            0:'images/blue-square.png',
            1:'images/X-square.png'
        }

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height,)
        )
        pygame.display.set_caption("Aenigma")

    def refresh_visable_map(self):
        self.visable_map = {
            1:[self.MAIN_MAP[self.player_Y-1][self.player_X-1], self.MAIN_MAP[self.player_Y-1][self.player_X], self.MAIN_MAP[self.player_Y-1][self.player_X+1]],
            2:[self.MAIN_MAP[self.player_Y][self.player_X-1], self.MAIN_MAP[self.player_Y][self.player_X], self.MAIN_MAP[self.player_Y][self.player_X+1]],
            3:[self.MAIN_MAP[self.player_Y+1][self.player_X-1], self.MAIN_MAP[self.player_Y+1][self.player_X], self.MAIN_MAP[self.player_Y+1][self.player_X+1]]
        }


    def generate_map(self):
        self.refresh_visable_map()
        numberX = 0
        numberY = 0
        row_number = 1
        row_position = 0
        for y in range(3):
            for x in range(3):
                image_number = self.visable_map[row_number][row_position]
                self.image = pygame.image.load(self.OBJECTS[image_number])
                self.rect = self.image.get_rect()
                self.rect.x = numberX
                self.rect.y = numberY
                self.screen.blit(self.image, self.rect)
                numberX += 100
                row_position +=1
            numberY += 100
            row_number +=1
            numberX = 0
            row_position = 0


    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()
            # controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if not self.player_X == 8:
                        self.player_X += 1
                elif event.key == pygame.K_LEFT:
                    if not self.player_X == 1:
                        self.player_X -= 1
                elif event.key == pygame.K_UP:
                    if not self.player_Y == 2:
                        self.player_Y -=1
                elif event.key == pygame.K_DOWN:
                    if not self.player_Y == 9:
                        self.player_Y += 1


        

    def run_game(self):
        # main game loop
        while True:
            self.check_events()

            # refresh screen
            self.screen.fill(self.settings.bg_color)
            self.generate_map()
            print("Player X: "+str(self.player_X)+"; Player Y: "+str(self.player_Y))
            pygame.display.flip()


if __name__ == '__main__':
    ai = Aenigma()
    ai.run_game()