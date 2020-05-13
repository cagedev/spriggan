"""
 A python implementation of Conway's Game of Life in Python/Pygame
"""
import pygame
import math

PALETTE = [
            (255, 255, 255),
            (  0,   0,   0),
            (  0, 255,   0),
            (255,   0,   0)
          ]

PIXEL_SIZE = 20
PIXEL_MARGIN = 5

GRID_SIZE_X = 60
GRID_SIZE_Y = 40

petri_old = [[0 for x in range(GRID_SIZE_X)] for y in range(GRID_SIZE_Y)]
petri_old[10][1] = 1 # y,x
petri_new = [y[:] for y in petri_old]

pygame.init()

WINDOW_SIZE = (255, 255)
screen = pygame.display.set_mode([
    GRID_SIZE_X*(PIXEL_SIZE+PIXEL_MARGIN)+PIXEL_MARGIN,
    GRID_SIZE_Y*(PIXEL_SIZE+PIXEL_MARGIN)+PIXEL_MARGIN,
    ])
pygame.display.set_caption("Game of Life")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # we hadden hier ook een break kunnen gebruiken
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            col = pos[0] / (PIXEL_SIZE+PIXEL_MARGIN)
            row = pos[1] / (PIXEL_SIZE+PIXEL_MARGIN)
            petri_new[math.floor(row)][math.floor(col)] = 1
            print("mouseclick(", pos, ") -> (", row,",", col, ")")

    screen.fill( PALETTE[0] )

    for j in range(GRID_SIZE_Y):
        for i in range(GRID_SIZE_X):
            pygame.draw.rect(
                screen, PALETTE[ petri_new[j][i] ],
                [(PIXEL_SIZE+PIXEL_MARGIN) * i + PIXEL_MARGIN,
                 (PIXEL_SIZE+PIXEL_MARGIN) * j + PIXEL_MARGIN,
                 PIXEL_SIZE, PIXEL_SIZE])

    clock.tick(60) # max 60 fps
    pygame.display.flip()

pygame.quit()
