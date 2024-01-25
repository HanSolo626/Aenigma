import pygame, sys, math, time
import pygame.font

sys.path.append('saves')
sys.path.append('map maker')


from FacillimumLibrary import Facillimum_Library
from image_library import ImageLibrary
from props import Props



class PropMaker:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((600,400), pygame.RESIZABLE)

        pygame.display.set_caption("Aenigma Prop Maker")

        # get FL
        self.FL = Facillimum_Library(self.screen)

        # get images
        self.image_library = ImageLibrary()

        self.props = Props(self, "")

        pygame.display.set_icon(self.image_library.load_image(self.image_library.SYSTEM_IMAGES[9])[0])


##############################
        self.prop_num = 0
##############################



        self.img = self.props.PROP_LIST[self.prop_num][2][0]
        self.rect = self.props.PROP_LIST[self.prop_num][2][1]
        self.rect.x = 50
        self.rect.y = 70

        self.shd_x = self.props.PROP_LIST[self.prop_num][10][0]
        self.shd_y = self.props.PROP_LIST[self.prop_num][10][1]

        self.shd = pygame.transform.scale(self.props.PROP_LIST[self.prop_num][3][0], (60,30))
        self.shd_rect = self.shd.get_rect()
        self.shd_rect.x = self.rect.x + (self.shd_x / 39)
        self.shd_rect.y = self.rect.y + (self.shd_y / 39)

        # 39



    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.shd_x = self.FL.open_text_box(30, (15, 10), "black")
                    self.shd_x = int(self.shd_x) # type: ignore
                    self.shd_rect.x = self.rect.x + (self.shd_x / 39)
                if event.key == pygame.K_y:
                    self.shd_y = self.FL.open_text_box(30, (135, 10), "black")
                    self.shd_y = int(self.shd_y) # type: ignore
                    self.shd_rect.y = self.rect.y + (self.shd_y / 39)
                if event.key == pygame.K_q:
                    sys.exit()


    def draw_all(self):
        self.screen.fill((50,50,50))
        
        self.screen.blit(self.shd, self.shd_rect)
        self.screen.blit(self.img, self.rect)

        self.FL.draw_rect((pygame.Surface.get_size(self.screen)[0], 50), (0,0), (100,100,100))

        self.FL.draw_words("X: "+str(self.shd_x), 30, (10, 10), False, "black")
        self.FL.draw_words("Y: "+str(self.shd_y), 30, (130, 10), False, "black")
        



    def run_program(self):
        while True:

            self.check_events()

            self.draw_all()
            pygame.display.update()





if __name__ == '__main__':
    ai = PropMaker()
    ai.run_program()