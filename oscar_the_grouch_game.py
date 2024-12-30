"""
author: Harrison Yu
date: 07/22/2024
desc: oscar the grouch game
"""

from string import whitespace
#allows pygame to run
import pygame
#allows for random functions
import random 
#instiliaze all pygame modules
pygame.init()
#allows for font
pygame.font.init()

#set caption
pygame.display.set_caption("Oscar's Trash")

#GLOBALVAR
#allows manipulation of fps allowing for speed control
clock = pygame.time.Clock()
#set display size
time_frame = 20
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])
#set user score to 0 
score = 0
highscore = 0
#create sprite list for collosions and updates
obstacle_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()



# Define colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class game_obstacles(pygame.sprite.Sprite):
    def __init__(self):
        """
        Creating obstacles

        create sprite
        Create the building paramteres for each obstacle. First create 6 images and add them to a list.
        Then randomize picking from the list to create different random objects.
        Randomize the speed on the obstacles.
        Finally draw them onto the screen
        
        Args: (if needed) parameters
            self allows variable to be called upon outside of this function in the same class
		"""

        super().__init__()
        #convert images
        self.old_comp_image = pygame.image.load("old_comp.png").convert_alpha()
        self.batteries_image = pygame.image.load("batteries.png").convert_alpha()
        self.phone_image = pygame.image.load("broken_phone.png").convert_alpha()
        self.tv_image = pygame.image.load("broken_tv.png").convert_alpha()
        self.keyboard_image = pygame.image.load("keyboard.png").convert_alpha()
        self.mouse_image = pygame.image.load("mouse.png").convert_alpha()
        #add all images to a list
        self.image_list = [self.old_comp_image,self.batteries_image,self.phone_image,self.tv_image,self.keyboard_image,self.mouse_image]
        #randomly choose which one will be drawn
        self.image = self.image_list[random.randint(0,5)]
        self.rect = self.image.get_rect()
        #set the speed
        self.speed = random.randint(1,5)
        #draw them onto the screen
        screen.blit (self.image, (self.rect.x, self.rect.y))

    def position_reset(self):
        """
		Resets obstacles to the top
        
        Randomly reset obstacles to the top by setting y to -40 and randomizing again their x values 
        as well as randomizing their speeds again.
        
        Args: (if needed) parameters
            self
		"""
        #set y position
        self.rect.y = -40
        #set x position
        self.rect.x = random.randrange(0,670)
        #set speed for each obstacle again
        self.speed = random.randrange(1,3)
 
    def update(self):
        """
		Check to see if needs resetting
        
        If obstacle is off screen reset back to the top.
        
        Args: (if needed) parameters
            self
		"""
        self.rect.y += self.speed
        #check if obstacle has passed display size
        if self.rect.y > 704:
            #call on reseting position function and do it 
            self.position_reset()

class oscar_the_grouch(pygame.sprite.Sprite):
    def __init__(self):
        """
		Draw oscar
        
        create sprite
        convert image of oscar
        set its spawn point at (320,648)
        blit it on screen for usre to see
        
        Args: (if needed) parameters
            self
		"""
        super().__init__()
        #convert to alpha to allow transparency
        self.image = pygame.image.load("oscar_the_grouch.png").convert_alpha()
        self.rect = self.image.get_rect()   
        #allows for transparency
        self.image.set_colorkey(BLACK)
        #place it in the middle bottom of the display
        self.rect.x = 320
        self.rect.y = 648
        #draw onto the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self):
        """
		Player movement
        
        Check if keys are pressed
        If keys are pressed move character in direction by 3 pixels
        
        Args: (if needed) parameters
            self
		"""
        #create keys variable to check if key pressed
        keys = pygame.key.get_pressed()
        #if key pressed move in direction according to key pressed by 3 pixels
        if keys[pygame.K_w]:
            self.rect.y -= 3
        if keys[pygame.K_s]:
            self.rect.y += 3 
        if keys[pygame.K_a]:
            self.rect.x -= 3 
        if keys[pygame.K_d]:
            self.rect.x += 3
        if keys[pygame.K_1]:
            self.rect.x = 30
        if keys[pygame.K_2]:
            self.rect.x = 235
        if keys[pygame.K_3]:
            self.rect.x = 445
        if keys[pygame.K_4]:
            self.rect.x = 620
        if keys[pygame.K_SPACE]:
            self.rect.x = 330
            self.rect.y = 648
        #create new move image on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def boundary(self):
        """
		Creates boundary for oscar
        
        Check where oscar is
        if off screen teleport to opposite side 
        
        Args: (if needed) parameters
            self
		"""
        #check if oscar is on screen
        #if not set him to opposite side
        if self.rect.x < -45:
            self.rect.x = 730
        if self.rect.x > 730:
            self.rect.x = -35
        if self.rect.y > 648:
            self.rect.y = 648
        if self.rect.y < -50:
            self.rect.y = 700
    
        
