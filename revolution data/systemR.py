import pygame
import pygame.font
import sys
import time
from image_libraryR import ImageLibrary

class QuitProgram():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_width, self.main_height = 100, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font =  pygame.font.SysFont("", 30)

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

        self.image_library = ImageLibrary()

        self.image = pygame.image.load(self.image_library.SYSTEM_IMAGES[1])
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

        self.image_library = ImageLibrary()

        self.zoom_main_image = pygame.image.load(self.image_library.SYSTEM_IMAGES[2])
        self.zoom_main_rect = self.zoom_main_image.get_rect()
        self.zoom_in_image = pygame.image.load(self.image_library.SYSTEM_IMAGES[3])
        self.zoom_in_rect = self.zoom_in_image.get_rect()
        self.zoom_out_image = pygame.image.load(self.image_library.SYSTEM_IMAGES[4])
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

class GeneralInfo():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.button_color = (40,40,40)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont("", 25, False, False)

        self.main_rect = pygame.Rect(0, 0, 700, 30)
        self.main_rect.x = 250
        self.main_rect.y = 760

    def print_m(self, message):
        self.screen.fill(self.button_color, self.main_rect)
        self.main_image = self.font.render(message, True, self.text_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.x = 252
        self.main_image_rect.y = 765

        self.screen.blit(self.main_image, self.main_image_rect)

class SaveFile():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont("", 25, False, False)

        self.red_color = (255,0,0)

        self.main_rect = pygame.Rect(0, 0, 60, 30)
        self.main_rect.x = 900
        self.main_rect.y = 7
        self.main_name = "Save"

        self.red_rect = pygame.Rect(0,0, 10,10)
        self.red_rect.x = 970
        self.red_rect.y = 17

        self.changes_made = False

        self.prep_main(self.main_name)

    def prep_main(self, msg):
        self.main_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = self.main_rect.center

    def draw_all(self):
        self.draw_save()
        if self.changes_made:
            self.draw_red_dot()

    def draw_dot(self):
        self.draw_red_dot()

    def draw_save(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.main_image, self.main_image_rect)

    def draw_red_dot(self):
        self.screen.fill(self.red_color, self.red_rect)



class UndoRedo():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image_library = ImageLibrary()

        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont("", 25, False, False)

        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.undo_name = "Undo"
        self.redo_name = "Redo"

        self.terrain_history = []
        self.prop_history = []
        self.object_history = []
        self.sound_history = []

        self.prep_undo(self.undo_name)
        self.prep_redo(self.redo_name)

    def prep_undo(self, name):
        self.undo_rect = self.arrow_left.get_rect()
        self.undo_rect.x = 420
        self.undo_rect.y = 10
        self.undo_image = self.font.render(name, True, self.text_color)
        self.undo_image_rect = self.undo_image.get_rect()
        self.undo_image_rect.x = self.undo_rect.x - 50
        self.undo_image_rect.y = self.undo_rect.y

    def prep_redo(self, name):
        self.redo_rect = self.arrow_right.get_rect()
        self.redo_rect.x = 480
        self.redo_rect.y = 10
        self.redo_image = self.font.render(name, True, self.text_color)
        self.redo_image_rect = self.redo_image.get_rect()
        self.redo_image_rect.x = self.redo_rect.x + 40
        self.redo_image_rect.y = self.redo_rect.y

    def draw_undo_redo(self):
        self.screen.blit(self.arrow_left, self.undo_rect)
        self.screen.blit(self.undo_image, self.undo_image_rect)

        self.screen.blit(self.arrow_right, self.redo_rect)
        self.screen.blit(self.redo_image, self.redo_image_rect)

    def add_to_terrain_history(self, history):
        self.terrain_history.append(dict.copy(history))

class PositionDisplay():
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont("", 25)
        self.position_position_x = 370
        self.position_position_y = 10
        self.mouse_position_x = 370
        self.mouse_position_y = 30

    def draw_position(self, pos, mouse):
        a = self.font.render("Position = "+str(pos[0])+", "+str(pos[1]), False, self.text_color)
        b = self.font.render("Mouse = "+str(mouse[0])+", "+str(mouse[1]), False, self.text_color)
        a_rect = a.get_rect()
        b_rect = b.get_rect()
        a_rect.x = self.position_position_x
        a_rect.y = self.position_position_y
        b_rect.x = self.mouse_position_x
        b_rect.y = self.mouse_position_y
        self.screen.blit(a, a_rect)
        self.screen.blit(b, b_rect)