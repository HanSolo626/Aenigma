import pygame
import sys
import os
import pygame.font
import importlib
import os.path as path
from PIL import Image

#sys.path.append('/Users/carsonball/Desktop/aenigma_game/map maker/game_maps')
sys.path.append('saves')
sys.path.append('map maker')


from image_library import ImageLibrary
from system import QuitProgram
from system import DragMap
from system import AjustSize
from test_button import TestButton
from open_file import OpenFile
from create_file import MainButton
from create_file import AffirmButton
from create_file import PickTerrain
from terrain import Terrain
from props import Props
from objects import Objects
from sound import Sound
from side_areas import AreaLeft
from side_areas import AreaRight
from side_areas import AreaUp
from side_areas import AreaDown
from system import GeneralInfo


class MapMaker:
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode((1200, 800))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Aenigma Map Maker")

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
        self.print = GeneralInfo(self)

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
        self.pick_terrain = PickTerrain(self, "Pick Terrain")

        self.IMAGES = self.image_library.IMAGES

        self.PYGAME_IMAGES = self.image_library.PYGAME_IMAGES

        self.square_x = 60
        self.square_y = 60

        self.square_zoom_x = 10
        self.square_zoom_y = 10

        self.shift_x = 30
        self.shift_y = 230

        self.camera_x = 0
        self.camera_y = 0

        self.mouse_drag_multiplyer = 1
        self.multiplyer_status = False

        self.screen_rect = self.screen.get_rect()

        self.speed_text_color = (0,0,0)
        self.speed_font = pygame.font.SysFont("", 25)

        self.map_present = False
        self.current_file_open = ''
        self.user_text = ''
        self.text_file_limit = 15
        self.text_in_stuff = False
        self.past_mode = "Open"
        self.current_tool = "Open"

        self.current_message = "Welcome to the Aenigma Map Maker!"
        self.saved_text = 'new'

        self.displayed_map = {}

        self.prep_speed()
        self.prep_default()
        self.set_active_tool("Open")



    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN and self.text_active:
                if event.key == pygame.K_BACKSPACE and self.text_active:
                    try:
                        self.user_text = self.user_text.removesuffix(self.user_text[self.user_text.__len__()-1])
                    except IndexError:
                        self.user_text = ''
                elif event.key == pygame.K_SPACE and self.text_active:
                    self.user_text += '_'
                elif event.key == pygame.K_ESCAPE and self.text_active:
                    self.user_text = ''
                    self.current_message = self.user_text
                    self.set_active_tool("Past")
                elif event.key == pygame.K_RETURN and self.text_active:
                    self.saved_text = self.user_text
                    self.user_text = ''
                    self.current_message = self.user_text
                    self.set_active_tool("Past")
                else:
                    if self.user_text.__len__() <= self.text_file_limit:
                        self.user_text += event.unicode

            # controls
            elif event.type == pygame.KEYDOWN and self.map_present:
                if event.key == pygame.K_x:
                    if self.multiplyer_status == False:
                        self.multiplyer_status = True
                        self.mouse_drag_multiplyer = 2
                    else:
                        self.multiplyer_status = False
                        self.mouse_drag_multiplyer = 1
                elif event.key == pygame.K_RIGHT:
                    self.player_X -= 60 * self.mouse_drag_multiplyer
                    self.camera_x += 1
                elif event.key == pygame.K_LEFT:
                    self.player_X += 60 * self.mouse_drag_multiplyer
                    self.camera_x -= 1
                elif event.key == pygame.K_UP:
                    self.player_Y += 60 * self.mouse_drag_multiplyer
                    self.camera_y -= 1
                elif event.key == pygame.K_DOWN:
                    self.player_Y -= 60 * self.mouse_drag_multiplyer
                    self.camera_y += 1
                elif event.key == pygame.K_SPACE and self.terrain_active:
                    self.terrain.paint_terrain(self.map_data.terrain_map, self.player_X / 60, self.player_Y / 60, 1, self.pick_terrain.current_image)
                elif event.key == pygame.K_t:
                    print(self.displayed_map)

            if self.text_active:
                self.current_message = "Enter name: "+self.user_text

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_system_functions(mouse_pos)
                self.check_open_file_functions(mouse_pos)
                self.check_create_file_functions(mouse_pos)
                if self.map_present:
                    self.check_terrain_functions(mouse_pos)
                    self.check_object_functions(mouse_pos)
                    self.check_sound_functions(mouse_pos)
                    self.check_prop_functions(mouse_pos)


    def get_concat_h_repeat(self, map, column, row_number):
        dst = Image.new('RGB', (self.square_x * column, self.square_y))
        for x in range(column):
            im = map[row_number][x]
            im = self.IMAGES[im]
            dst.paste(im, (x * im.width, 0))
            p = x
            self.current_message = "X done:"+str(p)
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
            self.current_message = "X done:"+str(p)
        return dst

    def get_concat_v_repeat(self, im, column, row):
        dst = Image.new('RGB', (self.square_x * column, self.square_y * row))
        for y in range(row):
            dst.paste(im, (0, y * im.height))
            p = y
            self.current_message = "Y done:"+str(p)
        return dst
    
    def get_concat_v_repeat_zoom(self, im, column, row):
        dst = Image.new('RGB', (self.square_zoom_x * column, self.square_zoom_y * row))
        for y in range(row):
            dst.paste(im, (0, y * im.height))
            p = y
            self.current_message = "Y done:"+str(p)
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
            self.current_message = "done"
            return mp
    
    def build_zoom_out_map(self, map, row, column):
        self.get_concat_tile_repeat_zoom(map, row, column).save('terrain_map_zoom.png')
        with open('terrain_map_zoom.png', 'r') as mp:
            os.remove("terrain_map_zoom.png")
            mp = pygame.image.load(mp)
            self.current_message = "done"
            return mp

    def display_whole_image_map(self, image, x, y):
        rect = image.get_rect()
        rect.x = x+600
        rect.y = y+600
        self.screen.blit(image, rect)

    def new_display_map(self, map, x, y):
        ls = []
        self.h = 0
        self.v = 0
        for v in range(13):
            self.v += 1
            self.v = int(self.v)
            for h in range(13):
                self.h += 1
                if (x + self.h - 7) < 0:
                    ls.append(0)
                else:
                    try:
                        ls.append(map[y + self.v - 6][x + self.h - 7])
                    except KeyError:
                        ls.append(0)
            self.displayed_map[self.v] = ls
            ls = []
            self.h = 0
        numberX = 250
        numberY = 50
        row_number = 1
        row_position = 0
        for y in range(13):
            for x in range(13):
                image_number = self.displayed_map[row_number][row_position]
                self.image = self.image_library.PRELOADED_IMAGES[image_number][0]
                self.rect = self.image_library.PRELOADED_IMAGES[image_number][1]
                self.rect.x = numberX - 40
                self.rect.y = numberY - 40
                self.screen.blit(self.image, self.rect)
                numberX += 60
                row_position +=1
            numberY += 60
            row_number +=1
            numberX = 250
            row_position = 0

    def check_open_file_functions(self, mouse_pos):
        if self.open_file.main_rect.collidepoint(mouse_pos):
            self.draw_open_file_buttons()
            self.set_active_tool("Open")
        if self.open_file.rect_left.collidepoint(mouse_pos) and self.open_file_active:
            self.open_file.current_file -= 1
        if self.open_file.rect_right.collidepoint(mouse_pos) and self.open_file_active:
            self.open_file.current_file += 1

        if self.open_file.open_rect.collidepoint(mouse_pos) and self.open_file_active:
            self.map_present = True
            self.current_file_open = path.splitext(self.open_file.file_list[self.open_file.current_file])[0]
    
    def check_create_file_functions(self, mouse_pos):
        if self.create_file.main_rect.collidepoint(mouse_pos):
            self.draw_create_file_buttons()
            self.set_active_tool("Create")
        if self.pick_terrain.rect_left.collidepoint(mouse_pos) and self.create_file_active == True:
            self.pick_terrain.current_image -= 1
        if self.pick_terrain.rect_right.collidepoint(mouse_pos) and self.create_file_active == True:
            self.pick_terrain.current_image += 1

        if self.affirm_file.affirm_rect.collidepoint(mouse_pos) and self.create_file_active:
            self.current_message = self.affirm_file.build_new_map(self.saved_text, 200, self.pick_terrain.current_image)

        if self.pick_terrain.pick_name_rect.collidepoint(mouse_pos) and self.create_file_active:
            self.set_active_tool("Text")


    def check_terrain_functions(self, mouse_pos):
        if self.terrain.main_rect.collidepoint(mouse_pos):
            self.draw_terrain_buttons()
            self.set_active_tool("Terrain")

        if self.pick_terrain.rect_left.collidepoint(mouse_pos) and self.terrain_active == True:
            self.pick_terrain.current_image -= 1
        if self.pick_terrain.rect_right.collidepoint(mouse_pos) and self.terrain_active == True:
            self.pick_terrain.current_image += 1

    def check_prop_functions(self, mouse_pos):
        if self.props.main_rect.collidepoint(mouse_pos):
            self.draw_prop_buttons()
            self.set_active_tool("Prop")

    def check_object_functions(self, mouse_pos):
        if self.objects.main_rect.collidepoint(mouse_pos):
            self.draw_object_buttons()
            self.set_active_tool("Object")

    def check_sound_functions(self, mouse_pos):
        if self.sound.main_rect.collidepoint(mouse_pos):
            self.draw_sound_buttons()
            self.set_active_tool("Sound")

    def check_system_functions(self, mouse_pos):
        if self.quit_program.main_rect.collidepoint(mouse_pos):
            self.quit_program.quit_program()
        elif self.ajust_size.zoom_out_rect.collidepoint(mouse_pos) and self.map_present:
            self.current_map = self.zoom_out_map
        elif self.ajust_size.zoom_in_rect.collidepoint(mouse_pos) and self.map_present:
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

    def prep_default(self):
        self.default = pygame.image.load(self.image_library.SYSTEM_IMAGES[6])
        self.default_rect = self.default.get_rect()
        self.default_rect.x = 250
        self.default_rect.y = 50

    def set_neutral(self):
        self.create_file_active = False
        self.terrain_active = False
        self.prop_active = False
        self.object_active = False
        self.sound_active = False
        self.area_left.draw_main()

    def set_active_tool(self, mode):
        self.open_file_active = False
        self.create_file_active = False
        self.terrain_active = False
        self.prop_active = False
        self.object_active = False
        self.sound_active = False
        self.text_active = False
        if mode == "Past":
            mode = self.past_mode
        self.past_mode = self.current_tool
        if mode == "Create":
            self.create_file_active = True
        elif mode == "Terrain":
            self.terrain_active = True
        elif mode == "Prop":
            self.prop_active = True
        elif mode == "Object":
            self.object_active = True
        elif mode == "Sound":
            self.sound_active = True
        elif mode == "Text":
            self.text_active = True
        elif mode == "Open":
            self.open_file_active = True
        self.current_tool = mode
        print(self.current_tool)
        print(self.text_active)

    def import_map(self, file_name):
        if file_name == '':
            self.map_present = False
        else:
            self.map_data = importlib.import_module(file_name)
            self.player_X = self.map_data.player_x
            self.player_Y = self.map_data.player_y
            
            

    def display_speed(self):
        self.screen.blit(self.speed_image, self.speed_rect)

    def draw_folders(self, draw_tools):
        if draw_tools:
            self.open_file.draw_main()
            self.create_file.draw_main()
            self.terrain.draw_main()
            self.props.draw_main()
            self.objects.draw_main()
            self.sound.draw_main()
        else:
            self.open_file.draw_main()
            self.create_file.draw_main()

        if self.open_file_active == True:
            self.open_file.draw_all()
        if self.create_file_active == True:
            self.draw_create_file_buttons()
        if self.terrain_active == True:
            self.draw_terrain_buttons()
        if self.prop_active == True:
            self.props.draw_all()
        if self.object_active == True:
            self.objects.draw_all()
        if self.sound_active == True:
            self.sound.draw_all()

    def draw_system(self):
        self.quit_program.draw_main()
        self.drag_area.draw_drag_area()
        self.display_speed()
        self.ajust_size.draw_all_zoom()
        self.print.print_m(self.current_message)

    def draw_sides(self):
        self.area_left.draw_main()
        self.area_right.draw_main()
        self.area_up.draw_main()
        self.area_down.draw_main()

    def draw_create_file_buttons(self):
        self.create_file.draw_main()
        self.affirm_file.draw_affirm()
        self.pick_terrain.draw_main()
        self.pick_terrain.draw_selected_image(self.pick_terrain.load_selected_terrain())
        self.pick_terrain.draw_words(self.pick_terrain.prep_words(self.saved_text)[0], self.pick_terrain.prep_words(self.saved_text)[1])
        self.pick_terrain.draw_pick_name()

    def draw_terrain_buttons(self):
        self.terrain.draw_main()
        self.terrain.draw_marker()
        self.pick_terrain.draw_main()
        self.pick_terrain.draw_selected_image(self.pick_terrain.load_selected_terrain())

    def draw_prop_buttons(self):
        self.props.draw_main()

    def draw_object_buttons(self):
        self.objects.draw_main()

    def draw_open_file_buttons(self):
        self.open_file.draw_all()
        
    def draw_sound_buttons(self):
        self.sound.draw_main()

    def draw_default(self):
        self.screen.blit(self.default, self.default_rect)



    def run_program(self):
        # initalize everything
        self.draw_system()
        self.draw_folders(True)
        self.set_active_tool("Create")
        self.draw_folders(True)
        self.set_active_tool("Terrain")
        self.draw_folders(True)
        self.set_active_tool("Prop")
        self.draw_folders(True)
        self.set_active_tool("Object")
        self.draw_folders(True)
        self.set_active_tool("Sound")
        self.draw_folders(True)
        self.set_active_tool("Open")
        while True:
            if self.map_present:
                # get map data
                self.import_map(self.current_file_open)

                #self.terrain_map = self.build_terrain_map(self.map_data.terrain_map, self.map_data.size_x, self.map_data.size_y)
                #self.zoom_out_map = self.build_zoom_out_map(self.map_data.terrain_map, self.map_data.size_x, self.map_data.size_y)
                #self.current_map = self.terrain_map

                while self.map_present:
                    self.screen.fill((0,0,0))
                    # refresh screen
                    self.check_events()
                    self.prep_speed()
                    #self.display_whole_image_map(self.current_map, self.player_X - self.shift_x, self.player_Y - self.shift_y)
                    self.new_display_map(self.map_data.terrain_map, self.camera_x, self.camera_y)
                    self.draw_sides()
                    self.draw_system()
                    self.draw_folders(True)
                    self.open_file.update_file_list()
                    pygame.display.update()
            else:
                while not self.map_present:
                    self.screen.fill((0,0,0))
                    # refresh screen
                    self.check_events()
                    self.prep_speed()
                    self.draw_default()
                    self.draw_sides()
                    self.draw_system()
                    self.draw_folders(False)
                    self.open_file.update_file_list()
                    pygame.display.update()

            

if __name__ == '__main__':
    ai = MapMaker()
    ai.run_program()