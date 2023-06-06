import pygame
from image_library import ImageLibrary

class AccessControl():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image_library = ImageLibrary()

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 40)

        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 500
        self.main_name = "Access"

        self.prep_main(msg)

    def prep_main(self, msg):
        self.main_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = self.main_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.main_image, self.main_image_rect)

    def draw_selection_buttons(self, right, left):
        self.rect_right = right.get_rect()
        self.rect_right.x = 1015
        self.rect_right.y = 300
        self.rect_left = left.get_rect()
        self.rect_left.x = 1095
        self.rect_left.y = 300

        self.screen.blit(right, self.rect_right)
        self.screen.blit(left, self.rect_left)

    def draw_all(self):
        self.draw_main()
        self.draw_selection_buttons(self.arrow_left, self.arrow_right)

    def extract_access_map(self, map):
        """Returns a GIANT dictionary that represents the access map."""
        a = []
        b = {}
        size = map.size_x
        base = map.base_access
        base_vision = map.base_vision
        access = map.access_map

        c = [base, base_vision]

        for x in range(size*12):
            a.append(c)
        for y in range(size*12):
            b[y+1] = a.copy()

        for d in range(access.__len__()-1):
            b = self.paint_rect(b, access[d])

        return b

    def paint_rect(self, map, data):
        x, y = data[0]
        type = data[1]
        size = data[2]
        V_H = data[3]
        a = size
        if x < 0 or y < 0:
            return map
        else:
            if size == 1:
                map[y+1][x] = [type, V_H]
            else:
                for v in range(a):
                    for h in range(a):
                        try:
                            map[(y+1)-v][x+h] = [type, V_H]
                        except KeyError:
                            map[y+1][x+h] = [type, V_H]
            return map

        