def speed(score,time_frame):
    """
        Higher speed per score
        
        Everytime player meets new milestone set fps to higher making game faster and harder
        
        Args: (if needed) parameters
            self
            time_frame(int) - allows time_frame to be used to set the speed of program
		"""
    #check score
    #set fps to x to make it harder progressively
    if score >= 0:
        time_frame = 20
    if score >= 50:
        time_frame = 40
    if score >= 100:
        time_frame = 60
    if score >= 500:
        time_frame = 80
    if score >= 1000:
        time_frame = 100
    if score >= 1500:
        time_frame = 150
    if score >= 2000:
        time_frame = 200
    if score >= 2500:
        time_frame = 300
    if score >= 4000: 
        time_frame = 400
    return time_frame

def quit():
    """
		Quit game
        
        If user presses ESC quit pygame
		"""
    #create variable
    exit_key = pygame.key.get_pressed()
    #if ESC pressed quit game
    if exit_key[pygame.K_ESCAPE]:
        pygame.quit()

def pause_game():
    """
		Pause game
        
        If Q is pressed pause game loop and print PAUSED
        If W is pressed resume game again
		"""
    
    pause_key = pygame.key.get_pressed()
    #if q pressed start pause loop
    pause_active = True
    if pause_key[pygame.K_q]:
        pause_active = False
    while not pause_active:
        for event in pygame.event.get():
            pause_key = pygame.key.get_pressed()
           #print paused and controls guide
            font = pygame.font.SysFont('Calibri', 30, True, False)
            text = font.render("PAUSED",True,GREEN)
            screen.blit(text, [300, 320])
            font = pygame.font.SysFont('Calibri', 15, True, False)
            text = font.render("Q/E - PAUSE/RESUME",True,GREEN)
            screen.blit(text, [277, 350])
            #update screen
            US()
            quit()
            #if w pressed close this loop and resume main game loop
            if pause_key[pygame.K_e]:
                pause_active = True

