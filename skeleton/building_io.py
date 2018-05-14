import building
import pygame

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
dgray    = (  63,  63,  63)
lgray    = ( 127, 127, 127)
red      = ( 255,   0,   0)
green    = (   0, 255,   0)
blue     = (   0,   0, 255)
brown    = ( 205, 102,  31)

def center_label(screen, label, x, y):
    """places a label on the screen so that its center is at (x,y)"""
    pos_x = x - label.get_width() // 2
    pos_y = y - label.get_height() // 2
    screen.blit(label, (pos_x,pos_y))

class BuildingRenderer:
    """renderer for displaying a building on screen"""
    
    def __init__(self, building, screen_pos, room_size):
        self.building = building
        self.screen_pos = screen_pos
        self.room_size = room_size
    
    def display_building(self, screen):
        # Set the screen background
        screen.fill(black)
        # init values
        myfont = pygame.font.SysFont("Comic Sans MS", 6 + self.room_size // 4)
        # draw each room
        dim = 2 * self.building.size + 1
        for row in range(dim):
            for col in range(dim):
                pos_x = self.screen_pos[0] + col * self.room_size
                pos_y = self.screen_pos[1] + row * self.room_size
                pygame.draw.rect(screen, white, pygame.Rect(pos_x, pos_y, self.room_size, self.room_size), 1)
                if self.building.is_collapsed(row, col):
                    pygame.draw.rect(screen, dgray, pygame.Rect(pos_x, pos_y, self.room_size, self.room_size))
                    continue
                elif row == self.building.player_row and col == self.building.player_col:
                    # draw player as @ symbol
                    label = myfont.render("@", 1, red)
                else:
                    # draw food and/or water in room
                    room = self.building.rooms[row][col]
                    if room.food == room.water == 0:
                        continue
                    elif room.food == room.water:
                        label = myfont.render(str(room.food), 1, lgray)
                    elif room.water == 0:
                        label = myfont.render(str(room.food), 1, brown)
                    elif room.food == 0:
                        label = myfont.render(str(room.water), 1, blue)
                    else:
                        label = myfont.render("{0}/{1}".format(room.food, room.water), 1, lgray)
                center_label(screen, label, pos_x + self.room_size // 2, pos_y + self.room_size // 2);
