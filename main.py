"""
Author: Sebastian Sanchez
Date: 2024/06/17
Description: platformer game where the goal is to survive.
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dog vs Space Cat")

# Define colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Game states
OPENING = 1
PLAYING = 2
GAME_OVER = 3

#Initialize game state
game_state = OPENING

#Level states
LEVEL_ONE = 1
LEVEL_TWO = 2
LEVEL_THREE = 3
LEVEL_FOUR = 4
ENDLESS = 5

"""
Text
"""
#game over text
game_over_font = pygame.font.Font("fonts/OWERSTINN.ttf", 175)
game_over_text = "GAME MEOWVER"
game_over_surface = game_over_font.render(game_over_text, True, RED)
game_over_rect = game_over_surface.get_rect(center = (WIDTH // 2, HEIGHT // 2))

#game font
game_font = pygame.font.Font("fonts/JMH Typewriter.ttf", 40)

#score text
score_text = "Score: {global_score}"
score_surface = game_font.render(score_text, True, WHITE)
score_rect = score_surface.get_rect(topleft = (30, 600))

#level text
level_text = "Level {game_lv}"
level_surface = game_font.render(level_text, True, WHITE)
level_rect = level_surface.get_rect(topleft = (30, 675))

#next level text
next_level_text = "Next Level: {next_level}"
next_level_surface = game_font.render(next_level_text, True, WHITE)
next_level_rect = next_level_surface.get_rect(left = score_rect.right - 150, top = score_rect.top)

#bark bark_cooldown text
bark_cooldown_text = "Bark Cooldown {bark_cooldown}"
bark_cooldown_surface = game_font.render(bark_cooldown_text, True, WHITE)
bark_cooldown_rect = bark_cooldown_surface.get_rect(left = next_level_rect.left, top = level_rect.top)

#over font
over_font = pygame.font.Font("fonts/MilknBalls-BlackDemo.ttf", 40)

#final score text
final_score_text = "Final Score {global_score}"
final_score_surface = over_font.render(final_score_text, True, WHITE)
final_score_rect = final_score_surface.get_rect(center = (WIDTH // 2, 200))

#global_highscore text
global_highscore = 0
highscore_text = "Highscore {global_highscore}"
highscore_surface = over_font.render(highscore_text, True, WHITE)
highscore_rect = highscore_surface.get_rect(center = (WIDTH // 2, 200))

#play again text
play_again_text = "Press E to Play Again"
play_again_surface = over_font.render(play_again_text, True, WHITE)
play_again_rect = play_again_surface.get_rect(center = (WIDTH // 2, 700))

all_score_text = [score_surface, final_score_surface, final_score_rect, highscore_surface, highscore_rect]

#start text
start_font = pygame.font.Font("fonts/Cross Boxed.ttf", 80)
start_text = "Press E to Start"
start_surface = start_font.render(start_text, True, WHITE, BLACK)
start_rect = start_surface.get_rect(center = (WIDTH // 2, 500))

#instruction text
instruction_font = pygame.font.Font(None, 30)
goal_text = "- Your Goal is to Survive by Dodging Projectiles and Escaping the Chasing Wall"
control_text = "- Use a and d to Move Left and Right, Use Space to Jump, Use LMB to Bark"
stages_text = "- Level Switches are Time Based, New Levels Introduce New Projectiles"
endless_text = "- After the Final Level, Enter Endless Mode Which Gets Progressively Harder"

goal_surface = instruction_font.render(goal_text, True, WHITE, BLACK)
goal_rect = goal_surface.get_rect(center = (WIDTH // 2, 250))

control_surface = instruction_font.render(control_text, True, WHITE, BLACK)
control_rect = control_surface.get_rect(centerx = goal_rect.centerx, top = goal_rect.bottom + 30)

stages_surface = instruction_font.render(stages_text, True, WHITE, BLACK)
stages_rect = stages_surface.get_rect(centerx = control_rect.centerx, top = control_rect.bottom + 30)

endless_surface = instruction_font.render(endless_text, True, WHITE, BLACK)
endless_rect = endless_surface.get_rect(centerx = stages_rect.centerx, top = stages_rect.bottom + 30)

"""
Load Images
"""


def spritesheet_breakdown(frames, spritesheet, start, row, length, width):
    """
    Breaks down a spritesheet horizontally into a list of frames for sprite animation.

    Parameters:
        frames (int): The number of images for the total animation.
        spritesheet (pygame.Surface): The original sprite to grab subsurfaces from.
        start (int): The diffrence in x coord of each frame.
        row (int): The y coord of all frames.
        length (int): The length of each frame.
        width (int): THe width of each frame.
    
    Returns:
        list: All the frames for animation in order.
    """

    #initialize the list of all frames
    all_frames = []

    #iterate over the number of frames and use subsurface dimensions to create animation frames
    for f in range(frames):
        image = spritesheet.subsurface(start * f, row, length, width)
        #add the frame to the other frames
        all_frames.append(image)
    
    return all_frames


#menu background
menu_background = pygame.image.load("images/menu_background.png").convert_alpha()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

#mars background
mars_background = pygame.image.load("images/mars.png").convert_alpha()
mars_background = mars_background.subsurface(0, 100, 1280, 1180)
mars_background = pygame.transform.scale(mars_background, (WIDTH, HEIGHT))

#star background
star_background = pygame.image.load("images/star_background.png").convert_alpha()
star_background = pygame.transform.scale(star_background, (1200, 1200))
star_background_rect = star_background.get_rect(center = (512, 200))

#base ground platforms
platform_spritesheet = pygame.image.load("images/red_tile_spritesheet.png").convert_alpha()
platform_spritesheet = pygame.transform.scale_by(platform_spritesheet, 4)
base_ground_platform = platform_spritesheet.subsurface(224, 592, 192, 192)

#floating platforms
#create a new surface for the area of the floating platform
platform = pygame.Surface((256, 48)).convert_alpha()
platform_spritesheet = pygame.transform.scale_by(platform_spritesheet, 0.5)
#main block
platform_tile = platform_spritesheet.subsurface(208, 192, 32, 32)
#decor under block
platform_under = platform_spritesheet.subsurface(144, 224, 64, 32)
platform_under = pygame.transform.scale_by(platform_under, 0.5)

#dog
dog_spritesheet = pygame.image.load("images/dog_spritesheet.png").convert_alpha()
dog_spritesheet = pygame.transform.scale_by(dog_spritesheet, 2)
#create list for the dog running animation
dog_running = spritesheet_breakdown(5, dog_spritesheet, 120, 146, 98, 72)

#enemies
#wall
enemy_wall = pygame.image.load("images/enemy_wall.png").convert_alpha()
enemy_wall = pygame.transform.scale_by(enemy_wall, 2.18)
enemy_wall = pygame.transform.rotate(enemy_wall, -90)
#void
enemy_void = pygame.image.load("images/void.png").convert_alpha()
enemy_void = pygame.transform.scale_by(enemy_void, 1.6)
#enemy_cat_rect
enemy_cat = pygame.image.load("images/cat.png").convert_alpha()
enemy_cat = pygame.transform.scale_by(enemy_cat, 2)
#enemy_cat_rect ship
cat_ship = pygame.image.load("images/boss_spaceship.png").convert_alpha()
cat_ship = pygame.transform.scale_by(cat_ship, 0.5)

#projectiles
#yarn
yarn = pygame.image.load("images/yarn.png").convert_alpha()
yarn = pygame.transform.scale_by(yarn, 0.72)
#lasers
laser_green = pygame.image.load("images/green_laser.png").convert_alpha()
laser_green = pygame.transform.scale_by(laser_green, 0.5)
laser_red = pygame.image.load("images/red_laser.png").convert_alpha()
laser_red = pygame.transform.scale_by(laser_red, 0.5)
laser_blue = pygame.image.load("images/blue_laser.png").convert_alpha()
laser_blue = pygame.transform.scale_by(laser_blue, 0.5)
#missile
missile = pygame.image.load("images/big_enemy_projectile.png").convert_alpha()
missile = pygame.transform.flip(missile, True, False)
missile = pygame.transform.scale_by(missile, 0.5)
#bomb
bomb = pygame.image.load("images/small_enemy_projectile.png").convert_alpha()
bomb = pygame.transform.scale_by(bomb, 0.65)

#screen tint
screen_tint = pygame.Surface((1024, 768)).convert_alpha()
screen_tint.fill((0, 0, 0, 150))

#bark effect
screen_bark = pygame.Surface((1024, 768)).convert_alpha()
screen_bark.fill((255, 255, 255, 0))


def game_initializations():
    """
    Initialize all variables for game and run one time fuctions
    """
    global game_state
    global start_time
    global global_dog_flip
    global global_jump
    global global_fall
    global global_on_platform
    global global_score
    global global_difficulty
    global mars_total_x_cut
    global star_angle
    global base_ground_locations
    global all_platform_tiles
    global all_platform_pos
    global last_platform_sector
    global final_dog_rect
    global dog_frame
    global last_dog_change
    global dog_velocity
    global dog_gravity
    global last_dog_bottom
    global last_bark_time
    global bark_cooldown
    global bark_active
    global bark_effect_tint
    global bark_dog_rect
    global last_score_change
    global boss_up
    global boss_down
    global boss_move_counter
    global boss_direction
    global boss_move_distance
    global enemy_cat_rect
    global enemy_wall_rect
    global enemy_void_rect
    global all_yarn_rects
    global all_yarn_movement
    global last_yarn_time
    global laser_rect
    global laser_color_switch
    global missile_rect
    global missile_offset_counter
    global all_bomb_rects
    global last_bomb_time
    global last_projectile_changes

    #game state
    game_state = PLAYING

    #time
    start_time = current_time

    #global variables
    global_dog_flip = True #True is dog facing right, False is dog facing left
    global_jump = False
    global_fall = False
    global_on_platform = False
    global_score = 0
    global_difficulty = 1

    #background and base ground variables
    mars_total_x_cut = 0
    star_angle = 0
    base_ground_locations = []

    #floating platform variables
    all_platform_tiles = [] #list of sprites to blit to platform
    all_platform_pos = [platform.get_rect(topleft = (1024, 466))]
    last_platform_sector = 1 #spawn platform on y coord depending on sector to create seperation
    
    #dog controls
    final_dog_rect = dog_running[1].get_rect(midbottom = (512, 576))
    dog_frame = 1
    last_dog_change = 0
    dog_velocity = 0
    dog_gravity = 0
    last_dog_bottom = 576
    last_bark_time = current_time
    bark_cooldown = 20
    bark_active = False
    bark_effect_tint = 255
    bark_dog_rect = dog_running[1].get_rect(topleft = (1150, 500))
    
    #text
    last_score_change = 255
    
    #boss
    boss_up = 1
    boss_down = 2
    boss_move_counter = 0
    boss_direction = boss_up
    boss_move_distance = 0
    enemy_cat_rect = enemy_cat.get_rect(midright = (WIDTH - 20, 288))
    
    #wall
    enemy_wall_rect = enemy_wall.get_rect(midbottom = (0, 576))
    enemy_void_rect = enemy_void.get_rect(topright = (25, 0))
    
    #projectiles
    all_yarn_rects = []
    all_yarn_movement = []
    last_yarn_time = 0
    laser_rect = laser_green.get_rect(bottomleft = (1200, 576))
    laser_color_switch = [laser_green, laser_red, laser_blue, 0]
    missile_rect = missile.get_rect(midright = (0, 500))
    missile_offset_counter = -25
    all_bomb_rects = [bomb.get_rect(midbottom = (800, 0))]
    last_bomb_time = 0
    last_projectile_changes = [last_yarn_time, last_bomb_time]

    #run one time fuctions

    #crate the starting locations for the base ground
    base_ground_placements()

    #create the floating platform by bliting images to it
    platform_creation(platform_tile, platform_under)


def game_over_conditions():
    """
    Test if collisions happen between the dog and enemies or projectiles to end the game.
    """

    global game_state

    #create new rect for dog for more accurate collisions
    if global_dog_flip == False:
        dog_head_rect = pygame.Rect(final_dog_rect.x + 4, final_dog_rect.y + 4, 16, 32)
        dog_body_rect = pygame.Rect(final_dog_rect.x + 16, final_dog_rect.y + 34, 48, 32)
    else:
        dog_head_rect = pygame.Rect(final_dog_rect.x + 78, final_dog_rect.y + 4, 16, 32)
        dog_body_rect = pygame.Rect(final_dog_rect.x + 30, final_dog_rect.y + 34, 48, 32)

    #test collision between wall and dog
    if enemy_wall_rect.colliderect(dog_head_rect) or enemy_wall_rect.colliderect(dog_body_rect):
        game_state = GAME_OVER

    #test collision between yarn and dog
    if game_state != GAME_OVER:
        for rect in all_yarn_rects:
            if rect.colliderect(dog_head_rect) or rect.colliderect(dog_body_rect):
                game_state = GAME_OVER

    #test collision between laser and dog
    if game_state != GAME_OVER:
        if laser_rect.colliderect(dog_head_rect) or laser_rect.colliderect(dog_body_rect):
            game_state = GAME_OVER

    #test collision between missile and dog
    if game_state != GAME_OVER:
        if missile_rect.colliderect(dog_head_rect) or missile_rect.colliderect(dog_body_rect):
            game_state = GAME_OVER

    #test collision between bomb and dog
    if game_state != GAME_OVER:
        for rect in all_bomb_rects:
            if rect.colliderect(dog_head_rect) or rect.colliderect(dog_body_rect):
                game_state = GAME_OVER


def bark_effect(tint):
    """
    Make the screen white and slowly make it more transparent when bark is active.

    Parameters:
        tint (int): The transparancy of the surface.

    Returns
        tuple: Contains the values for the new surface and the updated transparancy.
    """

    #create a solid white surface that gets more transparent while bark is active
    if bark_active:
        screen_bark.fill((255, 255, 255, tint))
        tint -= 4
    #default to no white surface while bark is not active
    else:
        tint = 255
        screen_bark.fill((255, 255, 255, 0))

    return screen_bark, tint


def bark(last_bark_time):
    """
    Handle bark activation and clear the screen of projectiles while bark is active.

    Parameters:
        last_bark_time (int): The last time bark was used.

    Returns:
        tuple: Contains updated value for when bark was used and updated display for bark cooldown.
    """
    global missile_offset_counter
    global bark_active

    #return True if left mouse button is clicked
    mouse_click = pygame.mouse.get_pressed()[0]

    #allows bark to be activated for 2 seconds every 20 seconds
    if (mouse_click and (current_time - last_bark_time > 20000)) or ((current_time - last_bark_time < 2000) and (current_time - start_time > 3000)):
        #reset all projectiles while bark is active for 2 seconds
        all_yarn_rects.clear()
        all_yarn_movement.clear()
        laser_rect.bottomleft = 1200, 576
        missile_rect.midright = 0, 500
        missile_offset_counter = -25
        all_bomb_rects.clear()
        bark_active = True
        if mouse_click and (current_time - last_bark_time > 20000):
            #update last bark time
            last_bark_time = current_time
    else:
        bark_active = False

    #to blit dog over everything while bark is active
    if bark_active:
        bark_dog_rect.center = final_dog_rect.center
    else:
        bark_dog_rect.center = 1150, 500

    #create a backwards timer from 20 to count bark cooldown
    bark_cooldown = 20 - ((current_time - last_bark_time) // 1000)

    #create text for cooldown
    if bark_cooldown < 1:
        bark_cooldown_text = "Bark Cooldown: Ready"
    else:
        bark_cooldown_text = f"Bark Cooldown: {bark_cooldown}"

    #render cooldown text
    bark_cooldown_surface = game_font.render(bark_cooldown_text, True, WHITE)

    return last_bark_time, bark_cooldown_surface


def yarn_projectile():
    """
    Control the movement of the yarn projectile.
    """

    #unpack list to get time of last yarn
    yarn_delay = last_projectile_changes[0]

    #extra movement for yarn if keyboard keys are pressed
    key_move = 0
    if keys[pygame.K_d]:
        key_move += 12
    if keys[pygame.K_a]:
        key_move += -12

    #create a new yarn if enough time has passed
    if current_time - yarn_delay > 1500:

        #start the yarn behind the enemy_cat_rect
        all_yarn_rects.append(yarn.get_rect(topleft = (enemy_cat_rect.left + 20, enemy_cat_rect.centery)))

        #get the last yarn
        current_yarn = all_yarn_rects[-1]

        #find the x and y diffrence between the yarn and dog
        x_diffrence = current_yarn.centerx - final_dog_rect.centerx
        y_diffrence = current_yarn.centery - final_dog_rect.centery

        #split the x and y diffrence into 75 sections
        x_yarn_movement_to_dog = x_diffrence // 75
        y_yarn_movement_to_dog = y_diffrence // 75

        #add the length of the 75 sections into a list
        all_yarn_movement.append((x_yarn_movement_to_dog, y_yarn_movement_to_dog))

        #update the yarn delay time
        yarn_delay = current_time
    
    #iterate over the yarn locations
    for move, pos in enumerate(all_yarn_rects):
        #move the yarn in specific corresponding segments so every yarn reaches the dog in 75 movements
        pos[0] -= (all_yarn_movement[move][0] * global_difficulty) + key_move
        pos[1] -= (all_yarn_movement[move][1] * global_difficulty)

        #delete the yarn and the corresponding movement if yarn goes off screen
        if pos[0] < 0 or pos[1] > 576:
            all_yarn_rects.remove(pos)
            all_yarn_movement.remove(all_yarn_movement[move])

    #put updated last yarn time back into list
    last_projectile_changes[0] = yarn_delay


def laser_projectile():
    """
    Control the movement of the laser projectile.
    """

    key_move = 0
    if keys[pygame.K_d]:
        key_move += 12
    if keys[pygame.K_a]:
        key_move += -12

    laser_rect.x -= (10 * global_difficulty) + key_move
    if laser_rect.right < 0:
        laser_color_switch[3] += 1
        laser_color_switch[3] %= 3
        laser_rect.left = 1024


def missile_projectile():
    """
    Control the movement of the missile projectile.
    """
    global missile_offset_counter

    #reset the missile if it goes off screen
    if missile_rect.left > 1024:
        y_location = random.randint(246, 528)
        missile_rect.y = y_location
        missile_rect.right = enemy_wall_rect.right

    #move the missile slow at first then speed it up once it passes the wall
    if missile_rect.left > enemy_wall_rect.right:
        missile_rect.x += (20 * global_difficulty)
        missile_offset_counter = -25
    else:
        missile_rect.right = enemy_wall_rect.right + missile_offset_counter
        missile_offset_counter += (1 * global_difficulty)


def bomb_projectile():
    """
    Control the movement of the bomb projectile.
    """
    
    #unpack list to get time of last bomb
    bomb_delay = last_projectile_changes[1]

    #move yarn in correlation with the ground
    key_move = 0
    if keys[pygame.K_d]:
        key_move += 12
    if keys[pygame.K_a]:
        key_move += -12

    #create a new bomb if enough time has passed
    if current_time - bomb_delay > (4000 / global_difficulty):
        x_location = random.randint(750, 900)
        all_bomb_rects.append(bomb.get_rect(midbottom = (x_location, 0)))
        #update the last bomb time
        bomb_delay = current_time
    
    if len(all_bomb_rects) >= 1:
        #only move the last bomb down
        all_bomb_rects[-1].y += (20 * global_difficulty)

    #initialize bomb fall
    fall = True

    if len(all_bomb_rects) >= 1:
        #iterate over the platform rects
        for pos in all_platform_pos:
            #stop bomb fall if the final bomb lands on a platform
            if pos.colliderect(all_bomb_rects[-1]):
                all_bomb_rects[-1].bottom = pos.top + 1
                fall = False

    #iterate over the bomb rects
    for pos in all_bomb_rects:
        #only move bombs horizontally with ground if they are on a platform
        if pos == all_bomb_rects[-1]:
            if fall == False:
                pos[0] -= key_move
        else:
            pos[0] -= key_move

        #remove bomb from list if it goes off screen
        if (pos[0] < 0 or pos[1] > 800) and len(all_bomb_rects) > 1:
            all_bomb_rects.remove(pos)

    #put updated last bomb time back into list
    last_projectile_changes[1] = bomb_delay


def boss_movement(move_counter, direction, move_distance):
    """
    Move the enemy_cat_rect and the enemy_cat_rect ship up or down randomly.

    Parameters:
        move_counter (int): The amount of times the enemy_cat_rect has moved.
        direction (int): The value to determine if the enemy_cat_rect moves up or down.
        move_distance (int): The total amount of times the enemy_cat_rect has to move.

    Returns:
        tuple: Contains updated values for the counter, distance, and direction. And the rectangle representing the enemy_cat_rect ship.
    """

    #choose a new path once the previous one is done
    if move_counter == 0:
        move_distance = random.randint(13, 70)
        direction = random.randint(1, 2)

    #change the enemy_cat_rect direction if it reaches top/bottom limits
    if enemy_cat_rect.bottom > 540:
        direction = boss_up
    if enemy_cat_rect.top < 50:
        direction = boss_down

    #move the enemy_cat_rect depending on the direction
    if direction == boss_up:
        enemy_cat_rect.y -= 3
    if direction == boss_down:
        enemy_cat_rect.y += 3

    #place the enemy_cat_rect ship directly below the enemy_cat_rect
    cat_ship_rect = cat_ship.get_rect(midtop = (enemy_cat_rect.centerx, enemy_cat_rect.bottom - 10))

    #update the counter each time the enemy_cat_rect moves
    move_counter += 1
    move_counter %= move_distance

    return move_counter, move_distance, direction, cat_ship_rect


def score_counter(delay):
    """
    Handles score related matters like difficulty and score display.

    Parameters:
        delay (int): The last time the score was changed.

    Returns:
        int: Contains updated value for last score change time.
    """
    global global_score
    global global_difficulty
    global global_highscore

    #update score every second
    if current_time - delay > 1000:
        global_score += 1
        delay = current_time

    if game_lv == ENDLESS:
        global_difficulty = ((global_score - 70) // 10) / 10
        global_difficulty += 1

    #update the score displayed
    score_text = f"Score: {global_score}"
    all_score_text[0] = game_font.render(score_text, True, WHITE)

    final_score_text = f"Final Score {global_score}"
    all_score_text[1] = over_font.render(final_score_text, True, WHITE)
    all_score_text[2] = all_score_text[1].get_rect(center = (WIDTH // 2, 500))

    if global_score > global_highscore:
        global_highscore = global_score

    highscore_text = f"Highscore {global_highscore}"
    all_score_text[3] = over_font.render(highscore_text, True, WHITE)
    all_score_text[4] = all_score_text[3].get_rect(center = (WIDTH // 2, 600))

    return delay


def platform_collision(last_bottom):
    """
    Test if there is collision between the dog and a floating platform to stop the dog from falling through.

    Parameters:
        last_bottom (int): The y coord of the bottom of the dog.

    Returns:
        int: The updated y coord of the bottom of the dog.
    """

    global global_on_platform

    #create a new rect around the dog to create more accurate collisions by eliminating excess rect from the dog tail
    if global_dog_flip == True:
        new_start = final_dog_rect.x + 26
        new_width = (final_dog_rect.right - final_dog_rect.x) - 26
        #create new rect with dimensions not including the tail length for dog looking right
        new_rect = pygame.Rect(new_start, final_dog_rect.y, new_width, (final_dog_rect.bottom - final_dog_rect.top))
    elif global_dog_flip == False:
        new_width = (final_dog_rect.right - final_dog_rect.x) - 26
        #create new rect with dimensions not including the tail length for dog looking left
        new_rect = pygame.Rect(final_dog_rect.x, final_dog_rect.y, new_width, (final_dog_rect.bottom - final_dog_rect.top))

    #reset dog to not be on platform
    global_on_platform = False

    #iterate over a list containing all floating platform rects
    for pos in all_platform_pos:
        #stop testing for collisions once dog is on a platform
        if global_on_platform == False:
            #update dog to be on platform if the bottom of dog equals top of platform, and if dog is coming from above
            if pos.colliderect(new_rect) and last_bottom < pos.top + 2:
                    final_dog_rect.bottom = pos.top + 1
                    global_on_platform = True

    #update the last bottom coord
    last_bottom = new_rect.bottom

    return last_bottom
    

def platform_movement(last_sector):
    """
    Controls the creation and movement of floating platforms depending on keyboard inputs.

    Parameters:
        last_sector (int): The sector a platform was set too.

    Returns:
        int: The updated sector for a new platform to be placed.
    """

    #iterate over all platform rects
    for pos in all_platform_pos:
        #move each platform right or left depending on inputs
        if keys[pygame.K_d]:
            pos.x -= 12
            if pos.right < 0:
                all_platform_pos.remove(pos)
        if keys[pygame.K_a]:
            pos.x += 12

    #create more platforms if further into the game
    if game_lv <= LEVEL_TWO:
        platform_creation_distance = 960
    else:
        platform_creation_distance = 1024

    #create a new platfrom once the last platfrom moves onto the screen
    if all_platform_pos[-1].centerx < platform_creation_distance:

        #set the sector to random number from 1-3 but not the same as the previous sector
        sector = random.randint(1, 3)
        while sector == last_sector:
            sector = random.randint(1, 3)

        #set each sector to a bool value
        sector_1 = sector == 1
        sector_2 = sector == 2
        sector_3 = sector == 3

        #get random y coord depending on sector for platform
        if sector_1:
            placement = random.randint(466, 528)
        if sector_2:
            placement = random.randint(356, 418)
        if sector_3:
            placement = random.randint(265, 308)

        #add the new platform rect to list
        all_platform_pos.append(platform.get_rect(topleft = (1024, placement)))

        return sector
    
    else:
        return last_sector
    

def platform_creation(tile, decor):
    """
    Blit multiple sprites to the floating platform surface for looks.

    Parameters:
        tile (pygame.Surface): The main block that takes up most of the platform.
        decor (pygame.Surface): Extra visuals for platform.
    """

    #make the surface transparent
    platform.fill((0, 0, 0, 0))

    #iterate over x to create coords for blocks in sequence
    for x in range(0, 225, 32):
        tile_coord = (x, 0)
        #add all the coords to a list
        all_platform_tiles.append(tile_coord)

    #iterate over list of block coords
    for pos in all_platform_tiles:
        #add the blocks and decor to the platform surface
        platform.blit(tile, pos)
        platform.blit(decor, (pos[0], pos[1] + 32))


def enemy_wall_movement(wall, void):
    """
    Move the wall enemy gradually towards the dog and depening on keyboard inputs.

    Paramaters:
        wall (pygame.Rect): The rect around the enemy wall sprite.
        void (pygame.Rect): The rect around the enemy void sprite.
    """

    #gradually move the wall/void towards the dog depending on given speed
    gradual_movement = 3
    wall.x += gradual_movement
    void.x += gradual_movement

    #move the wall/void to corelate with ground movements depending on keyboard inputs
    if keys[pygame.K_d]:
        wall.x -= 12
        void.x -= 12
    if keys[pygame.K_a]:
        wall.x += 12
        void.x += 12
 
    #limits the wall/void movement to the edge on the left of the screen
    if wall.centerx < 0:
        wall.centerx = 0
        void.right = 25


def falling_movement(gravity):
    """
    Moves the dog down if it is not on any ground.

    Parameters:
        gravity (int): The distance the dog moves downwards.

    Returns:
        int: The updated distance the dog moves downwards.
    """

    global global_fall
    
    #move dog downards if dog is not on ground
    if final_dog_rect.bottom < 576 and not(global_on_platform):
        #move dog downwards if dog is not jumping
        if not(global_jump):
            global_fall = True
            final_dog_rect.bottom += gravity
            #increase distance dog falls each time to give realistic effect
            gravity += 1
            #set the lowest point the dog can be
            if final_dog_rect.bottom > 576:
                final_dog_rect.bottom = 576
    else:
        global_fall = False
        #reset gravity if on ground
        gravity = 0

    return gravity


def dog_jump(velocity):
    """
    Increase the dog's height depending on keyboard input.

    Parameters:
        velocity (int): The distance the dog moves upwards.

    Returns:
        int: The updated distance the dog moves upwards.
    """

    global global_jump

    #allow a movement with input space if not already in jump and not falling
    if keys[pygame.K_SPACE] and global_jump == False and not(global_fall):
        global_jump = True
        #initialize movement distance
        velocity = 17

    #set distance dog moves if currently in jump
    if global_jump == True:
        #decrease distance dog moves each time to give realistic effect
        velocity -= 1
        #stop jump once dog reaches jump peak
        if velocity == 0:
            global_jump = False

    #move the dog upwards by the decreasing velocity
    final_dog_rect.bottom -= velocity
    
    return velocity


def dog_movement(frame, delay):
    """
    Create dog animation depending on keyboard inputs.

    Parameters:
        frame (int): The current frame in animation of the dog. Neutral dog is 1.
        delay (int): The time from the last frames change.

    Returns:
        tuple: Contains updated values for dog sprite visual, frame, and delay.
    """
    global global_dog_flip

    #flip dog according to the direction the game is moving
    if keys[pygame.K_d] and keys[pygame.K_a]:
        pass
    elif keys[pygame.K_d]:
        global_dog_flip = True
    elif keys[pygame.K_a]:
        global_dog_flip = False

    #allow a change in frame if anough time has passed
    if current_time - delay > 150:
        #if both a and d are pressed pause frame on neutral
        if (keys[pygame.K_d] and keys[pygame.K_a]) or not(keys[pygame.K_d] or keys[pygame.K_a]):
            if frame != 1:
                frame += 1
                frame %= 5
            final_dog = pygame.transform.flip(dog_running[frame], global_dog_flip, False)
        #increase frame by one if d or a is pressed
        elif keys[pygame.K_d] or keys[pygame.K_a]:
            frame += 1
            frame %= 5
            final_dog = pygame.transform.flip(dog_running[frame], global_dog_flip, False)
        #update the delay time
        delay = current_time
    #maintain frame if not enough time has passed
    else:
        final_dog = pygame.transform.flip(dog_running[frame], global_dog_flip, False)

    #set frame to 4 if dog is in air
    if (global_jump == True or global_fall == True) and not(global_on_platform):
        final_dog = pygame.transform.flip(dog_running[4], global_dog_flip, False)

    return final_dog, frame, delay


def base_ground_placements():
    """
    Calculate the first coords for the base ground sprites.
    """

    #iterate over the number of base platforms
    for ground_num in range(7):
        #calculate coords with a 192 pixel x diffrence each time
        new_ground = [192 * ground_num, 576]
        base_ground_locations.append(new_ground)


def base_ground_movement():
    """
    Move the base ground depending on keyboard input.
    """

    #move all base ground positions to the left if d is pressed
    if keys[pygame.K_d]:
        #iterate over all ground positions
        for pos in base_ground_locations:
            pos[0] -= 12
            #move ground section to far right if it goes off left screen
            if pos[0] < -192:
                pos[0] = 1140

    #move all base gorund positions to the right if a is pressed
    if keys[pygame.K_a]:
        #iterate over all ground positions
        for pos in base_ground_locations:
            pos[0] += 12
            #move ground section to far left if it goes off right screen
            if pos[0] > 1152:
                pos[0] = -180


def mars_background_movement(x_cut_pos):
    """
    Create a movement effect by spliting mars background depending on keyboard inputs.

    Parameters:
        x_cut_pos (int): Half the x coord for where to split the primary background.

    Returns:
        tuple: Contains updated values for where to split the image, one image for each side of the split, and location for the second image.
    """

    #move the split location depending on keyboard input.
    if keys[pygame.K_d]:
        x_cut_pos += 1
        if x_cut_pos > 511:
            x_cut_pos = 0
    if keys[pygame.K_a]:
        x_cut_pos -= 1
        if x_cut_pos < 0:
            x_cut_pos = 511

    #create a new image from primary background starting at the cut position
    primary_mars = mars_background.subsurface(2 * x_cut_pos, 0, 1024 - (2 * x_cut_pos), 768)

    #find the distance of the cut position from the right of the screen for the start of the second image
    second_start_point = 1024 - (2 * x_cut_pos)

    #create another new image from the primary background intil the cut position
    secondary_mars = mars_background.subsurface(0, 0, 2 * x_cut_pos, 768)
    #find the location for the second image
    secondary_mars_pos = (second_start_point, 0)
        
    return x_cut_pos, primary_mars, secondary_mars, secondary_mars_pos


def star_rotate(angle):
    """
    Rotate the star background in a circle.

    Parameters:
        angle (int): The amount in degrees to rotate the background.
        star_background (pygame.Surface): The image to rotate.
        start_rect (pygame.Rect): The rectangle to represent the location for the star background.

    Returns:
        tuple: The updated values for angle to rotate, the rotated image, and the rectangle for the location of the rotated image.
    """
   
    #rotate the primary image and create a rect around it
    rotated_star = pygame.transform.rotate(star_background, angle)
    rotated_star_rect = rotated_star.get_rect()

    #find the diffrence in the center of the rotated image and the primary image
    x_center_change = rotated_star_rect.centerx - star_background_rect.centerx
    y_center__change = rotated_star_rect.centery - star_background_rect.centery

    #move the rotated rect to align the center with the primary rect
    rotated_star_rect.x -= x_center_change
    rotated_star_rect.y -= y_center__change

    #update the angle to rotate
    angle += 0.5
    angle %= 360

    return angle, rotated_star, rotated_star_rect


def level_handler():
    """
    Handles which level the game is in.

    Returns:
        pygame.Surface: The text to be displayed for game level.
    """
    global game_lv

    if global_score < 10:
        game_lv = LEVEL_ONE
        next_level = 10

    elif global_score < 25:
        game_lv = LEVEL_TWO
        next_level = 25

    elif global_score < 45:
        game_lv = LEVEL_THREE
        next_level = 45

    elif global_score < 70:
        game_lv = LEVEL_FOUR
        next_level = 70

    else:
        game_lv = ENDLESS

    #create level realated text depending on level
    if game_lv == ENDLESS:
        level_text = "ENDLESS"
        next_level_text = ""
    else:
        level_text = f"Level {game_lv}"
        next_level_text = f"Next Level: {next_level} Score"
        if game_lv == LEVEL_FOUR:
            next_level_text = "Endless: 70 Score"
    
    level_surface = game_font.render(level_text, True, WHITE)

    next_level_surface = game_font.render(next_level_text, True, WHITE)

    return level_surface, next_level_surface


def handle_events():
    """
    Handles all pygame events.

    Returns:
        bool: Returns False if the game is to quit. Otherwise return True.
    """
    global game_state
    global keys
    global current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and (game_state == OPENING or game_state == GAME_OVER):
                game_initializations()
    
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    return True


def draw_opening_state():
    """
    Blit images for first screen when opening the game.
    """

    #background
    screen.blit(menu_background, (0, 0))

    #instruction text
    screen.blit(goal_surface, goal_rect)

    screen.blit(control_surface, control_rect)

    screen.blit(stages_surface, stages_rect)

    screen.blit(endless_surface, endless_rect)

    #start text
    screen.blit(start_surface, start_rect)


def draw_playing_state():
    """
    Blit all the images to the screen while playing.
    """

    #star background
    screen.blit(rotated_star_background, rotated_star_rect)

    #mars background
    screen.blit(mars_first_pic, (0, 0))
    screen.blit(mars_second_pic, mars_second_coord)

    #floating platforms
    for pos in all_platform_pos:
        screen.blit(platform, pos)

    #dog
    screen.blit(final_dog, final_dog_rect)

    #yarn
    for pos in all_yarn_rects:
        screen.blit(yarn, pos)

    #laser
    screen.blit(laser_color_switch[laser_color_switch[3]], laser_rect)

    #missile
    screen.blit(missile, missile_rect)

    #bomb
    for pos in all_bomb_rects:
        screen.blit(bomb, pos)

    #enemy_cat_rect ship
    screen.blit(cat_ship, cat_ship_rect)

    #enemy_cat_rect
    screen.blit(enemy_cat, enemy_cat_rect)

    #void
    screen.blit(enemy_void, enemy_void_rect)

    #wall
    screen.blit(enemy_wall, enemy_wall_rect)

    #base ground
    for pos in base_ground_locations:
        screen.blit(base_ground_platform, pos)

    #score text
    score_surface = all_score_text[0]
    
    screen.blit(score_surface, score_rect)

    #level text
    screen.blit(level_surface, level_rect)
    screen.blit(next_level_surface, next_level_rect)

    #bark bark_cooldown text
    screen.blit(bark_cooldown_surface, bark_cooldown_rect)

    #bark effect
    screen.blit(screen_bark, (0, 0))

    #reblit dog ontop of bark surface while bark is active
    screen.blit(final_dog, bark_dog_rect)
        

def draw_gameover_state():
    """
    Blit all images to screen once the game is over.
    """

    #star background
    screen.blit(rotated_star_background, rotated_star_rect)

    #mars background
    screen.blit(mars_first_pic, (0, 0))
    screen.blit(mars_second_pic, mars_second_coord)

    #floating platforms
    for pos in all_platform_pos:
        screen.blit(platform, pos)

    #dog
    screen.blit(final_dog, final_dog_rect)

    #enemy_cat_rect ship
    screen.blit(cat_ship, cat_ship_rect)

    #yarn
    for pos in all_yarn_rects:
        screen.blit(yarn, pos)

    #enemy_cat_rect
    screen.blit(enemy_cat, enemy_cat_rect)

    #laser
    screen.blit(laser_color_switch[laser_color_switch[3]], laser_rect)

    #missile
    screen.blit(missile, missile_rect)

    #bomb
    for pos in all_bomb_rects:
        screen.blit(bomb, pos)

    #void
    screen.blit(enemy_void, enemy_void_rect)

    #wall
    screen.blit(enemy_wall, enemy_wall_rect)

    #base ground
    for pos in base_ground_locations:
        screen.blit(base_ground_platform, pos)

    #screen tint
    screen.blit(screen_tint, (0, 0))

    #game over text
    screen.blit(game_over_surface, game_over_rect)

    #score text
    final_score_surface = all_score_text[1]
    final_score_rect = all_score_text[2]
    highscore_surface = all_score_text[3]
    highscore_rect = all_score_text[4]

    screen.blit(final_score_surface, final_score_rect)
    screen.blit(highscore_surface, highscore_rect)

    #play again text
    screen.blit(play_again_surface, play_again_rect)


# Define main loop
running = True
clock = pygame.time.Clock()  # Initialize clock object to cap frame rate

while running:
    running = handle_events()

    if game_state == PLAYING:
        level_surface, next_level_surface = level_handler()

        mars_total_x_cut, mars_first_pic, mars_second_pic, mars_second_coord = mars_background_movement(mars_total_x_cut)
       
        star_angle, rotated_star_background, rotated_star_rect = star_rotate(star_angle)
       
        base_ground_movement()
       
        final_dog, dog_frame, last_dog_change = dog_movement(dog_frame, last_dog_change)
       
        dog_velocity = dog_jump(dog_velocity)
       
        dog_gravity = falling_movement(dog_gravity)
       
        enemy_wall_movement(enemy_wall_rect, enemy_void_rect)
       
        last_platform_sector = platform_movement(last_platform_sector)
       
        last_dog_bottom = platform_collision(last_dog_bottom)
       
        boss_move_counter, boss_move_distance, boss_direction, cat_ship_rect = boss_movement(boss_move_counter, boss_direction, boss_move_distance)

        last_bark_time, bark_cooldown_surface = bark(last_bark_time)

        screen_bark, bark_effect_tint = bark_effect(bark_effect_tint)
       
        if game_lv >= LEVEL_ONE:
            yarn_projectile()

        if game_lv >= LEVEL_TWO:
            bomb_projectile()

        if game_lv >= LEVEL_THREE:
            laser_projectile()

        if game_lv >= LEVEL_FOUR:
            missile_projectile()
       
        game_over_conditions()

        last_score_change = score_counter(last_score_change)
       
        draw_playing_state()

    elif game_state == OPENING:
        draw_opening_state()

    elif game_state == GAME_OVER:
        draw_gameover_state()

    # Update display
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 fps

# Quit Pygame   
pygame.quit()
sys.exit()