import pygame, sys
from pygame.locals import *
import random

pygame.init()

#Skärmen
screen = pygame.display.set_mode((1200,800))

#KONSTANTER
FRICTION = 0.005
BRAKE = 0.07

# Player/Spelaren
player_sprite = pygame.image.load('player_sprite.png')
player_position_x = 300
player_position_y = 300
player_velocity_x = 0
player_velocity_y = 0

def draw_player():
    screen.blit(player_sprite,(player_position_x, player_position_y))

# Styrning
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
space_pressed = False

# Spel-loopen
    # Har något hänt? "events"
    # Uppdatera game state
    # Rita ut på skärmen
while True:


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
 
    #Rita på skärmen
#                R   G  B
    screen.fill((0,0,0))
    draw_player()

    pygame.display.update()