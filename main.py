import time
import pygame
import numpy as np

#https://www.youtube.com/watch?v=cRWg2SWuXtM
#Will add my own components to this project.
#Planned: Way to control tick rate, reset screen, and possibly more

COLOR_BACKGROUND = (150,30,140)
COLOR_GRID = (40,40,40)
COLOR_DIE = (170,170,170)
COLOR_ALIVE = (255,255,255)

SCREEN_SIZE = (800, 600)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row,col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = COLOR_BACKGROUND if cells[row, col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE
            elif 2 <= alive <=3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        else:
            if alive ==3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
        

    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Conway's Game of Life")


    sleeptime = .001
    
    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.update()

    running = False

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if running:
                        sleeptime = .001 #on pause, resets the tick rate because slow ticks means slower click input
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
                
                pressed = pygame.key.name(event.key)

                if pressed == 'r': #clear screen
                    cells = np.zeros((60, 80))
                    update(screen, cells, 10)
                    pygame.display.update()

                if pressed == 'q': #decrease tickrate
                    sleeptime += .025

                if pressed == 'w': #increase tickrate
                    if sleeptime > 0.001: sleeptime -= .025

                

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress = True)
            pygame.display.update()

        time.sleep(sleeptime)

if __name__ == '__main__':
    main()