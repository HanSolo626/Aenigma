import pygame
import pygame.font
import sys
import time

class QuitProgram():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_width, self.main_height = 100, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont(None, 30)

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 700
        self.main_name = "Quit"

        self.prep_main(msg)

    def prep_main(self, msg):
        self.main_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = self.main_rect.center

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.main_image, self.main_image_rect)

    def quit_program(self):
        # will eventually put save check here
        sys.exit()


class DragMap():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/drag_area.png')
        self.rect = self.image.get_rect()

        self.rect.x = 250
        self.rect.y = 50

    def draw_drag_area(self):
        self.screen.blit(self.image, self.rect)

    def drag_map_by_mouse(self, mouse_pos, multi):
        old_mouse_pos_x, old_mouse_pos_y = mouse_pos[0], mouse_pos[1]
        time.sleep(0.001)
        mouse_pos = pygame.mouse.get_pos()
        new_pos_x = old_mouse_pos_x - mouse_pos[0]
        new_pos_y = old_mouse_pos_y - mouse_pos[1]
        new_pos_x = new_pos_x * multi
        new_pos_y = new_pos_y * multi
        return new_pos_x, new_pos_y

    def speed_move(self):
        multiplyer = 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.KMOD_SHIFT:
                    if event.key == pygame.K_z:
                        multiplyer = multiplyer * 4
                        print("4")
                    else:
                        multiplyer = multiplyer * 2
                        print("2")
        print(multiplyer)
        return multiplyer

class AjustSize():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.zoom_main_image = pygame.image.load('images/zoom_image.png')
        self.zoom_main_rect = self.zoom_main_image.get_rect()
        self.zoom_in_image = pygame.image.load('images/zoom_in_plus.png')
        self.zoom_in_rect = self.zoom_in_image.get_rect()
        self.zoom_out_image = pygame.image.load('images/zoom_out_minus.png')
        self.zoom_out_rect = self.zoom_out_image.get_rect()

        self.zoom_main_rect.x = 790
        self.zoom_main_rect.y = 10
        self.zoom_in_rect.x = 750
        self.zoom_in_rect.y = 10
        self.zoom_out_rect.x = 830
        self.zoom_out_rect.y = 10


    def draw_main(self):
        self.screen.blit(self.zoom_main_image, self.zoom_main_rect)

    def draw_out(self):
        self.screen.blit(self.zoom_out_image, self.zoom_out_rect)

    def draw_in(self):
        self.screen.blit(self.zoom_in_image, self.zoom_in_rect)

    def draw_all_zoom(self):
        self.draw_main()
        self.draw_in()
        self.draw_out()

    def zoom_map_out(self, map):
        new_map = pygame.transform.scale(map, (100, 100))
        print("out")
        return new_map
    
    def zoom_map_in(self, map):
        new_map = pygame.transform.scale(map, (200, 200))
        print("in")
        return new_map



