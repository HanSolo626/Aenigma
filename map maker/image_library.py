
import sys
import pygame
import os

sys.path.append('aenigma_game/images')

class ImageLibrary():
    def __init__(self) -> None:

        terrain_images = self.get_terrain_images()

        self.PYGAME_IMAGES = {
            1:"images/terrain_images/test_square.png",
            2:"images/terrain_images/orange_test.png",
            3:"images/terrain_images/detailed_grass.png",
            4:"images/terrain_images/dark_square.png"
        }


        self.SYSTEM_IMAGES = {
            1:"images/system_images/drag_area.png",
            2:"images/system_images/zoom_image.png",
            3:"images/system_images/zoom_in_plus.png",
            4:"images/system_images/zoom_out_minus.png",
            5:"images/system_images/arrow.png",
            6:"images/system_images/default.png",
            7:"images/system_images/marker.png",
            8:"images/system_images/test_mouse.png"
        }

        self.PRELOADED_IMAGES = {}
        self.PRELOADED_IMAGES[0] = [terrain_images[1], terrain_images[1].get_rect()]

        for c in range(terrain_images[0].__len__()):
            self.PRELOADED_IMAGES[self.get_terrain_code(self.folderlist[c])] = [terrain_images[0][c-1], terrain_images[0][c-1].get_rect()]

        print(self.PRELOADED_IMAGES)

        

        self.ZOOM_MOUSE_NUMBERS = {
            20:2,
            19:1,
            18:2,
            17:1,
            16:1,
            15:0,
            14:0,
            13:-1,
            12:0,
            11:-2,
            10:-2,
            9:-3,
            8:-4,
            7:-6,
            6:-7,
            5:-11,
            4:-14,
            3:-21,
            2:-33
        }

    def get_terrain_images(self):
        """Returns a list of all 60x60 px. images along with the dark square."""

        self.folderlist = os.listdir("images/terrain_images")
        c = pygame.image.load("images/terrain_images/dark_square.png")
        self.folderlist.remove("dark_square.png")
        b = []
        for v in range(self.folderlist.__len__()):
            a = pygame.image.load("images/terrain_images/"+self.folderlist[v])
            if a.get_size() == (60, 60):
                b.append(a)
        return (b, c)
    
    def get_terrain_code(self, string_name: str):
        """Returns an interger code for the string name."""
        a = 0
        for g in range(string_name.__len__()):
            a += ord(string_name[g])
        return a