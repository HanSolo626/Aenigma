import pygame, sys


class Revolution:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((1680, 1050), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption("Revolution")

        self.fpsClock = pygame.time.Clock()



    def check_main_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update_screen(self):
        pygame.display.flip()
        self.fpsClock.tick(60)

    def run_program(self):
        while True:
            self.check_main_events()

            self.screen.fill((0,150,0))
            self.update_screen()

            

if __name__ == "__main__":
    ai = Revolution()
    ai.run_program()