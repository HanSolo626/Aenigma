import pygame
import pygame.font
import sys
import os
import os.path as path
import importlib
import inspect
from image_library import ImageLibrary

class OpenFile:
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.main_width, self.main_height = 150, 50
        self.open_width, self.open_height = 150, 50
        self.button_color = (255,255,255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont("", 40)
        self.file_font = pygame.font.SysFont("", 30)

        self.image_library = ImageLibrary()

        self.current_file = 0

        self.main_rect = pygame.Rect(0, 0, self.main_width, self.main_height)
        self.main_rect.x = 50
        self.main_rect.y = 50
        self.main_name = "Open File"

        self.open_rect = pygame.Rect(0, 0, self.open_width, self.open_height)
        self.open_rect.x = 995
        self.open_rect.y = 400
        self.open_name = "Open File"


        self.arrow_right = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.image.load(self.image_library.SYSTEM_IMAGES[5])
        self.arrow_left = pygame.transform.flip(self.arrow_left, True, False)

        self.file_list = self.filter_save_files(self.get_save_files())
        #self.file_list = self.get_save_files()

        self._prep_msg(msg)
        self.prep_open()

    def update_file_list(self):
        self.file_list = self.filter_save_files(self.get_save_files())

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.main_rect.center

    def prep_open(self):
        self.open_image = self.font.render(self.open_name, True, self.text_color, self.button_color)
        self.open_image_rect = self.open_image.get_rect()
        self.open_image_rect.center = self.open_rect.center

    def prep_words(self, words):
        words = str(words)
        image = self.file_font.render(words, True, self.text_color)
        image_rect = image.get_rect()
        image_rect.x = 1000
        image_rect.y = 250
        return image, image_rect
    
    def draw_open(self):
        self.screen.fill(self.button_color, self.open_rect)
        self.screen.blit(self.open_image, self.open_image_rect)

    def draw_file(self):
        if self.current_file < 0:
            self.current_file = self.file_list.__len__()-1
        elif self.current_file > self.file_list.__len__()-1:
            self.current_file = 0
        self.screen.blit(self.prep_words(self.file_list[self.current_file])[0], self.prep_words(self.current_file)[1])
        

    def draw_main(self):
        self.screen.fill(self.button_color, self.main_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_all(self):
        self.draw_main()
        self.draw_selection_buttons(self.arrow_left, self.arrow_right)
        self.draw_file()
        self.draw_open()

    def draw_selection_buttons(self, right, left):
        self.rect_right = right.get_rect()
        self.rect_right.x = 1015
        self.rect_right.y = 300
        self.rect_left = left.get_rect()
        self.rect_left.x = 1095
        self.rect_left.y = 300

        self.screen.blit(right, self.rect_right)
        self.screen.blit(left, self.rect_left)


    def get_save_files(self):
        filelist = os.listdir("saves")
        try:
            filelist.remove("__pycache__")
            if filelist == []:
                return ["No saves found."]
            else:
                return filelist
        except ValueError:
            return ["Error: Pycache not found!"]
        
    def import_map(self, file):
        module = importlib.import_module(file)
        return module

    def filter_save_files(self, file_list):
        i = file_list.__len__()-1
        for c in range(i):
            try:
                if not path.splitext(file_list[c])[1] == ".py":
                    file_list.remove(file_list[c])
            except IndexError:
                file_list = ["Error: Bad Files"]
        return file_list

