import pygame.font
import pygame
from image_library import ImageLibrary
from create_file import PickTerrain

class Terrain():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image_library = ImageLibrary()
        self.pick_terrain = PickTerrain(self, "")

        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont("", 40)
        self.big_font = pygame.font.SysFont("", 60)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 210
        self.main_name = "Terrain"

        self.size_rect = pygame.Rect(0, 0, 150, 30)
        self.size_rect.x = 1000
        self.size_rect.y = 450
        self.size_name = "Brush Size"

        self.brush_size = 1

        self.prep_size()
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.main_rect.center

    def prep_size(self):
        self.size_image = self.font.render(self.size_name, True, self.text_color, self.button_color)
        self.size_image_rect = self.size_image.get_rect()
        self.size_image_rect.center = self.size_rect.center

    def prep_words(self, words):
        self.words_image = self.big_font.render(str(words), True, self.text_color)
        self.words_image_rect = self.words_image.get_rect()
        self.words_image_rect.x = 1060
        self.words_image_rect.y = 400
        
        

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_size(self):
        self.screen.fill(self.button_color, self.size_rect)
        self.screen.blit(self.size_image, self.size_image_rect)

    def draw_selection_buttons(self, right, left):
        self.rect_right = right.get_rect()
        self.rect_right.x = 1015
        self.rect_right.y = 500
        self.rect_left = left.get_rect()
        self.rect_left.x = 1095
        self.rect_left.y = 500

        self.screen.blit(right, self.rect_right)
        self.screen.blit(left, self.rect_left)

    def draw_words(self, words):
        self.prep_words(words)
        self.screen.blit(self.words_image, self.words_image_rect)

    def draw_all(self):
        self.draw_main()
        self.draw_size()
        self.draw_selection_buttons(self.arrow_left, self.arrow_right)
        self.draw_words(self.brush_size)

    def increase_brush(self):
        if not self.brush_size == 10:
            self.brush_size +=1

    def decrease_brush(self):
        if not self.brush_size == 1:
            self.brush_size -= 1

    def paint_terrain(self, map, x, y, size, type):
        a = size
        c= 0
        l = 0
        if x < 0 or y < 0:
            return map
        else:
            if size == 1:
                try:
                    map[y+1][x] = type
                except IndexError:
                    pass
            else:
                for v in range(a):
                    for h in range(a):
                        try:
                            c = map[(y+1)-v]
                            try:
                                c[x+h] = type
                            except IndexError:
                                pass
                        except KeyError:
                            try:
                                l = map[y+1]
                                try:
                                    l[x+h] = type
                                except IndexError:
                                    pass
                            except KeyError:
                                pass
            return map
        
        
        