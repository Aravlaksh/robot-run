# Imports
import pygame
import random
import json


# Window settings
GRID_SIZE = 64
WIDTH = 20 * GRID_SIZE
HEIGHT = 15 * GRID_SIZE
TITLE = "Robot Run"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)

# Stages
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3



# Load fonts
font_xs = pygame.font.Font(None, 14)
font_md = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 32)
font_sm = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 24)
font_xl = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 96)
font_lg = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 64)
# Load images
hero_img = pygame.image.load('assets/images/characters/robot_idle.png').convert_alpha()





grass_dirt_img = pygame.image.load('assets/images/tiles/grass_dirt.png').convert_alpha()
platform_img = pygame.image.load('assets/images/tiles/block.png').convert_alpha()
dirt_img = pygame.image.load('assets/images/tiles/dirt.png').convert_alpha()
gem_img = pygame.image.load('assets/images/items/gem2.png').convert_alpha()

enemy_imgs = [pygame.image.load('assets/images/characters/enemy2a.png').convert_alpha(),
              pygame.image.load('assets/images/characters/enemy2b.png').convert_alpha()]
ghost_imgs = [pygame.image.load('assets/images/characters/ghost.png').convert_alpha(),
              pygame.image.load('assets/images/characters/ghost.png').convert_alpha()]
bat_imgs_rt = [pygame.image.load('assets/images/characters/bee.png').convert_alpha(),
               pygame.image.load('assets/images/characters/bee_fly.png').convert_alpha()]

bat_imgs_lt = [pygame.transform.flip(img, True, False) for img in bat_imgs_rt]

heart_img = pygame.image.load('assets/images/items/heart.png').convert_alpha()
flag_img = pygame.image.load('assets/images/tiles/door.png').convert_alpha()
pole_img = pygame.image.load('assets/images/tiles/locked_door.png').convert_alpha()
bg_img = pygame.image.load('assets/images/tiles/background.png').convert_alpha()

# Load sounds


# Game classes

class Enitity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2

    def apply_gravity(self):
        self.vy += gravity

        if self.vy > terminal_velocity:
            self.vy = terminal_velocity


class AnimatedEntity(Enitity):

    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])


        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.animation_speed = 8

    def set_image_list(self):
        self.images = self.images

    def animate(self):
        self.ticks += 1
        self.set_image_list()

        if self.ticks % self.animation_speed == 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0

            self.image = self.images[self.image_index]





