import pygame, sys
import os.path as path
from map_makerREVOLUTION import MapMaker

class Revolution:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((1680, 1050), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption("Revolution")

        self.mpm = MapMaker(False, self.screen)

        self.fpsClock = pygame.time.Clock()

        self.mpm.current_file_open = path.splitext(self.mpm.open_file.file_list[self.mpm.open_file.current_file])[0]

        self.mpm.screen_map_size = 1680
        self.mpm.map_present = True



    def check_main_events(self):
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        sys.exit()
        
        self.mpm.check_events()


    

    def update_screen(self):
        pygame.display.flip()
        self.fpsClock.tick(60)


    def run_program(self):

        self.mpm.import_map(self.mpm.current_file_open)

        while True:
            self.check_main_events()
            self.screen.fill((0,0,150))
            self.mpm.draw_world(self.mpm.map_data_instance, self.mpm.camera_x, self.mpm.camera_y)


            self.update_screen()

            

if __name__ == "__main__":
    ai = Revolution()
    ai.run_program()