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

        self.main_width, self.main_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont("", 40)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 210
        self.main_name = "Terrain"

        self.marker_image = pygame.image.load(self.image_library.SYSTEM_IMAGES[7])

        self._prep_msg(msg)
        self.prep_marker()

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.main_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def prep_marker(self):
        self.marker_rect = self.marker_image.get_rect()
        self.marker_rect.x = 250
        self.marker_rect.y = 50

    def draw_marker(self):
        self.screen.blit(self.marker_image, self.marker_rect)

    def draw_all(self):
        self.draw_main()
        self.draw_marker()

    def paint_terrain(self, map, x, y, size, type):
        spot = map[y+1][x]
        image = self.pick_terrain.load_selected_terrain()
        image_rect = image.get_rect()
        
        
        
