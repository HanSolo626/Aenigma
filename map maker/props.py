import pygame.font
import pygame, math
from image_library import ImageLibrary
from FacillimumLibrary import Facillimum_Library


class Props():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.FL = Facillimum_Library(self.screen)

        self.image_library = ImageLibrary()

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 40)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 280
        self.main_name = "Props"

        self.eraser_width, self.eraser_height = 150, 50
        self.eraser_rect = pygame.Rect(0,0, self.eraser_width, self.eraser_height)
        self.eraser_rect.x = 1000
        self.eraser_rect.y = 600

        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)


        self.current_displayed_prop = 0
        self.current_category = str
        self.category_keys = []
        self.categories = {}
        self.prop_keys = []
        self.prop_list_position = 0

        self.eraser_on = False


        self.category_keys_length = self.category_keys.__len__()
        

        self.prop_list = {
        # number:["name", "type", img num, shadow num, effect access?, number, shadow offset]
            0:["Zero", "Test", 0, 0, False, 0, (5, 0)],
            17:["Star", "Test", 1, 0, True, 17, (300, 2300)],
            4:["Logout", "Test", 2, 0, False, 4, (0, 0)]
        }


        self._prep_msg(msg)
        self._prep_eraser()
        self.prep_prop_list_and_categories(self.prop_list)



    def prep_prop_list_and_categories(self, props: dict):
        """Prep the prop lsit for the program."""

        # Prepare prop list
        m = {}
        for number in props:
            c = props[number]
            # number:["name", "type", img, shadow, portrait, effect access?, number, zoom: tuple, zoom_sh: tuple, dimensions: tuple]
            m[number] = [
                c[0],
                c[1],
                self.image_library.PROP_IMAGES[c[2]],
                self.image_library.SHADOW_IMAGES[c[3]],
                self.image_library.PROP_PORTRAITS[c[2]],
                c[4],
                c[5],
                self.image_library.get_zoom_difference(self.image_library.PROP_IMAGES[c[2]][0]), # 7
                self.image_library.get_zoom_difference(self.image_library.PROP_IMAGES[c[3]][0]), # 8 shadow
                self.get_prop_dimensions(self.image_library.PROP_IMAGES[c[2]][0]), # 9
                c[6], # 10
            ]
            
        self.prop_list = m
        self.PROP_LIST = m


        # Find keys
        for v in props:
            b = props[v]
            if b[1] not in self.category_keys:
                self.category_keys.append(b[1])

        # Prep categories
        for key in self.category_keys:
            a = {}
            for p in props:
                b = props[p]
                if b[1] == key:
                    a[p] = self.prop_list[p]
            self.categories[key] = a

        # Finalizing
        self.current_category = "Test"
        self.current_displayed_prop = 17
        self.length = self.get_prop_list_length(self.categories[self.current_category])


    def place_prop(self, prop_instance, coordinates, map_size):
        
        if not coordinates[0]-1 < 0 and not coordinates[1]-1 < 0 and not coordinates[0]-1 > map_size and not coordinates[1]-1 > map_size:

            if not [(coordinates[0]-1, coordinates[1]-1), self.current_displayed_prop] in prop_instance:
                prop_instance.append([(coordinates[0]-1, coordinates[1]-1), self.current_displayed_prop])
                prop_instance = self.sort_props(prop_instance)
                
        return prop_instance
    
    def erase_prop(self, prop_instance, coordinates):

        if [(coordinates[0]-1, coordinates[1]-1), self.current_displayed_prop] in prop_instance:
            prop_instance.remove([(coordinates[0]-1, coordinates[1]-1), self.current_displayed_prop])
            prop_instance = self.sort_props(prop_instance)

        return prop_instance
    

    def category_up(self):
        current = self.category_keys.index(self.current_category)
        try:
            self.current_category = self.category_keys[current+1]
        except:
            self.current_category = self.category_keys[0]
        self.prop_keys = self.get_prop_keys()
        self.current_displayed_prop = self.prop_keys[0]
        self.prop_list_position = 0
        self.length = self.get_prop_list_length(self.categories[self.current_category])
        

    def category_down(self):
        current = self.category_keys.index(self.current_category)
        try:
            self.current_category = self.category_keys[current-1]
        except:
            self.current_category = self.category_keys[self.category_keys_length]
        self.prop_keys = self.get_prop_keys()
        self.current_displayed_prop = self.prop_keys[0]
        self.prop_list_position = 0
        self.length = self.get_prop_list_length(self.categories[self.current_category])

 
    def prop_up(self):
        #self.length = self.get_prop_list_length(self.categories[self.current_category])
        a = self.get_prop_keys()
        #try:
        #    self.current_displayed_prop = self.categories[self.current_category][a[self.length+1]][6]
        #except:
        #    self.length = 0
        #   self.current_displayed_prop = self.categories[self.current_category][a[0]][6]

        if (self.length+1) > self.get_prop_list_length(self.categories[self.current_category]):
            self.length = 0
            self.current_displayed_prop = self.categories[self.current_category][a[self.length]][6]
        else:
            self.length +=1
            self.current_displayed_prop = self.categories[self.current_category][a[self.length]][6]


        
    def prop_down(self):
        a = self.get_prop_keys()
            
        if (self.length-1) < 0:
            self.length = self.get_prop_list_length(self.categories[self.current_category])
            self.current_displayed_prop = self.categories[self.current_category][a[self.length]][6]
        else:
            self.length -= 1
            self.current_displayed_prop = self.categories[self.current_category][a[self.length]][6]


    def on_off_eraser(self):
        if self.eraser_on:
            self.eraser_on = False
        else:
            self.eraser_on = True


    def get_props(self, prop_list, coordinates, get_map_size):
        good_props = []
        if get_map_size % 2:
            pass
        else:
            get_map_size += 1
        get_map_size /= 2
        

        get_map_size += 3
        for prop in prop_list:
            a = prop[0] 
            for n in range(a.__len__()):
                t = a[n]
                one = abs(t[0] - coordinates[0])
                two = abs(t[1] - coordinates[1])
                if one <= get_map_size and two <= get_map_size:
                    good_props.append(prop)
                    break

        return good_props


    def get_prop_coordinates(self, prop_list: list):
        k = []
        for prop in prop_list:
            a = prop[0]
            b = prop[1]
            c = []
            dimensions = self.prop_list[b][9]
            for y in range(dimensions[1]):
                for x in range(dimensions[0]):
                    c.append((a[0] + x, a[1] - y))
            k.append([c, b])
        return k
    
    def get_prop_num_x(self, e):
        return e[0][0]
    
    def get_prop_num_y(self, e):
        return e[0][1]
    
    def sort_props(self, prop_list: list):
        a = []
        b = []
        for y in range(0, 199):
            for prop in prop_list:
                if prop[0][1] == y:
                    a.append(prop)
            a.sort(key=self.get_prop_num_x)
            for prop in a:
                b.append(prop)
            a.clear()
        return b


    def get_prop_dimensions(self, image: pygame.Surface):
        a = image.get_size()
        b = math.ceil(a[0] / 60) + 3
        c = math.ceil(a[1] / 60) + 3
        return (b, c)


    def get_prop_list_length(self, list: list):
        return list.__len__() - 1
    
    def get_prop_keys(self):
        return list(self.categories[self.current_category].keys())



    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.main_rect.center

    def _prep_eraser(self):
        self.eraser_image = self.font.render("Eraser", True, self.text_color, self.button_color)
        self.eraser_image_rect = self.eraser_image.get_rect()
        self.eraser_image_rect.center = self.eraser_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_eraser(self):
        self.screen.fill(self.button_color, self.eraser_rect)
        self.screen.blit(self.eraser_image, self.eraser_image_rect)

    def draw_portrait(self):
        a = self.categories[self.current_category][self.current_displayed_prop][4]
        self.screen.blit(a[0], a[1])

    def draw_type_selection_buttons(self, right, left):
        self.rect_right_key = right.get_rect()
        self.rect_right_key.x = 1015
        self.rect_right_key.y = 190
        self.rect_left_key = left.get_rect()
        self.rect_left_key.x = 1095
        self.rect_left_key.y = 190
    
        self.screen.blit(right, self.rect_right_key)
        self.screen.blit(left, self.rect_left_key)

    def draw_selection_buttons(self, right, left):
        self.rect_right_prop = right.get_rect()
        self.rect_right_prop.x = 1015
        self.rect_right_prop.y = 400
        self.rect_left_prop = left.get_rect()
        self.rect_left_prop.x = 1095
        self.rect_left_prop.y = 400

        self.screen.blit(right, self.rect_right_prop)
        self.screen.blit(left, self.rect_left_prop)

    def draw_all(self):
        self.draw_main()
        self.draw_eraser()
        self.draw_selection_buttons(self.arrow_left, self.arrow_right)
        self.draw_type_selection_buttons(self.arrow_left, self.arrow_right)
        self.FL.draw_words(self.current_category, 30, (1015, 150), False, "black") # type: ignore
        self.FL.draw_words(self.prop_list[self.current_displayed_prop][0], 30, (1015, 375), False, "black") # type: ignore
        self.FL.draw_words(str(self.eraser_on), 30, (1050, 550), False, "black")
        self.draw_portrait()