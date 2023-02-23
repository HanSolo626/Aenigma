import pygame
import sys
import os
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
from PIL import Image


class MapMaker:
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode(
            (1200, 800)
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
            1:Image.open("/Users/carsonball/Desktop/aenigma_game/images/test_square.png"),
            2:Image.open("/Users/carsonball/Desktop/aenigma_game/images/orange_test.png")
        }

        self.square_x = 60
        self.square_y = 60

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
                    self.player_X -= 60
                elif event.key == pygame.K_LEFT:
                    self.player_X += 60
                elif event.key == pygame.K_UP:
                    self.player_Y +=60
                elif event.key == pygame.K_DOWN:
                    self.player_Y -= 60




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
                numberX += self.square_x
                row_position +=1
            numberY += self.square_y
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

    # experimental functions
    def get_concat_h_repeat(self, map, column, row_number):
        dst = Image.new('RGB', (self.square_x * column, self.square_y))
        for x in range(column):
            im = map[row_number][x]
            im = self.IMAGES[im]
            dst.paste(im, (x * im.width, 0))
            p = x
            print("X done:"+str(p))
        return dst

    def get_concat_v_repeat(self, im, column, row):
        dst = Image.new('RGB', (self.square_x * column, self.square_y * row))
        for y in range(row):
            dst.paste(im, (0, y * im.height))
            p = y
            print("Y done:"+str(p))
        return dst

    def get_concat_tile_repeat(self, map, row, column):
        dst_h = self.get_concat_h_repeat(map, column, row)
        return self.get_concat_v_repeat(dst_h, column, row)

    def build_terrain_map(self, map, row, column):
        self.get_concat_tile_repeat(map, row, column).save('terrain_map.png')
        with open('terrain_map.png', 'r') as mp:
            os.remove("terrain_map.png")
            mp = pygame.image.load(mp)
            print("done")
            return mp

    def display_whole_image_map(self, image, x, y):
        rect = image.get_rect()
        rect.x = x+600
        rect.y = y+600
        self.screen.blit(image, rect)



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
        #self.affirm_file.build_new_map("big_file2", 200, 1)
        self.screen.fill((127,127,127))
        self.terrain_map = self.build_terrain_map(self.map_data.terrain_map, 200, 200)
        while True:
            self.screen.fill((127,127,127))
            # refresh screen
            self.check_events()
            #self.test_button.draw_test()
            self.draw_folders()
            self.display_whole_image_map(self.terrain_map, self.player_X, self.player_Y)
            #self.display_current_map(self.map_data.terrain_map, self.player_X, self.player_Y)
            pygame.display.update()

if __name__ == '__main__':
    ai = MapMaker()
    ai.run_program()