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
        self.affirm_rect.y = 600
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

    def build_new_map(self, new_filename, map_size, floor_type, base_access):
        new_map = {}
        access_map = [[(0,map_size-1),1,map_size,0]]
        nest = []
        v = map_size
        t = True
        vision = 0
        if new_filename == '':
            return "Error: Give the file a name."
        elif new_filename+".py" in self.open_file.get_save_files():
            return "Error: File name taken! Pick another."
        else:
            for x in range(map_size):
                nest.append(floor_type)
            for y in range(map_size):
                new_map[y+1] = nest

            
            
            self.write_to_file(new_filename, 'x', new_map, [], [], [], access_map, base_access, vision, map_size)
            #with open(new_filename+".py", 'x') as file_object:
            #    file_object.write("terrain_map = "+str(new_map)+"\naccess_map = "+str(access_map)+"\nprop_map = []\nobject_map = []\nsound_map = []\nplayer_x = 1\nplayer_y = 1\nsize_x = "+str(map_size)+"\nsize_y = "+str(map_size))

            return "Map created succesfully!"
        
    def write_to_file(self, filename, mode, terrain, prop, object_, sound, access, base, base_vision, map_size):
        with open(filename+".py", mode) as file_object:
            file_object.write("terrain_map = "+str(terrain)+"\nprop_map = "+str(prop)+"\nobject_map = "+str(object_)+"\nsound_map = "+str(sound)+"\nplayer_x = 1\nplayer_y = 1\nsize_x = "+str(map_size)+"\nsize_y = "+str(map_size)+"\naccess_map="+str(access)+"\nbase_access="+str(base)+"\nbase_vision="+str(base_vision))
        shutil.move(filename+".py","saves/"+filename+".py")




class PickTerrain():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image_library = ImageLibrary()

        self.main_width, self.main_height = 180, 50
        self.pick_name_width, self.pick_name_height = 100, 45
        self.pick_size_width, self.pick_size_height = 100, 45
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 40)
        self.small_font = pygame.font.SysFont("", 30)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 985
        self.main_rect.y = 50
        self.main_name = "Pick Terrain"

        self.pick_name_image_rect = pygame.Rect(0, 0, self.pick_name_width, self.pick_name_height)
        self.pick_name_image_rect.x = 1025
        self.pick_name_image_rect.y = 350

        self.pick_size_image_rect = pygame.Rect(0,0, self.pick_size_width, self.pick_size_height)
        self.pick_size_image_rect.x = 1025
        self.pick_size_image_rect.y = 500

        self.current_image = 0
        self.current_map_size = 200
        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.file_name = "NewMap"

        self.prep_main(msg)
        self.prep_pick_name()
        self.prep_pick_size()

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

    def draw_pick_size(self):
        self.screen.fill(self.button_color, self.pick_size_image_rect)
        self.screen.blit(self.pick_size, self.pick_size_rect)

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
        image = self.small_font.render(words, True, self.text_color)
        pretend_image = self.small_font.render("", True, self.text_color)
        image_rect = image.get_rect()
        pretend_rect = pretend_image.get_rect()
        pretend_rect.x = 1075
        pretend_rect.y = 300
        image_rect.center = pretend_rect.center
        return image, image_rect
    
    
    def prep_pick_name(self):
        self.pick_name = self.font.render("Name", True, self.text_color, self.button_color)
        self.pick_name_rect = self.pick_name.get_rect()
        self.pick_name_rect.center = self.pick_name_image_rect.center
    
    def prep_pick_size(self):
        self.pick_size = self.font.render("Size", True, self.text_color, self.button_color)
        self.pick_size_rect = self.pick_size.get_rect()
        self.pick_size_rect.center = self.pick_size_image_rect.center


    def draw_words(self, image, image_rect):
        self.screen.blit(image, image_rect)

    def load_selected_terrain(self):
        #if self.current_image < 0:
            #self.current_image = self.image_library.PRELOADED_IMAGES.__len__()
        #    self.current_image = list(dict.keys(self.image_library.PRELOADED_IMAGES))[self.image_library.PRELOADED_IMAGES.__len__()-1]
        #    print(self.current_image)
        #elif self.current_image == list(dict.keys(self.image_library.PRELOADED_IMAGES))[self.image_library.PRELOADED_IMAGES.__len__()-1]:
        #    self.current_image = 0
        return self.image_library.PRELOADED_IMAGES[self.current_image][0]
    
    def add_substract_terrain(self, operator):
        a = self.current_image
        b = list(dict.keys(self.image_library.PRELOADED_IMAGES))
        c = b.index(a)
        if operator == "-":
            if c == 0:
                self.current_image = b[b.__len__()-1]
            else:
                self.current_image = b[c-1]
        elif operator == "+":
            if c == b.__len__()-1:
                self.current_image = 0
            else:
                self.current_image = b[c+1]
        else:
            raise ValueError
            
        
        
        