def intro():
    """
		Intro screen
        
        Display intro and words
        If space pressed intro screen disappears
		"""
    start = False
    while not start:
        for event in pygame.event.get():
            start_key = pygame.key.get_pressed()
            # if space pressed stop this loop and carry on
            if start_key[pygame.K_SPACE]:
                start = True
            """if start_key[pygame.K_m]:        #mute/play button if wanted
                pygame.mixer.music.stop()
            if start_key[pygame.K_n]:
                pygame.mixer.music.play()"""
        quit()
        #pring text on screen
        font = pygame.font.SysFont('Calibri', 50, True, False)
        text = font.render("Oscar's Trash",True,GREEN)
        screen.blit(text, [172, 265-45])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("HELP OSCAR THE GROUGH CLEAN UP E-WASTE!",True,GREEN)
        screen.blit(text, [163, 310-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("USE WASD TO MOVE",True,GREEN)
        screen.blit(text, [270, 325-35]) 
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("1, 2, 3, 4, SPACE - TELEPORT",True,GREEN)
        screen.blit(text, [240, 340-35]) 
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("Q/E - PAUSE/RESUME",True,GREEN)
        screen.blit(text, [260, 355-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("Collect e-waste! (2 pt)",True,GREEN)
        screen.blit(text, [270, 370-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("Do not drop any! (-1.5 pt)",True,GREEN)
        screen.blit(text, [257, 385-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("Score < 0 = GAME OVER",True,GREEN)
        screen.blit(text, [250, 400-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("ESC - EXIT GAME",True,GREEN)
        screen.blit(text, [275, 415-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("NO REDOS!",True,GREEN)
        screen.blit(text, [295, 430-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("Press SPACE to continue",True,GREEN)
        screen.blit(text, [250, 460-35])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("The highest scoring individual will have the option to donate $250",True,GREEN)
        screen.blit(text, [120, 470])
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("for any enviornmental cause and recieve $50.",True,GREEN)
        screen.blit(text, [120, 485])
        #update screen use black and green to create blinking text
        US()
        pygame.time.delay(50)
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render("Press SPACE to continue",True,BLACK)
        screen.blit(text, [250, 460-35])
        US()
        quit()

def score_text(score):
    """
		print score
        
        Displays score in the top left for user to see
        
        Args: (if needed) parameters
            score(int): allows score outside to be used to print score on screen
		"""
    font = pygame.font.SysFont('Calibri', 15, True, False)
    x = 0
    y = 0
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (x,y))

def highscore_text(highscore):
    """
		print highscore
        
        Displays highscore in the top left for user to see
        
        Args: (if needed) parameters
            score(int): allows score outside to be used to print score on screen
		"""
    font = pygame.font.SysFont('Calibri', 15, True, False)
    x = 0
    y = 15
    score_text = font.render("Highscore: " + str(highscore), True, WHITE)
    screen.blit(score_text, (x,y))

def lost():
    """
		lost game
        
        If game is lost print high-score and forever pause game
		"""
    
    lost_key = pygame.key.get_pressed()
    #if q pressed start pause loop
    lost_active = True
    if score < 0:
        lost_active = False
    while not lost_active:
        for event in pygame.event.get():
           #print paused and controls guide
            font = pygame.font.SysFont('Calibri', 75, True, False)
            text = font.render("YOU LOST",True,GREEN)
            screen.blit(text, [160, 220])
            font = pygame.font.SysFont('Calibri', 15, True, False)
            text = font.render("PRESS ESC TO QUIT",True,GREEN)
            screen.blit(text, [267, 330])
            font = pygame.font.SysFont('Calibri', 35, True, False)
            text = font.render("HIGHSCORE: " + str(highscore),True,GREEN)
            screen.blit(text, [220, 290])
            #update screen
            US()
            quit()

def US():
    """
		Update screen

        Shorter function to allow screen updates instead of typing display flip all out
		"""
    pygame.display.flip()



#MAIN CODE
pygame.init()

#MUSIC
#load and play intro music
pygame.mixer.music.load("intro_music.mp3")
pygame.mixer.music.play()


#INTRO
#call intro function
intro()

#GLOBALVAR_TWO
#define oscar to oscar class
oscar = oscar_the_grouch()

#STOP INTRO MUSIC
pygame.mixer.music.stop()

#DRAW
#draw 30 obstacles using the obstacle class and randomising
for i in range(40):
    #call class to randomise parameters 
    obstacles = game_obstacles()
    #random spawn 
    obstacles.rect.x = random.randrange(0,680)
    obstacles.rect.y = -40
    #add all obstacles to list for furture collision and update usages
    obstacle_list.add(obstacles)
    all_sprites_list.add(obstacles)

#add oscar to sprite list
all_sprites_list.add(oscar)

#GAME LOGIC
done = False
# -------- MAIN PROGRAM LOOP -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #stop all musics
    pygame.mixer.music.stop
    
    screen.fill(BLACK)
 
    #update all sprites
    all_sprites_list.update()
    
    #set level using speed function
    level = speed(score,time_frame)
    
    #create oscar
    oscar

    #allows user input/processing/output movement
    oscar.update()

    #checks is oscar is within bounds
    oscar.boundary()

    #if oscar and obstacle sprite are collided add to list #of times
    obstacle_hit_list = pygame.sprite.spritecollide(oscar, obstacle_list, False)


    for obstacle in obstacle_hit_list:
        #check to see how many times collided and add to list
        score += 2
        #everytime collided load and play hit sound
        pygame.mixer.music.load("point_sound.mp3")
        pygame.mixer.music.play()
        #reset obstacle back to top for further gameplay
        obstacle.position_reset()


    for obstacle in obstacle_list: 
        #if obstacles hit y=704 score -1 
        if obstacle.rect.y == 704:      #704 was picked because different speeds cause different pixels they hit 
                                        #forced to spawn all ay y=-40 and calculate LCM to get 704 so that all obstacles no matter the 
                                        #speed will hit this level and reset
            score -= 1.5

    #print scores on screen
    score_text(score)
    highscore_text(highscore)

    #if game is lost display lost screen and pause game indefintely
    lost()

    #draw all sprites
    all_sprites_list.draw(screen)

    #set fps of game using level as score gets higher so does speed
    clock.tick(level)

    #update screen
    US()

    #pause game function called upon
    pause_game()
    
    #once score hits -1 and lower (multiple collisions at once) quit pygame entirely
    if score <= -1:
        pygame.quit()
    if score > highscore:
        highscore = score

    #call quit function to allow user to quit whenever wanted
    quit()