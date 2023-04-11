from PIL import Image
import sys

sys.path.append('/Users/carsonball/Desktop/aenigma_game/images')

class ImageLibrary():
    def __init__(self) -> None:
        self.IMAGES = {
            1:Image.open("images/terrain_images/test_square.png"),
            2:Image.open("images/terrain_images/orange_test.png"),
            3:Image.open("images/terrain_images/detailed_grass.png")
        }

        self.PYGAME_IMAGES = {
            1:"images/terrain_images/test_square.png",
            2:"images/terrain_images/orange_test.png",
            3:"images/terrain_images/detailed_grass.png"
        }

        self.SYSTEM_IMAGES = {
            1:"images/system_images/drag_area.png",
            2:"images/system_images/zoom_image.png",
            3:"images/system_images/zoom_in_plus.png",
            4:"images/system_images/zoom_out_minus.png",
            5:"images/system_images/arrow.png",
            6:"images/system_images/default.png",
            7:"images/system_images/marker.png"
        }