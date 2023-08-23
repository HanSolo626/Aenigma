import pygame
from image_library import ImageLibrary
from FacillimumLibrary import Facillimum_Library

class AccessControl():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image_library = ImageLibrary()
        self.FL = Facillimum_Library(self.screen)

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 40)
        self.big_font = pygame.font.SysFont("", 60)

        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 500
        self.main_name = "Access"

        self.size_rect = pygame.Rect(0, 0, 150, 30)
        self.size_rect.x = 1000
        self.size_rect.y = 450
        self.size_name = "Brush Size"

        self.v_h_rect = pygame.Rect(0,0, 75, 50)
        self.v_h_rect.x = 1035
        self.v_h_rect.y = 570
        self.v_h_name = "V_H"

        self.current_selected_access_number = 1
        self.current_access_image = self.load_access_tile()
        self.brush_size = 1
        self.v_h = 0
        self.current_displayed_v_h = 0

        self.access_type_list = {
            0:"None",
            1:"Land",
            2:"Water",
            3:"All"
        }

        self.prep_main(msg)
        self.prep_size()
        self.prep_v_h()

    def prep_main(self, msg):
        self.main_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = self.main_rect.center

    def prep_size(self):
        self.size_image = self.font.render(self.size_name, True, self.text_color, self.button_color)
        self.size_image_rect = self.size_image.get_rect()
        self.size_image_rect.center = self.size_rect.center

    def prep_v_h(self):
        self.v_h_image = self.font.render(self.v_h_name, True, self.text_color, self.button_color)
        self.v_h_image_rect = self.v_h_image.get_rect()
        self.v_h_image_rect.center = self.v_h_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.main_image, self.main_image_rect)

    def draw_size(self):
        self.screen.fill(self.button_color, self.size_rect)
        self.screen.blit(self.size_image, self.size_image_rect)
    
    def draw_v_h(self):
        self.screen.fill(self.button_color, self.v_h_rect)
        self.screen.blit(self.v_h_image, self.v_h_image_rect)

    def prep_words(self, words):
        self.words_image = self.big_font.render(str(words), True, self.text_color)
        self.words_image_rect = self.words_image.get_rect()
        self.words_image_rect.x = 1060
        self.words_image_rect.y = 400

    def draw_words(self, words):
        self.prep_words(words)
        self.screen.blit(self.words_image, self.words_image_rect)

    def draw_selection_buttons(self, right, left):
        self.rect_right = right.get_rect()
        self.rect_right.x = 1015
        self.rect_right.y = 300
        self.rect_left = left.get_rect()
        self.rect_left.x = 1095
        self.rect_left.y = 300

        self.size_rect_right = right.get_rect()
        self.size_rect_right.x = 1015
        self.size_rect_right.y = 500
        self.size_rect_left = left.get_rect()
        self.size_rect_left.x = 1095
        self.size_rect_left.y = 500

        self.v_h_rect_right = right.get_rect()
        self.v_h_rect_right.x = 1015
        self.v_h_rect_right.y = 650
        self.v_h_rect_left = left.get_rect()
        self.v_h_rect_left.x = 1095
        self.v_h_rect_left.y = 650

        self.screen.blit(right, self.rect_right)
        self.screen.blit(left, self.rect_left)
        self.screen.blit(right, self.size_rect_right)
        self.screen.blit(left, self.size_rect_left)
        self.screen.blit(right, self.v_h_rect_right)
        self.screen.blit(left, self.v_h_rect_left)

    def alter_access_number(self, go_up):
        if go_up:
            if self.current_selected_access_number == 3:
                self.current_selected_access_number = 0
            else:
                self.current_selected_access_number += 1
        else:
            if self.current_selected_access_number == 0:
                self.current_selected_access_number = 3
            else:
                self.current_selected_access_number -= 1 

        self.current_access_image = self.load_access_tile()

    

    def draw_all(self):
        self.draw_main()
        self.draw_size()
        self.draw_v_h()
        self.draw_current_access()
        self.draw_selection_buttons(self.arrow_left, self.arrow_right)
        self.draw_words(self.brush_size)
        self.FL.draw_words(self.access_type_list[self.current_selected_access_number], 30, (1040, 150), False, "black")
        self.FL.draw_words(str(self.v_h), 40, (1065, 650), False, "black")

    def load_access_tile(self):
        return pygame.transform.scale(self.image_library.ACCESS_IMAGES[self.current_selected_access_number][0], (60, 60))
    
    def draw_current_access(self):
        image = self.current_access_image
        rect = image.get_rect()
        rect.x = 1040
        rect.y = 200
        self.screen.blit(image, rect)

    def increase_brush(self):
        if not self.brush_size == 10:
            self.brush_size +=1

    def decrease_brush(self):
        if not self.brush_size == 1:
            self.brush_size -= 1

    def increase_v_h(self):
        self.v_h += 1

    def decrease_v_h(self):
        if not self.v_h == 0:
            self.v_h -= 1

    def add_access_rect(self, map, x, y, size, type, v_h):
        a = [(x, y), type, size, v_h]
        b = True
        for rect in map:
            if a == rect:
                #print("denied")
                b = False
        if b:
            #print("accepted")
            map.append(a)

        return map



    def extract_access_map(self, map):
        """Returns a GIANT dictionary that represents the access map."""
        a = []
        b = {}
        size = map.size_x
        base = map.base_access
        base_vision = map.base_vision
        access = map.access_map

        c = [base, base_vision]

        for x in range(size*6):
            a.append(c)
        for y in range(size*6):
            b[y+1] = a.copy()

        for d in range(access.__len__()-1):
            b = self.paint_rect(b, access[d])

        return b

    def paint_rect(self, map, data):
        x, y = data[0]
        type = data[1]
        size = data[2]
        v_h = data[3]
        a = size
        if x < 0 or y < 0:
            return map
        else:
            if size == 1:
                map[y+1][x] = [type, v_h]
            else:
                for v in range(a):
                    for h in range(a):
                        try:
                            map[(y+1)-v][x+h] = [type, v_h]
                        except KeyError:
                            map[y+1][x+h] = [type, v_h]
            return map

        
