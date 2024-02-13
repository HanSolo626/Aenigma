import pygame, sys, math, time
import pygame.font
import importlib
import os.path as path

#sys.path.append('/Users/carsonball/Desktop/aenigma_game/map maker/game_maps')
sys.path.append('saves')
sys.path.append('revolution data')

from FacillimumLibrary import Facillimum_Library


from image_libraryR import ImageLibrary
from systemR import *
from test_buttonR import *
from open_fileR import *
from create_fileR import *
from terrainR import *
from propsR import *
from objectsR import *
from soundR import *
from side_areasR import *
from accessR import *

class MapMakerRevolution:
    def __init__(self, internal: bool, screen):
        pygame.init()

        if internal:
            self.screen = pygame.display.set_mode((1200, 800), pygame.SCALED | pygame.RESIZABLE)
            #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.set_caption("Aenigma Map Maker")

            self.map_posX = 250
            self.map_posY = 50
        else:
            self.screen = screen
            self.map_posX = -60
            self.map_posY = -60
            
        self.internal = internal

        # get FL
        self.FL = Facillimum_Library(self.screen)

        # get images
        self.image_library = ImageLibrary()

        # create sides
        self.area_left = AreaLeft(self)
        self.area_right = AreaRight(self)
        self.area_up = AreaUp(self)
        self.area_down = AreaDown(self)

        # create system functions
        self.quit_program = QuitProgram(self, "Exit")
        self.drag_area = DragMap(self)
        self.ajust_size = AjustSize(self)
        self.print = GeneralInfo(self)
        self.save = SaveFile(self)
        self.position = PositionDisplay(self)

        # make folder buttons
        self.test_button = TestButton(self, "Test")
        self.open_file = OpenFile(self, "Open File")
        self.create_file = MainButton(self, "Create File")
        self.terrain = Terrain(self, "Terrain")
        self.props = Props(self, "Props")
        self.objects = Objects(self, "Objects")
        self.sound = Sound(self, "Sound")
        self.access = AccessControl(self, "Access")

        # create file buttons
        self.affirm_file = AffirmButton(self, "Build File")
        self.pick_terrain = PickTerrain(self, "Pick Terrain")

        # set icon
        pygame.display.set_icon(self.image_library.load_image(self.image_library.SYSTEM_IMAGES[9])[0])


        self.PYGAME_IMAGES = self.image_library.PYGAME_IMAGES

        self.square_x = 60
        self.square_y = 60

        self.square_zoom_x = 10
        self.square_zoom_y = 10

        self.shift_x = 30
        self.shift_y = 230

        self.camera_x = 0
        self.camera_y = 0

        ##########
        self.screen_map_size = 780
        ##########

        self.mouse_drag_multiplyer = 1
        #self.mouse_drag_multiplyer = 0.2

        self.display_offset_x = 0.0
        self.display_offset_y = 0.0


        self.multiplyer_status = False

        self.screen_rect = self.screen.get_rect()

        self.speed_text_color = (0,0,0)
        self.speed_font = pygame.font.SysFont("", 25)

        self.map_present = False
        self.current_file_open = ''
        self.user_text = ''
        self.text_file_limit = 15
        self.text_in_stuff = False
        self.past_mode = "Open"
        self.current_tool = "Open"
        self.access_map_display_active = False

        self.current_message = "Welcome to the Aenigma Map Maker!"
        self.saved_text = 'new'

        self.displayed_map = {}
        self.displayed_access_map = {}
        self.current_size = 60 # NOTE
        self.access_control_size = 10
        self.move_x = 0
        self.move_y = 0
        self.old_move_x = 0
        self.old_move_y = 0

        self.recorded_lod = True
        self.left_click = False
        self.right_click = False

        self.going_right = False
        self.going_left = False
        self.going_up = False
        self.going_down = False

        self.movement_rate = 10

        #random stuff
        self.h = False
        self.r = False
        self.a = 0

        self.prep_speed()
        self.prep_default()
        self.set_active_tool("Open")





    def check_events(self):
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN and self.text_active:
                if event.key == pygame.K_BACKSPACE and self.text_active:
                    try:
                        self.user_text = self.user_text.removesuffix(self.user_text[self.user_text.__len__()-1])
                    except IndexError:
                        self.user_text = ''
                elif event.key == pygame.K_SPACE and self.text_active:
                    self.user_text += '_'
                elif event.key == pygame.K_ESCAPE and self.text_active:
                    self.user_text = ''
                    self.current_message = self.user_text
                    self.set_active_tool("Past")
                elif event.key == pygame.K_RETURN and self.text_active:
                    self.saved_text = self.user_text
                    self.user_text = ''
                    self.current_message = self.user_text
                    self.set_active_tool("Past")
                else:
                    if self.user_text.__len__() <= self.text_file_limit:
                        self.user_text += event.unicode

            # controls
            elif event.type == pygame.KEYDOWN and self.map_present:
                if event.key == pygame.K_x:
                    if self.mouse_drag_multiplyer == 8:
                        self.mouse_drag_multiplyer = 1
                    else:
                        self.mouse_drag_multiplyer += 1
                elif event.key == pygame.K_z:
                    if self.mouse_drag_multiplyer == 1:
                        self.mouse_drag_multiplyer = 8
                    else:
                        self.mouse_drag_multiplyer -= 1

                elif event.key == pygame.K_RIGHT:
                    self.going_right = True


                elif event.key == pygame.K_LEFT:
                    self.going_left = True


                elif event.key == pygame.K_UP:
                    self.going_up = True


                elif event.key == pygame.K_DOWN:
                    self.going_down = True

                

                #elif event.key == pygame.K_t:
                    #print(self.displayed_access_map)

                elif event.key == pygame.K_s:
                    self.camera_x = 0
                    self.camera_y = 0

            elif event.type == pygame.KEYUP and self.map_present:
                if event.key == pygame.K_RIGHT:
                    self.going_right = False


                elif event.key == pygame.K_LEFT:
                    self.going_left = False


                elif event.key == pygame.K_UP:
                    self.going_up = False


                elif event.key == pygame.K_DOWN:
                    self.going_down = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and not self.access_active:
                    self.zoom_in()
                if event.y < 0 and not self.access_active:
                    self.zoom_out()
                


            elif event.type == pygame.MOUSEBUTTONUP:
                self.recorded_lod = True
                if not pygame.mouse.get_pressed()[0]:
                    self.left_click = False
                if not pygame.mouse.get_pressed()[2]:
                    self.right_click = False
                    

            if self.text_active:
                self.current_message = "Enter name: "+self.user_text

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.left_click = True
                if pygame.mouse.get_pressed()[2]:
                    self.right_click = True

                mouse_pos = pygame.mouse.get_pos()
                if self.internal:
                    self.check_system_functions(mouse_pos)
                    self.check_open_file_functions(mouse_pos)
                    self.check_create_file_functions(mouse_pos)
                    if self.map_present:
                        self.check_terrain_functions(mouse_pos)
                        self.check_object_functions(mouse_pos)
                        self.check_sound_functions(mouse_pos)
                        self.check_prop_functions(mouse_pos)
                        self.check_access_functions(mouse_pos)



    def new_display_map(self, map, x, y):
        
        map = map.terrain_map
        #print(map[1].__len__())
        ls = []
        self.h = 0
        self.v = 0
        b = 0
        thing1 = self.get_map_size()
        thing2 = self.get_half_size()
        for v in range(thing1):
            self.v += 1
            self.v = int(self.v)
            for h in range(thing1):
                self.h += 1
                if (x + self.h - thing2) < 0:
                    ls.append(0)
                else:
                    try:
                        b = map[y + self.v - (thing2 - 1)]
                        try:
                            ls.append(b[x + self.h - thing2])
                        except IndexError:
                            ls.append(0)
                    except KeyError:
                        ls.append(0)
            self.displayed_map[self.v] = ls
            ls = []
            self.h = 0
        #print("build time")
        #print(time.time() - ntime)
        
        numberX = self.map_posX
        numberY = self.map_posY
        row_number = 1
        row_position = 0
        #ntime = time.time()
        blit = self.screen.blit
        t = self.image_library.PRELOADED_IMAGES
        for y in range(thing1):
            for x in range(thing1):
                #a = time.time()
                image_number = self.displayed_map[row_number][row_position]
                self.image = t[image_number][0]
                
                #p = time.time()
                #self.image = pygame.transform.scale(self.image, (self.current_size, self.current_size))
                #print(time.time() - p)
                
                self.rect = self.image_library.PRELOADED_IMAGES[image_number][1]
                #self.rect.x = numberX + self.display_offset_x
                #self.rect.y = numberY + self.display_offset_y
                self.rect.x, self.rect.y = numberX + self.display_offset_x, numberY + self.display_offset_y
                
                blit(self.image, self.rect)
                
                #numberX += self.current_size
                #row_position +=1
                numberX, row_position = numberX + self.current_size, row_position + 1
                #print(time.time() - a)
            numberY += self.current_size
            row_number +=1
            numberX = self.map_posX
            row_position = 0
        b = time.time()
        
        #print("display time")
        #print(b - ntime2)






    def display_props(self, prop_map, x, y):
        ls = self.props.get_props(prop_map, (x, y), self.get_map_size())
        get_map_size = self.get_map_size()
        j = self.get_map_size()
        if get_map_size % 2:
            pass
        else:
            get_map_size += 1
        get_map_size /= 2
        if j == 11 or j == 31 or j == 39:
            get_map_size += 1
        
        get_map_size -= 1.5
        get_map_size *= self.current_size
        for prop in ls:
            num = prop[1]
            coor = prop[0][0]
            img = self.props.PROP_LIST[num][2]
            scale_ratio = self.props.PROP_LIST[num][7]
            img_sur = img[0]
            img_sur = pygame.transform.scale(img[0], (scale_ratio[0] * self.current_size, scale_ratio[1] * self.current_size))
            xv = ((coor[0] - x) * self.current_size + get_map_size)
            yv = ((coor[1] - y) * self.current_size + get_map_size)
            xx = ((coor[0]) + self.map_posX) + xv
            yy = ((coor[1]) + self.map_posY) + yv
            
            img[1].x = xx + self.display_offset_x #- (get_map_size)
            img[1].y = yy + self.display_offset_y #- (get_map_size)
            self.screen.blit(img_sur, img[1])




    def display_shadows(self, prop_map, object_map, x, y):
        prop_ls = self.props.get_props(prop_map, (x, y), self.get_map_size())
        get_map_size = self.get_map_size()
        j = self.get_map_size()
        if get_map_size % 2:
            pass
        else:
            get_map_size += 1
        get_map_size /= 2
        if j == 11 or j == 31 or j == 39:
            get_map_size += 1
        get_map_size -= 1.5
        get_map_size *= self.current_size
        for prop in prop_ls:
            num = prop[1]
            coor = prop[0][0]
            img = self.props.PROP_LIST[num][3]
            scale_ratio = self.props.PROP_LIST[num][8]
            img_sur = img[0]
            img_sur = pygame.transform.scale(img_sur, (scale_ratio[0] * self.current_size, scale_ratio[1] * self.current_size))
            xv = ((coor[0] - x) * self.current_size + get_map_size) + (self.props.PROP_LIST[num][10][0] / self.get_map_size())
            yv = ((coor[1] - y) * self.current_size + get_map_size) + (self.props.PROP_LIST[num][10][1] / self.get_map_size())
            xx = ((coor[0]) + self.map_posX) + xv
            yy = ((coor[1]) + self.map_posY) + yv
            img[1].x = xx + self.display_offset_x
            img[1].y = yy + self.display_offset_y
            self.screen.blit(img_sur, img[1])




        

    def display_access_map(self, map, x, y):
        x = (x * 6) + 8
        y = (y * 6) + 8
        ls = []
        self.h = 0
        self.v = 0
        for v in range(self.get_map_size_access()):
            self.v += 1
            self.v = int(self.v)
            for h in range(self.get_map_size_access()):
                self.h += 1
                if (x + self.h - self.get_half_size_access()) < 0:
                    ls.append([0,0])
                else:
                    try:
                        b = map[y + self.v - (self.get_half_size_access() - 1)]
                        try:
                            ls.append(b[x + self.h - self.get_half_size_access()])
                        except IndexError:
                            ls.append([0,0])
                    except KeyError:
                        ls.append([0,0])
            self.displayed_access_map[self.v] = ls.copy()
            ls = []
            self.h = 0
        numberX = self.map_posX
        numberY = self.map_posY
        row_number = 1
        row_position = 0
        for y in range(self.get_map_size_access()):
            for x in range(self.get_map_size_access()):
                image_number = self.displayed_access_map[row_number][row_position][0]
                v_h_number = self.displayed_access_map[row_number][row_position][1]
                self.image = self.image_library.ACCESS_IMAGES[image_number][0]
                self.image = pygame.transform.scale(self.image, (self.access_control_size, self.access_control_size))
                self.rect = self.image_library.ACCESS_IMAGES[image_number][1]
                self.rect.x = numberX
                self.rect.y = numberY
                self.screen.blit(self.image, self.rect)

                if image_number != 0:
                    self.FL.draw_words(str(v_h_number), 15, (numberX, numberY), False, "black")


                numberX += self.access_control_size
                row_position +=1
            numberY += self.access_control_size
            row_number +=1
            numberX = self.map_posX
            row_position = 0


    def check_open_file_functions(self, mouse_pos):
        if self.open_file.main_rect.collidepoint(mouse_pos):
            self.draw_open_file_buttons()
            self.set_active_tool("Open")
        if self.open_file.rect_left.collidepoint(mouse_pos) and self.open_file_active:
            self.open_file.current_file -= 1
        if self.open_file.rect_right.collidepoint(mouse_pos) and self.open_file_active:
            self.open_file.current_file += 1

        if self.open_file.open_rect.collidepoint(mouse_pos) and self.open_file_active:
            self.map_present = False
            self.h = True
            self.current_file_open = path.splitext(self.open_file.file_list[self.open_file.current_file])[0]
        
    def check_if_file_open(self):
        if self.h:
            self.map_present = True
            self.h = False
    
    def check_create_file_functions(self, mouse_pos):
        if self.create_file.main_rect.collidepoint(mouse_pos):
            self.draw_create_file_buttons()
            self.set_active_tool("Create")
        if self.pick_terrain.rect_left.collidepoint(mouse_pos) and self.create_file_active == True:
            self.pick_terrain.add_substract_terrain("-")
        if self.pick_terrain.rect_right.collidepoint(mouse_pos) and self.create_file_active == True:
            self.pick_terrain.add_substract_terrain("+")

        if self.affirm_file.affirm_rect.collidepoint(mouse_pos) and self.create_file_active:
            self.current_message = self.affirm_file.build_new_map(self.saved_text, 200, self.pick_terrain.current_image, 3)

        if self.pick_terrain.pick_name_rect.collidepoint(mouse_pos) and self.create_file_active:
            self.set_active_tool("Text")


    def check_terrain_functions(self, mouse_pos):
        if self.terrain.main_rect.collidepoint(mouse_pos):
            self.draw_terrain_buttons()
            self.set_active_tool("Terrain")

        if self.pick_terrain.rect_left.collidepoint(mouse_pos) and self.terrain_active:
            self.pick_terrain.add_substract_terrain("-")
        if self.pick_terrain.rect_right.collidepoint(mouse_pos) and self.terrain_active:
            self.pick_terrain.add_substract_terrain("+")

        if self.terrain.rect_left.collidepoint(mouse_pos) and self.terrain_active:
            self.terrain.increase_brush()
        if self.terrain.rect_right.collidepoint(mouse_pos) and self.terrain_active:
            self.terrain.decrease_brush()

    def check_prop_functions(self, mouse_pos):
        if self.props.main_rect.collidepoint(mouse_pos):
            self.draw_prop_buttons()
            self.set_active_tool("Prop")

        if self.props.rect_left_key.collidepoint(mouse_pos) and self.prop_active:
            self.props.category_up()
        if self.props.rect_right_key.collidepoint(mouse_pos) and self.prop_active:
            self.props.category_down()

        if self.props.rect_left_prop.collidepoint(mouse_pos) and self.prop_active:
            self.props.prop_up()
        if self.props.rect_right_prop.collidepoint(mouse_pos) and self.prop_active:
            self.props.prop_down()

        if self.props.eraser_rect.collidepoint(mouse_pos) and self.prop_active:
            self.props.on_off_eraser()


    def check_object_functions(self, mouse_pos):
        if self.objects.main_rect.collidepoint(mouse_pos):
            self.draw_object_buttons()
            self.set_active_tool("Object")

    def check_sound_functions(self, mouse_pos):
        if self.sound.main_rect.collidepoint(mouse_pos):
            self.draw_sound_buttons()
            self.set_active_tool("Sound")

    def check_access_functions(self, mouse_pos):
        if self.access.main_rect.collidepoint(mouse_pos):
            self.draw_access_buttons()
            self.set_active_tool("Access")
            self.set_mean_zoom()
            self.FL.prep_color_zero()

        if self.access_active and self.access.rect_left.collidepoint(mouse_pos):
            self.access.alter_access_number(False)

        if self.access_active and self.access.rect_right.collidepoint(mouse_pos):
            self.access.alter_access_number(True)

        if self.access_active and self.access.size_rect_left.collidepoint(mouse_pos):
            self.access.increase_brush()
        
        if self.access_active and self.access.size_rect_right.collidepoint(mouse_pos):
            self.access.decrease_brush()

        if self.access_active and self.access.v_h_rect_right.collidepoint(mouse_pos):
            self.access.decrease_v_h()
        if self.access_active and self.access.v_h_rect_left.collidepoint(mouse_pos):
            self.access.increase_v_h()


    def check_system_functions(self, mouse_pos):
        if self.quit_program.main_rect.collidepoint(mouse_pos):
            self.quit_program.quit_program()
        elif self.ajust_size.zoom_out_rect.collidepoint(mouse_pos) and self.map_present and not self.access_active:
            self.zoom_out()
        elif self.ajust_size.zoom_in_rect.collidepoint(mouse_pos) and self.map_present and not self.access_active:
            self.zoom_in()
            #print(self.current_file_open)

        elif self.drag_area.rect.collidepoint(mouse_pos):
            self.recorded_lod = True

        elif self.save.main_rect.collidepoint(mouse_pos) and self.map_present and self.save.changes_made:
            self.affirm_file.write_to_file(self.current_file_open, 'w', self.terrain_instance, self.prop_map, [], [], self.access_data_instance, 1, 0)
            self.save.changes_made = False
            


    def check_mouse(self):
        if self.recorded_lod == True:
            self.old_move_x = pygame.mouse.get_pos()[0]
            self.old_move_y = pygame.mouse.get_pos()[1]
            self.recorded_lod = False
        if self.right_click == True and self.recorded_lod == False:
            self.move_x = pygame.mouse.get_pos()[0]
            self.move_y = pygame.mouse.get_pos()[1]
            if (abs(self.old_move_x) - self.move_x) > 10:
                self.camera_x += 1 * self.mouse_drag_multiplyer
                self.recorded_lod = True
            if (abs(self.old_move_x) - self.move_x) < -10:
                self.camera_x -= 1 * self.mouse_drag_multiplyer
                self.recorded_lod = True
            if (abs(self.old_move_y) - self.move_y) > 10:
                self.camera_y += 1 * self.mouse_drag_multiplyer
                self.recorded_lod = True
            if (abs(self.old_move_y) - self.move_y) < -10:
                self.camera_y -= 1 * self.mouse_drag_multiplyer
                self.recorded_lod = True
        
        # PAINT TERRAIN
        elif self.left_click == True and self.terrain_active and self.drag_area.rect.collidepoint(pygame.mouse.get_pos()):
            #print(self.move_x, self.move_y)
            #print(self.get_minus_zoom_number())
            #print(self.get_mouse_pos_terrain(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[1]))
            self.terrain_instance = self.terrain.paint_terrain(
                self.terrain_instance,
                self.get_mouse_pos_terrain(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[1])[0],
                self.get_mouse_pos_terrain(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[1])[1],
                self.terrain.brush_size,
                self.pick_terrain.current_image
                )
            self.r = True

        # PAINT ACCESS
        elif self.left_click and self.access_active and self.drag_area.rect.collidepoint(pygame.mouse.get_pos()):
            self.access_data_instance = self.access.add_access_rect(
                self.access_data_instance,
                self.get_mouse_pos_access(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.access_control_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.access_control_size)[1])[0],
                self.get_mouse_pos_access(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.access_control_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.access_control_size)[1])[1],
                self.access.brush_size,
                self.access.current_selected_access_number,
                self.access.v_h
            )
            self.access_map_instance = self.access.extract_access_map(self.map_data)
            self.r = True

        # PLACE PROPS
        elif self.left_click and self.prop_active and self.drag_area.rect.collidepoint(pygame.mouse.get_pos()):
            if self.props.eraser_on:
                self.prop_map = self.props.erase_prop(
                    self.prop_map,
                    self.get_mouse_pos_terrain(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[1]),
                )
            else:
                self.prop_map = self.props.place_prop(
                    self.prop_map,
                    self.get_mouse_pos_terrain(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[1]),
                )
            self.prop_instance = self.props.get_prop_coordinates(self.prop_map)
            self.r = True

            
        elif self.left_click == False and self.r:
            if self.terrain_active or self.access_active or self.prop_active or self.object_active or self.sound_active:
                self.save.changes_made = True
                self.r = False

    def check_keys(self):
        if self.going_up:
            self.move_up()
        if self.going_down:
            self.move_down()
        if self.going_right:
            self.move_right()
        if self.going_left:
            self.move_left()


    def move_up(self):
        self.player_Y += 60 * self.mouse_drag_multiplyer
        self.display_offset_y += self.movement_rate
        if self.display_offset_y >= 60:
            self.display_offset_y = 0.0
            self.camera_y -= 1 * self.mouse_drag_multiplyer

    def move_down(self):
        self.player_Y -= 60 * self.mouse_drag_multiplyer
        self.display_offset_y -= self.movement_rate
        if self.display_offset_y <= -60:
            self.display_offset_y = 0.0        
            self.camera_y += 1 * self.mouse_drag_multiplyer

    def move_left(self):
        self.player_X += 60 * self.mouse_drag_multiplyer
        self.display_offset_x += self.movement_rate
        if self.display_offset_x >= 60:
            self.display_offset_x = 0.0
            self.camera_x -= 1 * self.mouse_drag_multiplyer

    def move_right(self):
        self.player_X -= 60 * self.mouse_drag_multiplyer
        self.display_offset_x -= self.movement_rate
        if self.display_offset_x <= -60:
            self.display_offset_x = 0.0
            self.camera_x += 1 * self.mouse_drag_multiplyer
            



    def get_mouse_pos_terrain(self, x, y):
        x = x + self.camera_x - math.floor(self.current_size / 2) + math.ceil(self.current_size / 2) + (self.get_minus_zoom_number()) + self.get_minus_zoom_number()
        y = y + self.camera_y - math.floor(self.current_size / 2) + math.ceil(self.current_size / 2) + (self.get_minus_zoom_number()) + self.get_minus_zoom_number()
        return x, y
    
    def get_mouse_pos_access(self, x, y):
        x = x + self.camera_x - math.floor(self.access_control_size / 2) + math.ceil(self.access_control_size / 2) + (self.get_minus_zoom_number_access()) + self.get_minus_zoom_number_access()
        y = y + self.camera_y - math.floor(self.access_control_size / 2) + math.ceil(self.access_control_size / 2) + (self.get_minus_zoom_number_access()) + self.get_minus_zoom_number_access()
        x = x + (self.camera_x * 5)
        y = y + (self.camera_y * 5)
        return x+41, y+41
    
    def get_minus_zoom_number(self):
        a = self.image_library.ZOOM_MOUSE_NUMBERS[int(self.current_size / 5)]
        return a -5
    
    def get_minus_zoom_number_access(self):
        a = self.image_library.ZOOM_MOUSE_NUMBERS[int(self.access_control_size/ 5)]
        return a - 5


    def zoom_out(self):
        #if not self.current_size == 10:
        #    self.current_size -= 5
        print("zoom out disabled")
    
    def zoom_in(self):
        #if not self.current_size == 100:
        #    self.current_size += 5
        print("zoom in disabled")

    def set_mean_zoom(self):
        self.current_size = 60

    def get_mouse_click_pos(self, pos, size):
        x = pos[0] - self.map_posX
        y = pos[1] - self.map_posY
        x = math.floor(x / size) - self.get_minus_zoom_number()
        y = math.floor(y / size) - self.get_minus_zoom_number()
        return (x, y)


    def prep_speed(self):
        speed_str = "Speed: "+str(self.mouse_drag_multiplyer)
        self.speed_image = self.speed_font.render(speed_str, True, self.speed_text_color, (127,127,127))

        self.speed_rect = self.speed_image.get_rect()
        self.speed_rect.x = 275
        self.speed_rect.y = 12

    def prep_default(self):
        self.default = pygame.image.load(self.image_library.SYSTEM_IMAGES[6])
        self.default_rect = self.default.get_rect()
        self.default_rect.x = 250
        self.default_rect.y = 50

    def set_neutral(self):
        """OUTDATED"""
        self.create_file_active = False
        self.terrain_active = False
        self.prop_active = False
        self.object_active = False
        self.sound_active = False
        self.area_left.draw_main()
        

    def set_active_tool(self, mode):
        self.open_file_active = False
        self.create_file_active = False
        self.terrain_active = False
        self.prop_active = False
        self.object_active = False
        self.sound_active = False
        self.text_active = False
        self.access_active = False
        if mode == "Past":
            mode = self.past_mode
        self.past_mode = self.current_tool
        if mode == "Create":
            self.create_file_active = True
        elif mode == "Terrain":
            self.terrain_active = True
        elif mode == "Prop":
            self.prop_active = True
        elif mode == "Object":
            self.object_active = True
        elif mode == "Sound":
            self.sound_active = True
        elif mode == "Text":
            self.text_active = True
        elif mode == "Open":
            self.open_file_active = True
        elif mode == "Access":
            self.access_active = True
        self.current_tool = mode

    def import_map(self, file_name):
        if file_name == '':
            self.map_present = False
        else:
            self.map_data = importlib.import_module(file_name)
            self.map_data_instance = importlib.import_module(file_name)
            self.terrain_instance = self.map_data_instance.terrain_map
            self.prop_map = self.map_data_instance.prop_map
            self.prop_instance = self.props.get_prop_coordinates(self.prop_map)
            #print(self.prop_instance)
            self.object_instance = self.map_data_instance.object_map
            self.access_map_instance = self.access.extract_access_map(self.map_data)
            self.access_data_instance = self.map_data.access_map
            self.player_X = self.map_data.player_x
            self.player_Y = self.map_data.player_y
            self.save.changes_made = False

    def build_terrain_map(self, terrain_instance: dict):
        new_map = {}
        new_row = []
        il_ref = self.image_library.PRELOADED_IMAGES
        tf_ref = self.image_library.TERRAIN_FILEPATHS
        print(tf_ref)

        a = True
        b = True

        h = 0
        
        # Ensure map size is even
        if terrain_instance.__len__() % 2 == 0:
            print("Map size even. Assuming X length is even")
        else:
            raise AssertionError("Map size is uneven. Cannot build.")
        
        # Build images
        for y in range(terrain_instance.__len__()):
            
            if a:
                for x in range(terrain_instance[y+1].__len__()):

                    if b:
                        # Build new image and save it
                        topleft_image = Image.open(tf_ref[terrain_instance[y+1][x]])
                        topright_image = Image.open(tf_ref[terrain_instance[y+1][x+1]])
                        bottomleft_image = Image.open(tf_ref[terrain_instance[y+2][x]])
                        bottomright_image = Image.open(tf_ref[terrain_instance[y+2][x+1]])
                        new_img = Image.new('RGB', (120, 120), (0,0,0))
                        new_img.paste(topleft_image, (0,0))
                        new_img.paste(topright_image, (60, 0))
                        new_img.paste(bottomleft_image, (0, 60))
                        new_img.paste(bottomright_image, (60, 60))
                        name = str(y)+str(x)+'.png'
                        new_img.save(name,'PNG')

                        # Resolve new image to new_map
                        ordered_img = pygame.image.load(name)
                        os.remove(name)
                        new_row.append([ordered_img, ordered_img.get_rect()])
                        #progress = 100 * float(y)/float(terrain_instance.__len__())
                        #self.screen.fill((0,0,0))
                        #self.FL.draw_words(str(progress)+"%", 100, (100, 100), False, "white")
                        #pygame.display.update()
                        #for event in pygame.event.get():
                        #    # check for quit
                        #    if event.type == pygame.QUIT:
                        #        sys.exit()
                    

                        # Prepare for next step
                        b = False
                    else:
                        b = True
                a = False
                h += 1
                new_map[h] = new_row.copy()
                new_row.clear()
            else:
                a = True

        return new_map
        




    def get_map_size(self):
        return round(self.screen_map_size / self.current_size)
    
    def get_map_size_access(self):
        return round(self.screen_map_size / self.access_control_size)

    def get_half_size(self):
        return round(self.get_map_size() / 2)
    
    def get_half_size_access(self):
        return round(self.get_map_size_access() / 2)
            
            

    def display_speed(self):
        self.screen.blit(self.speed_image, self.speed_rect)

    def draw_folders(self, draw_tools):
        if draw_tools:
            self.open_file.draw_main()
            self.create_file.draw_main()
            self.terrain.draw_main()
            self.props.draw_main()
            self.objects.draw_main()
            self.sound.draw_main()
            self.access.draw_main()
        else:
            self.open_file.draw_main()
            self.create_file.draw_main()

        if self.open_file_active == True:
            self.open_file.draw_all()
        if self.create_file_active == True:
            self.draw_create_file_buttons()
        if self.terrain_active == True:
            self.draw_terrain_buttons()
        if self.prop_active == True:
            self.props.draw_all()
        if self.object_active == True:
            self.objects.draw_all()
        if self.sound_active == True:
            self.sound.draw_all()
        if self.access_active:
            self.access.draw_all()

    def draw_system(self):
        self.quit_program.draw_main()
        self.drag_area.draw_drag_area()
        self.display_speed()
        self.ajust_size.draw_all_zoom()
        self.print.print_m(self.current_message)
        self.save.draw_all()
        if self.access_active:
            self.position.draw_position(
                (self.camera_x, self.camera_y), 
                self.get_mouse_pos_access(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.access_control_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.access_control_size)[1])
                                        )
        else:
            self.position.draw_position(
                (self.camera_x, self.camera_y), 
                self.get_mouse_pos_terrain(self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[0], self.get_mouse_click_pos(pygame.mouse.get_pos(), self.current_size)[1])
                                        )



    def draw_sides(self):
        self.area_left.draw_main()
        self.area_right.draw_main()
        self.area_up.draw_main()
        self.area_down.draw_main()

    def draw_create_file_buttons(self):
        self.create_file.draw_main()
        self.affirm_file.draw_affirm()
        self.pick_terrain.draw_main()
        self.pick_terrain.draw_selected_image(self.pick_terrain.load_selected_terrain())
        self.pick_terrain.draw_words(self.pick_terrain.prep_words(self.saved_text)[0], self.pick_terrain.prep_words(self.saved_text)[1])
        self.pick_terrain.draw_pick_name()

    def draw_terrain_buttons(self):
        self.terrain.draw_all()
        self.pick_terrain.draw_main()
        self.pick_terrain.draw_selected_image(self.pick_terrain.load_selected_terrain())

    def draw_prop_buttons(self):
        self.props.draw_main()

    def draw_object_buttons(self):
        self.objects.draw_main()

    def draw_open_file_buttons(self):
        self.open_file.draw_all()
        
    def draw_sound_buttons(self):
        self.sound.draw_main()

    def draw_access_buttons(self):
        self.access.draw_all()
        
    def draw_default(self):
        self.screen.blit(self.default, self.default_rect)

    def draw_world(self, map, x, y):
        self.new_display_map(map, x, y)
        self.display_shadows(self.prop_instance, self.object_instance, x, y)
        self.display_props(self.prop_instance, x, y)
        if self.access_active:
            self.display_access_map(self.access_map_instance, x, y)


    def run_program(self):

        # initalize everything
        self.draw_system()
        self.draw_folders(True)
        self.set_active_tool("Create")
        self.draw_folders(True)
        self.set_active_tool("Terrain")
        self.draw_folders(True)
        self.set_active_tool("Prop")
        self.draw_folders(True)
        self.set_active_tool("Object")
        self.draw_folders(True)
        self.set_active_tool("Sound")
        self.draw_folders(True)
        self.set_active_tool("Open")

        while True:
            #start_time = time.time()
            if self.map_present:
                # get map data
                self.import_map(self.current_file_open)

                #self.terrain_map = self.build_terrain_map(self.map_data.terrain_map, self.map_data.size_x, self.map_data.size_y)
                #self.zoom_out_map = self.build_zoom_out_map(self.map_data.terrain_map, self.map_data.size_x, self.map_data.size_y)
                #self.current_map = self.terrain_map



                while self.map_present:
                    self.screen.fill((0,0,0))
                    # refresh screen
                    self.check_events()
                    self.check_mouse()
                    self.prep_speed()
                    self.draw_world(self.map_data_instance, self.camera_x, self.camera_y)
                    self.draw_sides()
                    self.draw_system()
                    self.draw_folders(True)
                    self.open_file.update_file_list()
                    self.check_if_file_open()
                    #print(self.get_map_size())
                    pygame.display.update()
                    #duration = time.time() - start_time
                    #print(duration)
                    #start_time = time.time()
            else:
                while not self.map_present:
                    self.screen.fill((0,0,0))
                    # refresh screen
                    self.check_events()
                    self.prep_speed()
                    self.draw_default()
                    self.draw_sides()
                    self.draw_system()
                    self.draw_folders(False)
                    self.open_file.update_file_list()
                    self.check_if_file_open()
                    pygame.display.update()


if __name__ == '__main__':
    ai = MapMakerRevolution(True, 0)
    ai.run_program()
