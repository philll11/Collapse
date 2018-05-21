import building, building_io, optimizer
import pygame, os, sys, time

# init screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Collapse")

# default config
size = 1
equal_supplies = True


# utility functions
def limit(lower, x, upper):
    return min(max(lower, x), upper)


def local_delay(t):
    """stops the current execution for t seconds without delaying other threads"""
    start = time.time()
    while time.time() - start < t: pass


# command line overwrite
print("syntax: python collapse.py [size] [easy|hard]")
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    size = limit(1, int(sys.argv[1]), 20)
if len(sys.argv) > 2 and sys.argv[2] == "hard":
    equal_supplies = False


# drawing functions
def show_status():
    myfont = pygame.font.SysFont("Comic Sans MS", 12)

    def print_at(msg, x, y):
        label = myfont.render(msg, 1, building_io.white)
        screen.blit(label, (x, y))

    if equal_supplies:
        print_at("Supplies collected:  {0} / {1}".format(my_building.player_food, player_needs), screen_size[1] + 15,
                 20)
    else:
        print_at("Food collected:  {0} / {1}".format(my_building.player_food, player_needs), screen_size[1] + 15, 20)
        print_at("Water collected:  {0} / {1}".format(my_building.player_water, player_needs), screen_size[1] + 15, 40)
    print_at("r: reset", screen_size[1] + 15, 60)
    print_at("n: new", screen_size[1] + 15, 80)


def redraw(flip=True):
    my_renderer.display_building(screen)
    show_status()
    if flip: pygame.display.flip()


# initialization function
def new_building():
    global my_building, my_renderer, player_needs
    my_building = building.random_building(size, equal_supplies)
    player_needs = optimizer.max_food(my_building) if equal_supplies else optimizer.max_supplies(my_building)
    # new renderer
    room_size = screen_size[1] // (2 * size + 1)
    offset = (screen_size[1] - (2 * size + 1) * room_size) // 2
    my_renderer = building_io.BuildingRenderer(my_building, (offset, offset), room_size)


# initialization
new_building()
redraw(True)

# -------- Main Program Loop -----------
while True:
    event = pygame.event.wait()  # get one event, wait until it happens
    if event.type == pygame.QUIT:  # user clicked close
        break
    # handle player movement
    if event.type == pygame.KEYDOWN:
        if ((event.key == pygame.K_LEFT and my_building.move_player(0, -1)) or
                (event.key == pygame.K_RIGHT and my_building.move_player(0, 1)) or
                (event.key == pygame.K_UP and my_building.move_player(-1, 0)) or
                (event.key == pygame.K_DOWN and my_building.move_player(1, 0))):
            # game over?
            if not my_building.can_move():
                redraw(False)
                # show win/loss message
                myfont = pygame.font.SysFont("Comic Sans MS", 16)
                supplies = min(my_building.player_food, my_building.player_water)
                victory = supplies >= player_needs
                msg = "You collected supplies for {0} out of {1} days. You {2}.".format(supplies, player_needs,
                                                                                        "survive" if victory else "die")
                if victory:
                    label = myfont.render(msg, 1, building_io.green)
                else:
                    label = myfont.render(msg, 1, building_io.red)
                building_io.center_label(screen, label, screen_size[1] / 2, screen_size[1] / 2)
                pygame.display.flip()
                # progress to next level
                if victory and (size < 20 or equal_supplies):
                    local_delay(2.0)
                    if size < 20:
                        size += 1
                    else:
                        size = 1
                        equal_supplies = False
                    new_building()
                    redraw()
            else:
                redraw()
        elif event.key == pygame.K_p:  # print current game to stdout
            print(my_building)
        elif event.key == pygame.K_n:  # new game
            new_building()
            redraw()
        elif event.key == pygame.K_r:  # reset current game
            my_building.reset()
            redraw()

# clean exit
pygame.quit()
