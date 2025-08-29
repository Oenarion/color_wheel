import pygame
import colorsys
import math
import numpy as np

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def draw_color_wheel(surface, center, radius):
    cx, cy = center
    w, h = surface.get_size()

    for y in range(h):
        for x in range(w):
            # computing radius
            dx, dy = x - cx, y - cy
            r = math.sqrt(dx*dx + dy*dy)

            # sanity check
            if r > radius:
                surface.set_at((x, y), (0, 0, 0, 0))  
                continue

            # compute angle
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

            # HSV computation
            hue = angle / 360.0
            sat = r / radius
            val = 1.0

            r_col, g_col, b_col = colorsys.hsv_to_rgb(hue, sat, val)

            surface.set_at((x, y), (
                int(r_col * 255),
                int(g_col * 255),
                int(b_col * 255)
            ))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    surface = pygame.Surface((800,600), pygame.SRCALPHA)
    pygame.display.set_caption("Color Wheel")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_color_wheel(screen, (300, 300), 250)
        pygame.display.flip()


    

if __name__ == "__main__":
    main()