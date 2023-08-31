# This python library was written by Carson J. Ball

import pygame, multiprocessing

class Facillimum_Library():
    """A library of python functions that make it easier to make stuff with pygame."""

    def __init__(self, screen) -> None:
        pygame.init()

        if type(screen) == pygame.Surface:
            self.screen = screen
        else:
            raise ValueError("Your screen must be a pygame Surface object!")
        
        self.color_list = {
            "white":(255,255,255),
            "black":(0,0,0),
            "red":(255,0,0),
            "green":(0,255,0),
            "blue":(0,0,255),
            "yellow":(255,255,0),
            "purple":(255,0,255),
            "cyan":(0,255,255)
        }

        self.rendered_words = {}


    def draw_image(
            self,
            image: pygame.Surface,
            coordinates: tuple
            ):
        """This function will draw a pygame Surface object at the inputed x and y coordinates onto the window."""
        if type(image) == pygame.Surface:
            if type(coordinates) == tuple:
                rect = image.get_rect()
                rect.x = coordinates[0]
                rect.y = coordinates[1]
                self.screen.blit(image, rect)
            else:
                raise ValueError("Second argument must be a tuple with two intergers.")
        else:
            raise ValueError("First argument must a pygame Surface.")
        

    def load_image(self,
            file_path: str
        ):
        """Returns a pygame Surface object by loading up the given file path. Note that the file must be a BMP or PNG image."""
        try:
            return pygame.image.load(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("File was not found!")
        

    def prep_color_zero(self):
        """IGNORE THIS"""
        font = pygame.font.SysFont("", 15)
        self.zero_image = font.render("0", True, (0,0,0))
        
    
    def draw_words(self,
            words: str,
            size: int,
            coordinates: tuple,
            shadow: bool,
            color
            ):
        """This function will draw words onto the screen at whatever size, position, and color you want!"""
        if type(color) == str:
            try:
                color = self.color_list[color]
            except KeyError:
                raise ValueError("'"+color+"' not found in color list.\nColor List:\n"+str(self.color_list.keys()))
        elif type(color) == tuple:
            pass
        else:
            raise ValueError("Fourth argument must be a string or a tuple: (int, int, int).")
        
        try:
            if (words+str(size)) in self.rendered_words:
                image = self.rendered_words[(words+str(size))]
            else:
                font = pygame.font.SysFont("", size)
                self.rendered_words[(words+str(size))] = font.render(words, True, color)
                image = self.rendered_words[(words+str(size))]

            if shadow:
                shadow = font.render(words, True, (0,0,0)) # type: ignore
                self.draw_image(shadow, (coordinates[0]+3, coordinates[1]+3)) # type: ignore
        except ValueError:
            raise ValueError("You can only pass in a tuple that has at least three intergers and that none of them are negative or are above 255.")
        self.draw_image(image, coordinates)

    def draw_words_access_zero(self,
            words: str,
            size: int,
            coordinates: tuple,
            shadow: bool,
            color
            ):
        
        if type(color) == str:
            try:
                color = self.color_list[color]
            except KeyError:
                raise ValueError("'"+color+"' not found in color list.\nColor List:\n"+str(self.color_list.keys()))
        elif type(color) == tuple:
            pass
        else:
            raise ValueError("Fourth argument must be a string or a tuple: (int, int, int).")
        
        #font = pygame.font.SysFont("", size)
        try:
            #image = font.render(words, True, color)
            image = self.zero_image
            if shadow:
                shadow = font.render(words, True, (0,0,0)) # type: ignore
                self.draw_image(shadow, (coordinates[0]+3, coordinates[1]+3)) # type: ignore
        except ValueError:
            raise ValueError("You can only pass in a tuple that has at least three intergers and that none of them are negative or are above 255.")
        self.draw_image(image, coordinates)


    def paint_screen(self,
            color
            ):
        """This function will paint the entire screen with the given color."""
        if type(color) == str:
            try:
                color = self.color_list[color]
            except KeyError:
                raise ValueError("'"+color+"' not found in color list.\nColor List:\n"+str(self.color_list.keys()))
        elif type(color) == tuple:
            pass
        else:
            raise ValueError("First argument must be a string or a tuple: (int, int, int).")
        self.screen.fill(color)


    def open_text_box(self,
                      size: int,
                      coordinates: tuple,
                      color):
        """Returns a string from the keyboard. Note that everything will freeze until the text box is closed."""
        if type(color) == str:
            try:
                color = self.color_list[color]
            except KeyError:
                raise ValueError("'"+color+"' not found in color list.\nColor List:\n"+str(self.color_list.keys()))
        elif type(color) == tuple:
            pass
        else:
            raise ValueError("Third argument must be a string or a tuple: (int, int, int).")
        a = ""
        b = True
        c = 0
        d = True
        while b:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if not a.__len__() > 999999999:
                        if event.key == pygame.K_RETURN:
                            #if not d:
                            #    a = a.removesuffix(a[a.__len__()-1])
                            if not a.__eq__(""):
                                if not a.__eq__("|"):
                                    if a[a.__len__()-1].__eq__("|"):
                                        a = a.removesuffix(a[a.__len__()-1])
                                    return str.strip(str(a))
                            #a = a.removesuffix(a[a.__len__()-1])

                        elif event.key == pygame.K_BACKSPACE:
                            if not d:
                                a = a.removesuffix(a[a.__len__()-1])
                            try:
                                a = a.removesuffix(a[a.__len__()-1])
                                c = 0
                                d = True
                            except IndexError:
                                a = ''
                                c = 0
                                d = True
                        elif not a.__len__() > 12:
                            c = 0
                            if not d:
                                a = a.removesuffix(a[a.__len__()-1])
                                d = True
                            a += event.unicode
            self.draw_rect((400, size+14), (coordinates[0]-7,coordinates[1]-12), (50,50,50))
            if c == 100:
                if d:
                    d = False
                    a += "|"
                else:
                    d = True
                    a = a.removesuffix(a[a.__len__()-1])
                c = 0
            self.draw_words(str(a), size, coordinates, False, color)
            self.update(1)
            c+=1
    

    def draw_rect(self,
                  dimensions: tuple,
                  coordinates: tuple,
                  color):
        """Draws a rectangle at the passed in coordiates with the passed in dimensions and color."""
        if type(color) == str:
            try:
                color = self.color_list[color]
            except KeyError:
                raise ValueError("'"+color+"' not found in color list.\nColor List:\n"+str(self.color_list.keys()))
        elif type(color) == tuple:
            pass
        else:
            raise ValueError("Third argument must be a string or a tuple: (int, int, int).")
        rect = pygame.Rect(0,0, dimensions[0], dimensions[1])
        rect.x = coordinates[0]
        rect.y = coordinates[1]
        self.screen.fill(color, rect)



    def update(self,
               *time
               ):
        """This function will update the screen with the latest graphics and add a delay in miliseconds if any is given."""
        pygame.display.flip()
        try:
            pygame.time.delay(time) # type: ignore
        except TypeError:
            pass
