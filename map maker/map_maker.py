import pygame
import sys
import pygame.font
from test_button import TestButton
from open_file import OpenFile
from create_file import MainButton
from create_file import AffirmButton
from terrain import Terrain
from props import Props
from objects import Objects
from sound import Sound
from big_file2 import MapData


class MapMaker:
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode(
            (1800, 1200)
        )
        pygame.display.set_caption("Aenigma Map Maker")

        # get map data
        self.map_data = MapData()

        # make folder buttons
        self.test_button = TestButton(self, "Test")
        self.open_file = OpenFile(self, "Open File")
        self.create_file = MainButton(self, "Create File")
        self.terrain = Terrain(self, "Terran")
        self.props = Props(self, "Props")
        self.objects = Objects(self, "Objects")
        self.sound = Sound(self, "Sound")

        # create file buttons
        self.affirm_file = AffirmButton(self, "Build File")

        self.IMAGES = {
            1:"/Users/carsonball/Desktop/aenigma_game/images/test_square.png",
            2:"/Users/carsonball/Desktop/aenigma_game/images/orange_test.png"
        }

        self.player_X = self.map_data.player_x
        self.player_Y = self.map_data.player_y




    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()
            # controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player_X += 1
                elif event.key == pygame.K_LEFT:
                    self.player_X -= 1
                elif event.key == pygame.K_UP:
                    self.player_Y -=1
                elif event.key == pygame.K_DOWN:
                    self.player_Y += 1




    def display_current_map(self, map, x, y):
        self.refresh_visable_map(map, x, y)
        numberX = 250
        numberY = 0
        row_number = 1
        row_position = 0
        for y in range(20):
            for x in range(20):
                image_number = self.visable_map[row_number][row_position]
                self.image = pygame.image.load(self.IMAGES[image_number])
                self.rect = self.image.get_rect()
                self.rect.x = numberX
                self.rect.y = numberY
                self.screen.blit(self.image, self.rect)
                numberX += 60
                row_position +=1
            numberY += 60
            row_number +=1
            numberX = 250
            row_position = 0

    

    def refresh_visable_map(self, map, x, y):
        self.visable_map = {}
        nest = []
        e = -20
        p = -20
        for e in range(20):
            for p in range(20):
                nest.append(map[y+e+1][x+p+1])
            self.visable_map[e+1] = nest
            nest = []
        #print(self.visable_map)



    def _check_test_button(self, mouse_pos):
        if self.test_button.rect.collidepoint(mouse_pos):
            print("works!")

    def draw_folders(self):
        self.open_file.draw_all()
        self.draw_create_file_buttons()
        self.terrain.draw_all()
        self.props.draw_all()
        self.objects.draw_all()
        self.sound.draw_all()

    def draw_create_file_buttons(self):
        self.create_file.draw_main()
        self.affirm_file.draw_affirm()



    def run_program(self):
        #self.affirm_file.build_new_map("big_file2", 2000, 1)
        self.screen.fill((127,127,127))
        while True:
            # refresh screen
            self.check_events()
            #self.test_button.draw_test()
            self.draw_folders()
            self.display_current_map(self.map_data.terrain_map, self.player_X, self.player_Y)
            pygame.display.flip()

if __name__ == '__main__':
    ai = MapMaker()
    ai.run_program()