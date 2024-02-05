'''
Names: Tsebaot Wabella, Emnet Mekonnen
CSC 201
Project 3

Use the alien to shoot meteors. Move the alien by clicking to the left and right of it.
To shoot press the spacebar.
If the alien shoots and dodges enough meteors before they escape, you win.
Click start button to begin the game, click yes or no when prompted to play again.

Assistance:
Our pair received no assistance on this project.
'''
from graphics2 import *
from button import *
import time
import random
import math

LASER_SPEED = 20  
METEOR_SPEED = 5
ALIEN_SPEED = 25
NUM_WIN = 20  
STALL_TIME = 0.05
THRESHOLD = 95


def distance_between_points(point1, point2):
    '''
    Calculates the distance between two points
    
    Params:
    point1 (Point): the first point
    point2 (Point): the second point
    
    Returns:
    the distance between the two points
    '''
    p1x = point1.getX()
    p1y = point1.getY()
    p2x = point2.getX()
    p2y = point2.getY()
    return math.sqrt((p1x - p2x)*(p1x - p2x) + (p1y - p2y) * (p1y - p2y))


def is_close_enough(alien_img, meteor_img):
    '''
    Determines if the alien is close enough to the meteor to say the alien
    caught the meteor.
    
    Params:
    alien_img (Image): the image of the alien
    meteor_img (Image): the image of the meteor
    
    Returns:
    True if the alien catches the meteor
    '''
    center_alien = alien_img.getCenter()
    center_meteor = meteor_img.getCenter()
    if distance_between_points(center_alien, center_meteor) < THRESHOLD :
        return True
    else:
        return False
        

def move_meteors(meteor_img_list):
    '''
    Moves every meteor one METEOR_SPEED unit down the window
    
    Params:
    meteor_img_list (list): the list of falling meteors
    '''
    for meteor in meteor_img_list:
        meteor.move(0, METEOR_SPEED)
        

def move_alien(window, alien_img):
    '''
    Each time the left arrow key is pressed the alien moves ALIEN_SPEED units left and
    each time the right arrow key is pressed the alien moves ALIEN_SPEED units right.
    
    window (GraphWin): the window where game play takes place
    alien_img (Image): the alien image
    '''
    width = alien_img.getWidth()
    height = alien_img.getHeight()
    
    click = window.checkMouse()
    
    if click != None:
        click_x = click.getX()
        click_y = click.getY()
        
        center_alien = alien_img.getCenter()
        alien_x = center_alien.getX()
        alien_y = center_alien.getY()
        
        
        alien_top = alien_y - 1/2 * height
        alien_bottom = alien_y + 1/2 * height
        alien_left = alien_x - width / 2
        alien_right = alien_x + width / 2
        
        # checks whether the click is to the left or right of alien image
        if click_y < alien_bottom and click_y > alien_top:
            if alien_left > click_x:
                alien_img.move(-ALIEN_SPEED, 0)
            elif alien_right < click_x:
                alien_img.move(ALIEN_SPEED, 0)
              

def add_meteor_to_window(window):
    '''
    Adds one meteor to the top of the window at a random location
    
    Params:
    window (GraphWin): the window where game play takes place
    
    Returns:
    the meteor added to the window
    '''
    x_location = random.randrange(40, 601)
    meteor = Image(Point(x_location, 0), 'meteor.gif')
    meteor.draw(window)
    return meteor

def meteorNotInScreen(meteor_y):
    '''
    Tests if the meteor went out of the screen
    
    Params:
    meteor_y: The y point of the meteor images
    
    Returns:
    True if the meteor went out of screen

    '''  
    if meteor_y >= 666:
        return True
    

def draw_laser(window, alien_img,laser_list):
    '''
    If spacebar is clicked the laser image gets drawn inside the window
    and the lasers get appended to a list.
    
    Params:
    window: window (GraphWin): the window where game play takes place
    alien_img(Image): the image of the alien
    laser_list(List): list of lasers that have shot
    '''
    # checks if space bar was clicked
    key = window.checkKey()
    if key.lower() == "space":
        alienX = alien_img.getCenter().getX()   #gets x coordinate of the alien image
        alienY = alien_img.getCenter().getY()   #gets y coordinate of the alien image
        laser = Image(Point(alienX, alienY), "laser.gif")
        laser.draw(window)
        laser_list.append(laser)
            
            
def move_laser(laser_img_list):
    '''
    Moves every laser one LASER_SPEED unit up the window
    
    Params:
    laser_img_list (list): the list of lasers being shot
    '''
    for laser in laser_img_list:
        laser.move(0, -LASER_SPEED)
    
          
