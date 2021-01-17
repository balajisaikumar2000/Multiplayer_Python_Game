import pygame                                                    #pygame module
pygame.font.init()                                               #initialize font (if we want to work with font's then we need to do this)
pygame.mixer.init()                                              #to work with Sounds 

WIDTH,HEIGHT  = 900,500                                          #width and height of output window
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))                   #it will set the window
pygame.display.set_caption("multiplayer game")                   #set's caption for the window i.e title


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER  =pygame.Rect(WIDTH//2-5,0,10,HEIGHT)                     #pygame.Rect will create rectangle-->(x,y,width of rectangle,height of rectangle)

BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/Grenade+1.mp3")    #it will produce sound when bullet interact with spaceship
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3") #it will produce sound when bullet emerges from the spaceship

HEALTH_FONT = pygame.font.SysFont('comicsans',40)                 #health text font
WINNER_FONT  = pygame.font.SysFont('comicsans',100)                #final winner text font

FPS = 60                                                           #frames per second(the number of frames per second shown when we move a object)
VEL = 5                                                            #speed of ship 
BULLET_VEL  = 7                                                 
MAX_BULLETS = 3                                                   #max bullets we can fire at a time 
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40                          #generally the image we render are large hence we defining the ship width and height and later we will convert them

YELLOW_HIT = pygame.USEREVENT + 1                                 #it is differentiating the two user events by mentioning user 1,and user 2
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_yellow.png")      #pygame.load("the image to be present on the screen")

#pygame.transform.rotate,scale are used to transform into different dimensions
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

SPACE = pygame.transform.scale(pygame.image.load("Assets/space.png"),(WIDTH,HEIGHT))    #we are pasting the background image at window size itself

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
        # WIN.fill(WHITE)
        WIN.blit(SPACE,(0,0))                                                     #blit(the image we want to show,starting points)
        pygame.draw.rect(WIN,BLACK,BORDER)                                        #we are drawing the rectangle to seperate the spaces of the spaceships



        red_health_text = HEALTH_FONT.render("Health:" + str(red_health),1,WHITE)          #renders the text we specify
        yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health),1,WHITE)    #renders the text we specify
        WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()- 10,10))               #blit(the image/text we want to show ,starting points)
        WIN.blit(yellow_health_text,(10,10))                  

        WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))                                  #yellow.x and yellow.y are the coardinates where we want to show the ship intislly at start of  the game
        WIN.blit(RED_SPACESHIP,(red.x,red.y))                          


#here we are drawing bullets as rectangles:-
        for bullet in red_bullets:
            pygame.draw.rect(WIN,RED,bullet,)              #rect(surface where we want to draw,color of that rect value,rect value) )

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN,YELLOW,bullet)

#NOTE:the most important part is display.update() ,every change in the code need to be updated regularly ,so this method should definetly called
        pygame.display.update()

#NOTE: these are events for red,yellow space ships,these are easily understable
def yellow_handle_movement(keys_pressed,yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:    #LEFT
            yellow.x -= VEL
        if keys_pressed[pygame.K_d]  and yellow.x + VEL + yellow.width < BORDER.x:    #RIGHT
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:    #UP
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -15:    #DOWN
            yellow.y += VEL

def red_handle_movement(keys_pressed,red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:    #LEFT
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT]  and red.x + VEL + red.width < WIDTH:    #RIGHT
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0:    #UP
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15:    #DOWN
            red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL                                  #bullet  will move from left to right
        if red.colliderect(bullet):                             #if red spaceship is collide with bullet
            pygame.event.post(pygame.event.Event(RED_HIT))      #red hit will happen
            yellow_bullets.remove(bullet)                          #the bullet will disappear when it collides with red spaceship
        elif bullet.x > WIDTH:                                   #if bullet  reaches the boundary line then also it will disappear
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL                                   #bullet will move from right to left
        if yellow.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def  draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)             #it will render the "text" with "WINNER_FONT" font
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))    #will draw the text to the window
    pygame.display.update()                                      #it's neeed to be updated
    pygame.time.delay(5000)                                    #the time till it displays

def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)          #this will create rectangle for the red spaceship
    yellow  =pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)      #this will create rectangle for the yellow spaceship
 
#initially the no.of bullets are zero
    red_bullets = [] 
    yellow_bullets = [] 

#healths are initialized
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run  = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():          #event.get() will retrieve all events
            if event.type == pygame.QUIT:          #if we click the close button in py window the game will be exited
                run = False
        # red.x += 1

#if any key is pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2-2,10,5)  #will create bullet which will eject from the center of the spaceship
                    yellow_bullets.append(bullet)                          #if we press the respective ctrl button the bullet will be append to the resepective lists
                    BULLET_FIRE_SOUND.play()                                #sound will be played

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y + red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
#if the event is related to the red the respective things will happen
            if event.type == RED_HIT:
                red_health  -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""                                    #intially the final output is kept empty

        if red_health <= 0:                                #if health points of red reduces to <= 0 ,yellow will win and will display "Yellow Wins"
            winner_text = "Yellow Wins"

        if yellow_health <= 0:                            #if health points of yelllow reduces to <= 0 ,red will win and will display "Red Wins"
            winner_text = "Red Wins"
        
        if winner_text != "":
            draw_winner(winner_text)                     #the text is passed to draw_winner()
            break                                        #will exit from the loop and game ends

#keys are pressed
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)     #it will call handle_bullets()

        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)    #it will call draw_window()

    pygame.quit()                                                     #exit for the game

if __name__ == "__main__":                #if  we run the file it will call main() automatically
    main()