class Hero(Enitity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

        self.speed = 5
        self.jump_power = 15
        self.vx = 0
        self.vy = 0

        self.gems = 0
        self.hearts = 3
        self.hurt_timer = 0
        self.score = 0

    def move_to(self, x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2
       
    def move_right(self):
    	self.vx = -self.speed
    	
    def move_left(self):
    	self.vx = self.speed

    def stop(self):
        self.vx = 0
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(hits) > 0:
            self.vy = -1 * self.jump_power


    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)


    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > world_width:
            self.rect.right = world_width


    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in hits:
            if self.hurt_timer == 0:
                self.hearts -= 1
                print(self.hearts)
                print('oof!')#Platy sound
                self.hurt_timer = 1.0 * FPS

            if self.rect.x < enemy.rect.x:
                self.vx = -70
            elif self.rect.x > enemy.rect.x:
                self.vx = 70

            if self.rect.y < enemy.rect.y:
                self.vy = -15
            elif self.rect.y > enemy.rect.y:
                self.vy = 15
        else:
            self.hurt_timer -=1
            if self.hurt_timer < 0:
                self.hurt_timer = 0




    
    def update(self):
        self.apply_gravity()
        self.check_world_edges()
        self.check_items()
        self.check_enemies()
        self.move_and_check_platforms()

       

class Gem(Enitity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


    def apply(self, character):
        character.gems +=1
        character.score +=10
        print(character.gems)

class Enemy(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        

        self.speed = 2
        self.vx = -1 * self.speed
        self.vy = 0


    def reverse(self):
        self.vx *= -1


    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.reverse()

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.reverse()

    def check_platform_edges(self):
        self.rect.y +=2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -=2

        must_reverse = True

        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()




    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.apply_gravity()
        self.check_platform_edges()
        self.animate()






class Bat(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

    def set_image_list(self):
        if self.vx > 0:
            self.images = bat_imgs_lt
        else:
            self.images = bat_imgs_rt


    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()

class Ghost(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)


    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()



class Platform(Enitity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Flag(Enitity):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        

# Helper functoins
def show_start_screen():
    text = font_xl.render(TITLE, True, BLACK)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

    text = font_sm.render('Press and Key to Start', True, BLACK)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_lose_screen():
    text = font_lg.render('Game Over', True, BLACK)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

    text = font_sm.render('Press R to restart', True, BLACK)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)


def show_level_complete_screen():
    text = font_lg.render('Level Complete', True, BLACK)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_hud():
    text = font_md.render('score:'+ str(hero.score), True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 16
    screen.blit(text, rect)

    screen.blit(gem_img,  [WIDTH - 128, 16])
    text = font_md.render(': ' + str(hero.gems), True, WHITE)
    rect = text.get_rect()
    rect.topleft = WIDTH -90, 16
    screen.blit(text, rect)

    for i in range(hero.hearts):
        x = i * 36
        y = 5
        screen.blit(heart_img, [x, y])

def start_game():
    global hero, stage, player

    player = pygame.sprite.GroupSingle()


    hero = Hero(0, 0, hero_img)



    stage = START


def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, WHITE, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, WHITE, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, WHITE)
            screen.blit(text, [adj_x, adj_y])




#setup
def start_level():
    global player, platforms, items, enemies, hero, goal, all_sprites
    global gravity, terminal_velocity
    global world_width, world_height


    player = pygame.sprite.GroupSingle()
    platforms = pygame.sprite.Group()
    items = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    #load level
    with open('assets/levels/world_1.json') as f:
        data = json.load(f)

    world_width = data['width'] * GRID_SIZE
    world_height = data['height']* GRID_SIZE

    for i, loc in enumerate(data['flag_locs']):
        if i == 0:
            goal.add(Flag(loc[0], loc[1], flag_img))
        else:
            goal.add(Flag(loc[0], loc[1], pole_img))

    for loc in data['grass_locs']:
        platforms.add(Platform(loc[0], loc[1], grass_dirt_img))

    for loc in data ['block_locs']:
        platforms.add(Platform(loc[0], loc[1], platform_img))

    for loc in data ['dirt_locs']:
        platforms.add(Platform(loc[0], loc[1], dirt_img))

    for loc in data ['gem_locs']:
        items.add(Gem(loc[0], loc[1], gem_img))

    for loc in data ['enemy_locs']:
        enemies.add(Enemy(loc[0], loc[1], enemy_imgs))

    for loc in data['bat_locs']:
        enemies.add(Bat(loc[0], loc[1], bat_imgs_lt))

    for loc in data['ghost_locs']:
        enemies.add(Ghost(loc[0], loc[1], ghost_imgs))

    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)

    all_sprites.add(player, platforms, items, enemies, goal)




#Physcias settings
    gravity = data['gravity']
    terminal_velocity = data['terminal_velocity']



# Game loop
running = True
grid_on = False


start_game()
start_level()

while running:

    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                grid_on = not grid_on

            elif stage == START:
                stage = PLAYING

            elif stage == PLAYING:
                if event.key == pygame.K_UP:
                    hero.jump()

            elif stage == LOSE:
                if event.key == pygame.K_r:
                    start_game()
                    start_level()









    pressed = pygame.key.get_pressed()
    if stage == PLAYING:
        if pressed[pygame.K_RIGHT]:
            hero.move_left()
        elif pressed[pygame.K_LEFT]:
            hero.move_right()
        else:
            hero.stop()

    
    # Game logic
    if stage == PLAYING:
        all_sprites.update()
        

        if hero.hearts ==0:
            stage = LOSE
        elif hero.reached_goal():
            stage = LEVEL_COMPLETE


            countdown = 2 * FPS
    elif stage == LEVEL_COMPLETE:
        countdown -= 1
        if countdown <= 0:
            start_level()
            stage = PLAYING
            
    if hero.rect.centerx < WIDTH //2:
        offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH //2 :
        offset_x = world_width - WIDTH
    else:
        offset_x = hero.rect.centerx - WIDTH // 2
    


        
    # Drawing code
    screen.fill(SKY_BLUE)
    screen.blit(bg_img, [0, 0])


    for sprite in all_sprites:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])

   
    show_hud()
    if stage == START:
        show_start_screen()
    elif stage == LOSE:
        show_lose_screen()
    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()
    if grid_on:
        draw_grid(offset_x)



    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

