import pygame

pygame.init()
width = 350
height = 200

#make the pygame window
pygame.display.set_mode((width, height ) )

running = True

while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
