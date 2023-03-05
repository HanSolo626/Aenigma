from PIL import Image

class ImageLibrary():
    def __init__(self) -> None:
        self.IMAGES = {
            1:Image.open("/Users/carsonball/Desktop/aenigma_game/images/test_square.png"),
            2:Image.open("/Users/carsonball/Desktop/aenigma_game/images/orange_test.png")
        }

        self.PYGAME_IMAGES = {
            1:"/Users/carsonball/Desktop/aenigma_game/images/test_square.png",
            2:"/Users/carsonball/Desktop/aenigma_game/images/orange_test.png"
        }