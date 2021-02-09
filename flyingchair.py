import pygame, sys
from pygame.locals import *
import random

from mine_manager import MineManager
pygame.init()

# Skärmen
screen = pygame.display.set_mode((1200,800))

# KONSTANTER
FRICTION = 0.005
BRAKE = 0.07

# Avgör vilket spelläge som gäller för tillfället. Spelet ska börja med att visa menyn
gamestate = 'title_screen'

# Text
font = pygame.font.SysFont("Comic Sans MS", 70)

# Rita "startmenyn"
def draw_title_screen():
    textobjekt = font.render('Text till startmeny', 1, (255,255,0))
    screen.blit(textobjekt, (50, 300))

# Håller koll på minor!
mine_sprite = pygame.image.load('mine_sprite.png').convert_alpha()
mine_manager = MineManager(screen, mine_sprite)

# Player/Spelaren
player_sprite = pygame.image.load('player_sprite.png').convert_alpha()
player_position_x = 300
player_position_y = 300
player_velocity_x = 0
player_velocity_y = 0
player_hp = 100

# Ritar spelaren
def draw_player():
    screen.blit(player_sprite,(player_position_x, player_position_y))

# Undersöker om spelaren krockar med ett annat objekt.
# Returnerar True om krock, annars False.
def player_check_hit(other_hitbox):
    hitbox = player_sprite.get_rect()
    hitbox.x = player_position_x
    hitbox.y = player_position_y

    if hitbox.colliderect(other_hitbox):
        return True
    else:
        return False
    
# Styrning av spelaren
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
space_pressed = False
x_pressed = False


# Spel-loopen
    # Har något hänt? "events"
    # Uppdatera game state
    # Rita ut på skärmen
while True:

    # Ska startmenyn visas?
    if gamestate == 'title_screen':
        for event in pygame.event.get(): 

            #Om en knapp på tangentbordet trycks ned, ändra spelläget till running
            if event.type == KEYDOWN:
                gamestate = 'running'
        
        # Visa menyn
        draw_title_screen()
        pygame.display.update()


    # Körs spelet?
    elif gamestate == 'running':
  
        if random.randint(1, 50) == 1:
            mine_manager.create_mine()

        #For-loop - den där get() ger alltså en LISTA med händelser. Kolla vilken TYP
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #Om en knapp på tangentbordet trycks ned
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    left_pressed = True

                if event.key == K_RIGHT:
                    right_pressed = True
                
                if event.key == K_UP:
                    up_pressed = True
                
                if event.key == K_DOWN:
                    down_pressed = True

                if event.key == K_SPACE:
                    space_pressed = True

                if event.key == K_x:
                    x_pressed = True


            #Om en knapp på tangentbordet har släppts
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    left_pressed = False

                if event.key == K_RIGHT:
                    right_pressed = False

                if event.key == K_UP:
                    up_pressed = False

                if event.key == K_DOWN:
                    down_pressed = False

                if event.key == K_SPACE:
                    space_pressed = False

                if event.key == K_x:
                    x_pressed = False


        #Vilka knappar är nedtryckta just nu?
        if left_pressed:
            player_velocity_x -= 0.05
        if right_pressed:
            player_velocity_x += 0.1
        if up_pressed:
            player_velocity_y -= 0.03
        if down_pressed:
            player_velocity_y += 0.04

        # Broms!
        if space_pressed:
            player_velocity_x *= 1 - BRAKE
            player_velocity_y *= 1 - BRAKE

        # Minska hastigheten lite pga FRICTION
        player_velocity_x *= 1 - FRICTION
        player_velocity_y *= 1 - FRICTION

        # Ändra spelarens position - alltså FLYTTA SPELAREN
        player_position_x += player_velocity_x
        player_position_y += player_velocity_y
    
        # Om spelaren är för långt till höger: Flytta till vänster!
        if player_position_x > 1250:
            player_position_x = -100
            player_velocity_y += 0.01

        # Uppdaterar alla minor
        mine_manager.update()
        
        # Går igenom alla minor och undersöker om de krockar med spelaren
        for mine in mine_manager.mines:
            if player_check_hit(mine.hitbox()):
                mine_manager.remove_mine(mine)


        #Rita på skärmen

        if not x_pressed:
            #            R  G  B
            screen.fill((0, 0, 0))

        # Ritar spelaren
        draw_player()
        
        # Ritar alla minor
        mine_manager.draw()

        pygame.display.update()