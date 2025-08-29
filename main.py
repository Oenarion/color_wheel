import pygame
import colorsys
import math
import numpy as np
from graphical_components import Slider, NumberInput



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

def text_blitting(screen, font):
    text_r = font.render('Red', True, (255, 0, 0))
    text_rect_r = text_r.get_rect(center=(595, 100))    
    screen.blit(text_r, text_rect_r)

    text_g = font.render('Green', True, (0, 255, 0))
    text_rect_g = text_g.get_rect(center=(605, 200))    
    screen.blit(text_g, text_rect_g)

    text_b = font.render('Blue', True, (0, 0, 255))
    text_rect_b = text_b.get_rect(center=(598, 300))   
    screen.blit(text_b, text_rect_b)

    text_a = font.render('Alpha', True, (255, 255, 255))
    text_rect_a = text_a.get_rect(center=(604, 400))
    screen.blit(text_a, text_rect_a)

def draw_graphical_components(components, screen):
    for component in components:
        component.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 30)
    
    # Pre-render color wheel 
    color_wheel_surface = pygame.Surface((560, 560), pygame.SRCALPHA)
    draw_color_wheel(color_wheel_surface, (280, 300), 250)  

    input_box_r = NumberInput(650, 85, 80, 30, (0,0,0), font)
    input_box_g = NumberInput(650, 185, 80, 30, (0,0,0), font)
    input_box_b = NumberInput(650, 285, 80, 30, (0,0,0), font)
    slider = Slider(650, 395, 100, 10, 0, 255, 1, font, interval=1)
    components = [input_box_r, input_box_g, input_box_b, slider]

    pygame.display.set_caption("Color Wheel")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Switch active input box with TAB
                if event.key == pygame.K_TAB:
                    if input_box_r.active:
                        input_box_r.active = False
                        input_box_g.active = True
                    elif input_box_g.active:
                        input_box_g.active = False
                        input_box_b.active = True
                    elif input_box_b.active:
                        input_box_b.active = False
                        

            # components event handling
            input_box_r.handle_event(event)
            input_box_g.handle_event(event)
            input_box_b.handle_event(event)
            slider.handle_event(event)

        screen.fill((0, 0, 0))
        screen.blit(color_wheel_surface, (0, 0))
        text_blitting(screen, font)
        draw_graphical_components(components, screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()