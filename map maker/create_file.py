import pygame.font
import pygame
import shutil
from image_library import ImageLibrary
from open_file import OpenFile


class MainButton():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 40)

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
        self.font =  pygame.font.SysFont("", 40)

        self.affirm_rect = pygame.Rect(0, 0, self.affirm_width, self.affirm_height)
        self.affirm_rect.x = 1000
        self.affirm_rect.y = 450
        self.affirm_name = "Build File"

        self.open_file = OpenFile(self, "")

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
        t = True
        if new_filename == '':
            return "Error: Give the file a name."
        elif new_filename+".py" in self.open_file.get_save_files():
            return "Error: File name taken! Pick another."
        else:
            for x in range(map_size):
                nest.append(floor_type)
                cool.append(True)
            for y in range(map_size):
                new_map[y+1] = nest
                access_map[y+1] = cool

                    
            with open(new_filename+".py", 'x') as file_object:
                file_object.write("terrain_map = "+str(new_map)+"\naccess_map = "+str(access_map)+"\nprop_map = []\nobject_map = []\nsound_map = []\nplayer_x = 1\nplayer_y = 1\nsize_x = "+str(map_size)+"\nsize_y = "+str(map_size))

            shutil.move(new_filename+".py","saves/"+new_filename+".py")
            return "Map created succesfully!"



class PickTerrain():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image_library = ImageLibrary()

        self.main_width, self.main_height = 180, 50
        self.pick_name_width, self.pick_name_height = 100, 45
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 40)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 985
        self.main_rect.y = 50
        self.main_name = "Pick Terrain"

        self.pick_name_image_rect = pygame.Rect(0, 0, self.pick_name_width, self.pick_name_height)
        self.pick_name_image_rect.x = 1000
        self.pick_name_image_rect.y = 350

        self.current_image = 3
        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.file_name = "NewMap"

        self.prep_main(msg)
        self.prep_pick_name()

    def prep_main(self, msg):
        self.main_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = self.main_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.main_image, self.main_image_rect)

    def draw_pick_name(self):
        self.screen.fill(self.button_color, self.pick_name_image_rect)
        self.screen.blit(self.pick_name, self.pick_name_rect)

    def draw_selection_buttons(self, right, left):
        self.rect_right = right.get_rect()
        self.rect_right.x = 1015
        self.rect_right.y = 210
        self.rect_left = left.get_rect()
        self.rect_left.x = 1095
        self.rect_left.y = 210

        self.screen.blit(right, self.rect_right)
        self.screen.blit(left, self.rect_left)
        
    def draw_selected_image(self, image):
        rect = image.get_rect()
        rect.x = 1045
        rect.y = 130
        self.screen.blit(image, rect)

        self.draw_selection_buttons(self.arrow_left, self.arrow_right)

    def prep_words(self, words):
        image = self.font.render(words, True, self.text_color)
        image_rect = image.get_rect()
        image_rect.x = 1000
        image_rect.y = 300
        return image, image_rect
    
    def prep_pick_name(self):
        self.pick_name = self.font.render("Name", True, self.text_color, self.button_color)
        self.pick_name_rect = self.pick_name.get_rect()
        self.pick_name_rect.center = self.pick_name_image_rect.center

    
    def draw_words(self, image, image_rect):
        self.screen.blit(image, image_rect)

    def load_selected_terrain(self):
        if self.current_image <= 0:
            self.current_image = self.image_library.PYGAME_IMAGES.__len__()
        elif self.current_image >= self.image_library.PYGAME_IMAGES.__len__()+1:
            self.current_image = 1
        return pygame.image.load(self.image_library.PYGAME_IMAGES[self.current_image])