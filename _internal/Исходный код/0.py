import os, random, math
 
import pygame
 
pygame.init()
 
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
 
x,y = 100,100
dx,dy = 0,0
vx,vy = 0,0 
speed = 100
draw = False
run = True 
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        if event.type == pygame.MOUSEBUTTONUP:
            draw = False
        if event.type == pygame.MOUSEMOTION:
            vx, vy = pygame.mouse.get_pos()
    if draw:            
        dx,dy = (vx - x)/speed,(vy - y)/speed
        x += dx
        y += dy
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,0,0),(x,y),10)    
    pygame.display.flip()
    clock.tick(100)
 
pygame.quit()
