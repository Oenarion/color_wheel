import pygame
import colorsys
import math
from graphical_components import Slider, NumberInput

def draw_color_wheel(surface, center, radius, alpha):
    """
    Draws the color wheel on the given surface.
    """
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
                int(b_col * 255),
                int(alpha)
            ))


def current_color(r, g, b, radius, cx, cy, screen):
    """
    Draws a circle on the color wheel indicating the current color.
    """
    hue, sat, _ = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    angle = hue * 360
    r = sat * radius
    x = int(cx + r * math.cos(math.radians(angle)))
    y = int(cy + r * math.sin(math.radians(angle)))
    pygame.draw.circle(screen, (200, 200, 200), (x, y), 5, width=2)

def draw_value_slider(screen, x, y, width, height, r, g, b):
    """
    Disegna lo slider verticale della Value (luminosità) per il colore dato.
    Restituisce la lista dei colori per ogni posizione verticale.
    """
    hue, sat, val = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    rgb_values = []
    for i in range(height):
        v = 1 - i / height  # dall'alto (1.0) al basso (0.0)
        r_col, g_col, b_col = colorsys.hsv_to_rgb(hue, sat, v)
        r_col, g_col, b_col = int(r_col*255), int(g_col*255), int(b_col*255)
        pygame.draw.line(screen, (r_col, g_col, b_col), (x, y+i), (x+width, y+i))
        rgb_values.append((r_col, g_col, b_col))

    # cursore basato sul "val" attuale
    cursor_y = int(y + (1 - val) * height)
    pygame.draw.rect(screen, (255, 255, 255), (x-2, cursor_y-2, width+4, 4), 2)

    return rgb_values

def handle_value_slider_click(mouse_pos, y, height, rgb_values):
    """
    Returns new RGB values based on mouse click/drag on the vertical slider.
    """
    _, my = mouse_pos

    # Compute value from y
    val = 1 - ((y - my) / height)  # top = 1, bottom = 0
    val = int(val*height)
    r_new, g_new, b_new = rgb_values[val]
    return r_new, g_new, b_new


def change_rgb_with_click(radius, cx, cy):
    """
    Changes the RGB values based on mouse position on the color wheel.
    """
    x, y = pygame.mouse.get_pos()
    dx, dy = x - cx, y - cy
    r = math.sqrt(dx*dx + dy*dy)
    if r > radius:
        r = radius

    # compute angle
    angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

    # HSV computation
    hue = angle / 360.0
    sat = r / radius
    val = 1.0

    r_col, g_col, b_col = colorsys.hsv_to_rgb(hue, sat, val)
    r_col = int(r_col * 255)
    g_col = int(g_col * 255)    
    b_col = int(b_col * 255)

    return r_col, g_col, b_col 

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

    text_color = font.render('Color', True, (255, 255, 255))
    text_rect_color = text_color.get_rect(center=(600, 500))
    screen.blit(text_color, text_rect_color)

def draw_graphical_components(components, screen):
    for component in components:
        component.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 30)
    
    radius, cx, cy = 230, 250, 300

    input_box_r = NumberInput(x=650, y=85, width=80, height=30, color=(0,0,0), font=font)
    input_box_g = NumberInput(x=650, y=185, width=80, height=30, color=(0,0,0), font=font)
    input_box_b = NumberInput(x=650, y=285, width=80, height=30, color=(0,0,0), font=font)
    slider = Slider(x=650, y=395, width=100, height=10, min_val=0, max_val=255, initial_val=255, font=font, interval=1)
    components = [input_box_r, input_box_g, input_box_b, slider]
    current_slider_value = 255
    
    # Pre-render color wheel
    color_wheel_surface = pygame.Surface((560, 560), pygame.SRCALPHA)
    draw_color_wheel(color_wheel_surface, (cx, cy), radius, current_slider_value)  

    pygame.display.set_caption("Color Wheel")
    running = True
    start_drag = False
    
    rgb_values = []

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

            if event.type == pygame.MOUSEBUTTONDOWN:    
                mx, my = pygame.mouse.get_pos()
                if mx < 480:
                    start_drag = True
                if 500 <= mx <= 520 and 100 <= my < 500:
                    r, g, b = handle_value_slider_click((mx, my), y=500, height=400, rgb_values=rgb_values)
                    input_box_r.text = str(r)
                    input_box_g.text = str(g)
                    input_box_b.text = str(b)
                    input_box_r.txt_surface = font.render(input_box_r.text, True, input_box_r.color)
                    input_box_g.txt_surface = font.render(input_box_g.text, True, input_box_g.color)
                    input_box_b.txt_surface = font.render(input_box_b.text, True, input_box_b.color)

            if event.type == pygame.MOUSEBUTTONUP:
                start_drag = False
                        
            # components event handling
            input_box_r.handle_event(event)
            input_box_g.handle_event(event)
            input_box_b.handle_event(event)
            slider.handle_event(event)

            slider_value = slider.current_val
            if slider_value != current_slider_value:
                current_slider_value = slider_value

        screen.fill((20, 20, 20))

        temp_surface = color_wheel_surface.copy()
        temp_surface.set_alpha(current_slider_value)
        screen.blit(temp_surface, (0, 0))

        if start_drag:
            r, g, b =change_rgb_with_click(radius, cx, cy)  
            input_box_r.text = str(r)
            input_box_g.text = str(g)
            input_box_b.text = str(b)
            input_box_r.txt_surface = font.render(input_box_r.text, True, input_box_r.color)
            input_box_g.txt_surface = font.render(input_box_g.text, True, input_box_g.color)
            input_box_b.txt_surface = font.render(input_box_b.text, True, input_box_b.color)

        if not input_box_r.active and not input_box_g.active and not input_box_b.active:
            current_color(int(input_box_r.text), int(input_box_g.text), int(input_box_b.text), 
                          radius, cx, cy, screen)
            
            # We need to use a surface because pygame.draw.rect does not support alpha
            pygame.draw.rect(screen, (255, 255, 255), (648, 483, 104, 34), width=2)
            color_rect_surface = pygame.Surface((100, 30), pygame.SRCALPHA)
            color_rect_surface.fill((
                int(input_box_r.text),
                int(input_box_g.text),
                int(input_box_b.text),
                current_slider_value
            ))
            screen.blit(color_rect_surface, (650, 485))

            rgb_values = draw_value_slider(screen, x=500, y=100, width=20, height=400, 
                  r=int(input_box_r.text), 
                  g=int(input_box_g.text), 
                  b=int(input_box_b.text))
        else:
            # Highlight color preview border if any input box is active
            pygame.draw.rect(screen, (100, 100, 100), (648, 483, 104, 34), width=2)
        

        text_blitting(screen, font)
        draw_graphical_components(components, screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()