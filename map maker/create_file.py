import pygame.font
import pygame
import sys


class MainButton():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont(None, 40)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 120
        self.main_name = "Create File"

        self.prep_main(msg)

    def prep_main(self, msg):
        self.main_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = self.main_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.main_image, self.main_image_rect)


class AffirmButton():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.affirm_width, self.affirm_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont(None, 40)

        self.affirm_rect = pygame.Rect(0, 0, self.affirm_width, self.affirm_height)
        self.affirm_rect.x = 1000
        self.affirm_rect.y = 300
        self.affirm_name = "Build File"

        self.prep_affirm(msg)

    def prep_affirm(self, msg):
        self.affirm_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.affirm_image_rect = self.affirm_image.get_rect()
        self.affirm_image_rect.center = self.affirm_rect.center

    def draw_affirm(self):
        self.screen.fill(self.button_color, self.affirm_rect)
        self.screen.blit(self.affirm_image, self.affirm_image_rect)

    def build_new_map(self, new_filename, map_size, floor_type):
        new_map = {}
        access_map = {}
        nest = []
        cool = []
        v = map_size
        some_number = 0
        t = True
        for x in range(map_size):
            if some_number == 2:
                some_number = 0
            nest.append(floor_type + some_number)
            cool.append(True)
            print("building lists")
            some_number += 1
        for y in range(map_size):
            new_map[y+1] = nest
            access_map[y+1] = cool
            print("building dicts")

                
        with open(new_filename+".py", 'x') as file_object:
            file_object.write("class MapData:\n    def __init__(self):\n        self.terrain_map = "+str(new_map)
            +"\n\n        self.access_map = "+str(access_map)+"\n\n        self.prop_map = []\n\n        self.object_map = []\n\n        self.sound_map = []\n\n        self.player_x = 1000 \
            \n\n        self.player_y = 1000")

        print("done")