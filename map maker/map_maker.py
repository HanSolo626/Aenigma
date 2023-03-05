import pygame
import sys
import os
import pygame.font
import time

sys.path.append('/Users/carsonball/Desktop/aenigma_game/map maker/game_maps')

from image_library import ImageLibrary
from system import QuitProgram
from system import DragMap
from system import AjustSize
from test_button import TestButton
from open_file import OpenFile
from create_file import MainButton
from create_file import AffirmButton
from terrain import Terrain
from props import Props
from objects import Objects
from sound import Sound
from side_areas import AreaLeft
from side_areas import AreaRight
from side_areas import AreaUp
from side_areas import AreaDown
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

        # get images
        self.image_library = ImageLibrary()

        # create sides
        self.area_left = AreaLeft(self)
        self.area_right = AreaRight(self)
        self.area_up = AreaUp(self)
        self.area_down = AreaDown(self)

        # create system functions
        self.quit_program = QuitProgram(self, "Exit")
        self.drag_area = DragMap(self)
        self.ajust_size = AjustSize(self)

        # make folder buttons
        self.test_button = TestButton(self, "Test")
        self.open_file = OpenFile(self, "Open File")
        self.create_file = MainButton(self, "Create File")
        self.terrain = Terrain(self, "Terrain")
        self.props = Props(self, "Props")
        self.objects = Objects(self, "Objects")
        self.sound = Sound(self, "Sound")

        # create file buttons
        self.affirm_file = AffirmButton(self, "Build File")

        self.IMAGES = self.image_library.IMAGES

        self.PYGAME_IMAGES = self.image_library.PYGAME_IMAGES

        self.square_x = 60
        self.square_y = 60

        self.square_zoom_x = 10
        self.square_zoom_y = 10

        self.shift_x = 30
        self.shift_y = 30

        self.player_X = self.map_data.player_x
        self.player_Y = self.map_data.player_y

        self.mouse_drag_multiplyer = 1
        self.multiplyer_status = False

        self.screen_rect = self.screen.get_rect()

        self.speed_text_color = (0,0,0)
        self.speed_font = pygame.font.SysFont(None, 25)

        self.prep_speed()





    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()

            # controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    if self.multiplyer_status == False:
                        self.multiplyer_status = True
                        self.mouse_drag_multiplyer = 2
                    else:
                        self.multiplyer_status = False
                        self.mouse_drag_multiplyer = 1
                elif event.key == pygame.K_RIGHT:
                    self.player_X -= 60 * self.mouse_drag_multiplyer
                elif event.key == pygame.K_LEFT:
                    self.player_X += 60 * self.mouse_drag_multiplyer
                elif event.key == pygame.K_UP:
                    self.player_Y += 60 * self.mouse_drag_multiplyer
                elif event.key == pygame.K_DOWN:
                    self.player_Y -= 60 * self.mouse_drag_multiplyer

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_system_functions(mouse_pos)


    def get_concat_h_repeat(self, map, column, row_number):
        dst = Image.new('RGB', (self.square_x * column, self.square_y))
        for x in range(column):
            im = map[row_number][x]
            im = self.IMAGES[im]
            dst.paste(im, (x * im.width, 0))
            p = x
            print("X done:"+str(p))
        return dst
    
    def get_concat_h_repeat_zoom(self, map, column, row_number):
        dst = Image.new('RGB', (self.square_zoom_x * column, self.square_zoom_y))
        for x in range(column):
            im = map[row_number][x]
            im = self.PYGAME_IMAGES[im]
            im = pygame.image.load(im)
            im = pygame.transform.scale(im, (10, 10))
            pygame.image.save(im, 'image_file.png')
            im = Image.open('image_file.png')
            os.remove('image_file.png')
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
    
    def get_concat_v_repeat_zoom(self, im, column, row):
        dst = Image.new('RGB', (self.square_zoom_x * column, self.square_zoom_y * row))
        for y in range(row):
            dst.paste(im, (0, y * im.height))
            p = y
            print("Y done:"+str(p))
        return dst

    def get_concat_tile_repeat(self, map, row, column):
        dst_h = self.get_concat_h_repeat(map, column, row)
        return self.get_concat_v_repeat(dst_h, column, row)

    def get_concat_tile_repeat_zoom(self, map, row, column):
        dst_h = self.get_concat_h_repeat_zoom(map, column, row)
        return self.get_concat_v_repeat_zoom(dst_h, column, row)

    def build_terrain_map(self, map, row, column):
        self.get_concat_tile_repeat(map, row, column).save('terrain_map.png')
        with open('terrain_map.png', 'r') as mp:
            os.remove("terrain_map.png")
            mp = pygame.image.load(mp)
            print("done")
            return mp
    
    def build_zoom_out_map(self, map, row, column):
        self.get_concat_tile_repeat_zoom(map, row, column).save('terrain_map_zoom.png')
        with open('terrain_map_zoom.png', 'r') as mp:
            os.remove("terrain_map_zoom.png")
            mp = pygame.image.load(mp)
            print("done")
            return mp

    def display_whole_image_map(self, image, x, y):
        rect = image.get_rect()
        rect.x = x+600
        rect.y = y+600
        self.screen.blit(image, rect)



    def check_system_functions(self, mouse_pos):
        if self.quit_program.main_rect.collidepoint(mouse_pos):
            self.quit_program.quit_program()
        elif self.ajust_size.zoom_out_rect.collidepoint(mouse_pos):
            self.current_map = self.zoom_out_map
        elif self.ajust_size.zoom_in_rect.collidepoint(mouse_pos):
            self.current_map = self.terrain_map

        # This is something I might work on later.
        #elif self.drag_area.rect.collidepoint(mouse_pos):
        #    new_map_pos = self.drag_area.drag_map_by_mouse(mouse_pos, self.mouse_drag_multiplyer)
        #    print(new_map_pos)
            #self.player_X, self.player_Y += new_map_pos[0], new_map_pos[1]

    def prep_speed(self):
        speed_str = "Speed: "+str(self.mouse_drag_multiplyer)
        self.speed_image = self.speed_font.render(speed_str, True, self.speed_text_color, (127,127,127))

        self.speed_rect = self.speed_image.get_rect()
        self.speed_rect.x = 275
        self.speed_rect.y = 12

    def display_speed(self):
        self.screen.blit(self.speed_image, self.speed_rect)

    def draw_folders(self):
        self.open_file.draw_all()
        self.draw_create_file_buttons()
        self.terrain.draw_all()
        self.props.draw_all()
        self.objects.draw_all()
        self.sound.draw_all()

    def draw_system(self):
        self.quit_program.draw_main()
        self.drag_area.draw_drag_area()
        self.display_speed()
        self.ajust_size.draw_all_zoom()

    def draw_sides(self):
        self.area_left.draw_main()
        self.area_right.draw_main()
        self.area_up.draw_main()
        self.area_down.draw_main()

    def draw_create_file_buttons(self):
        self.create_file.draw_main()
        self.affirm_file.draw_affirm()



    def run_program(self):
        #self.affirm_file.build_new_map("big_file2", 200, 1)
        self.screen.fill((127,127,127))
        self.terrain_map = self.build_terrain_map(self.map_data.terrain_map, 200, 200)
        self.zoom_out_map = self.build_zoom_out_map(self.map_data.terrain_map, 200, 200)
        self.current_map = self.terrain_map
        while True:
            self.screen.fill((0,0,0))
            # refresh screen
            self.check_events()
            self.prep_speed()
            self.display_whole_image_map(self.current_map, self.player_X - self.shift_x, self.player_Y - self.shift_y)
            self.draw_sides()
            self.draw_system()
            #self.test_button.draw_test()
            self.draw_folders()
            pygame.display.update()
            

if __name__ == '__main__':
    ai = MapMaker()
    ai.run_program()