def game_loop(window, alien):
    '''
    Loop continues to allow the meteors to fall and the alien to move
    until enough meteors escape or the alien shoots enough meteors to
    end the game.
    
    Params:
    window (GraphWin): the window where game play takes place
    alien (Image): the alien image
    '''
    point_text = Text(Point(590, 75), '0')
    point_text.setSize(16)
    point_text.setTextColor("white")
    point_text.draw(window)
    
    points = 0
    meteor_list = []
    laser_list = []
    while points < NUM_WIN:
        move_alien(window, alien)
        move_meteors(meteor_list)
        move_laser(laser_list)

        draw_laser(window, alien,laser_list)            
       
        if random.randrange(100) < 4:
            meteor = add_meteor_to_window(window)
            meteor_list.append(meteor)
            
        for meteor in meteor_list:
            if is_close_enough(alien, meteor):
                meteor.undraw()
                meteor_list.remove(meteor)
                alienX = alien.getCenter().getX()
                alien.move(666 - alienX ,0) # moves alien out of screen
                time.sleep(3)
                window.close()
                game_over_window()
                exit(1)
           
            meteor_Y = meteor.getCenter().getY()
                
            if meteorNotInScreen(meteor_Y):
                points = points - 1
                meteor.undraw()
                meteor_list.remove(meteor)
                point_text.setText(str(points))
                
            for laser in laser_list:
                if is_close_enough(laser, meteor):
                    points = points + 1
                    meteor.undraw()
                    meteor_list.remove(meteor)
                    laser.undraw()
                    laser_list.remove(laser)
                    point_text.setText(str(points))
       
        time.sleep(STALL_TIME)
        
    window.close()
    win_game_window()   
def create_instructions_window():
    '''
    Opens a window to display introduction and instructions for the game.
    The window will close once the user clicks on the screen.

    '''
    window = GraphWin("Instructions Window", 666,666)
    window.setBackground("black")
    intro = Text(Point(333, 30), 'Welcome to Meteor Hunter ')
    intro.setSize(25)
    intro.setTextColor("white")
    intro.draw(window)
    
    directions = Text(Point(333, 333), f'Your goal is to destroy all the meteors\n that are threatening your planet.\n\n To play the game, click left and right \n of the alien to move it. \n\n To shoot, you will need to click on the spacebar.\n\n You will need to destroy {NUM_WIN} meteors\n to save everyone.\n\n If you get hit by a meteor, the game will be over. \n\n Good Luck!!')
    directions.setSize(20)
    directions.setTextColor("white")
    directions.draw(window)
    
    #Buttons
    start_button = Button(Point(333, 600), 150, 50, "Click to start", "red")
    start_button.activate()
    start_button.draw(window)
    
    click = window.getMouse()
    while not start_button.isClicked(click):
        click = window.getMouse()    
   
    window.close()
        
def game_over_window():
    '''
    Opens a new window once the alien collides with a meteor.
    '''
    window = GraphWin("Game Over", 666,666)
    background = Image(Point(333,333), "gameover.gif")
    background.draw(window)
    #Yes or No buttons
    yes_button = Button(Point(200, 600), 150, 50, "YES", "white")
    yes_button.activate()
    yes_button.draw(window)
    
    no_button = Button(Point(450, 600), 150, 50, "NO", "white")
    no_button.activate()
    no_button.draw(window)
    
    click = window.getMouse()
    while (not yes_button.isClicked(click)) and (not no_button.isClicked(click)):
        click = window.getMouse()
        
    if yes_button.isClicked(click):
        window.close()
        main()
    elif no_button.isClicked(click):
        window.close()

    
def win_game_window():
    '''
    Opens a new window once {NUM_WIN} points have been reached.
    '''
    window = GraphWin("Winner!!!", 666,666)
    background = Image(Point(333,333), "win.gif")
    background.draw(window)
    # Yes or No button
    yes_button = Button(Point(200, 600), 150, 50, "YES", "white")
    yes_button.activate()
    yes_button.draw(window)
    
    no_button = Button(Point(450, 600), 150, 50, "NO", "white")
    no_button.activate()
    no_button.draw(window)
    
    click = window.getMouse()
    while (not yes_button.isClicked(click)) and (not no_button.isClicked(click)):
        click = window.getMouse()
        
    if yes_button.isClicked(click):
        window.close()
        main()
    elif no_button.isClicked(click):
        window.close()
            
def main():
    create_instructions_window()
    # setup the game
    
    window = GraphWin("Meteor Hunter", 666,666)
    window.setBackground("white")
    background = Image(Point(333,333), "background.gif")
    background.draw(window)
    directions = Text(Point(333, 650), 'Click left and right of the alien to move it.')
    directions.setSize(16)
    directions.draw(window)
    
    #point counter 
    points = Text(Point(540, 75), 'Points: ')
    points.setSize(16)
    points.setTextColor("white")
    points.draw(window)
    
    #alien image
    alien = Image(Point(333,580), "alien.gif")
    alien.draw(window)

    game_loop(window, alien)


main()