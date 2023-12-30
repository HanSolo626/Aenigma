import pygame, sys, math, time
import pygame.font

sys.path.append('saves')
sys.path.append('map maker')


from FacillimumLibrary import Facillimum_Library
from image_library import ImageLibrary



class PropMaker:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((500,300), pygame.RESIZABLE)

        pygame.display.set_caption("Aenigma Prop Maker")

        # get FL
        self.FL = Facillimum_Library(self.screen)

        # get images
        self.image_library = ImageLibrary()

        pygame.display.set_icon(self.image_library.load_image(self.image_library.SYSTEM_IMAGES[9])[0])



    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()


    def draw_all(self):
        self.screen.fill((50,50,50))



    def run_program(self):
        while True:

            self.check_events()

            self.draw_all()
            pygame.display.update()





if __name__ == '__main__':
    ai = PropMaker()
    ai.run_program()