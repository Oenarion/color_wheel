import pygame
import math

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def draw_color_wheel(surface):
    
    center = (300, 300)
    radius = 200
    step = 1


    for angle in range(0, 360, step):
        for r in range(radius, -1, -1):
            # x = int(center[0] + r * math.cos(math.radians(angle)))
            # y = int(center[1] + r * math.sin(math.radians(angle)))
            # alpha = int((r / radius) * 255)


            # RED COMPUTATION
            if angle >= 210 and angle <= 330:
                red = 255
            elif (150 < angle < 210) or (angle < 30) or (angle > 330):
                if (angle < 30):
                    new_angle = map_range(angle, 0, 30, 45, 90)
                    red = 255 * math.cos(math.radians(new_angle))
                elif angle > 315:
                    new_angle = map_range(angle, 330, 360, 0, 45)
                    red = 255 * math.cos(math.radians(new_angle))
                else:
                    new_angle = map_range(angle, 150, 210, 0, 90)
                    red = 255 * math.sin(math.radians(new_angle))
                    
            else:
                red = 0

            # GREEN COMPUTATION
            if angle >=330 or angle <= 90:
                green = 255
            elif (angle > 270 and angle < 330) or (angle < 150):
                if angle < 150:
                    new_angle = map_range(angle, 90, 150, 0, 90)
                    green = 255 * math.cos(math.radians(new_angle))
                else:
                    new_angle = map_range(angle, 270, 330, 0, 90)
                    green = 255 * math.sin(math.radians(new_angle))

            else:
                green = 0

            # BLUE COMPUTATION
            if 90 <= angle <= 210:
                blue = 255
            elif (210 < angle < 270) or (30 < angle < 90):
                if angle < 135:
                    new_angle = map_range(angle, 30, 90, 0, 90)
                    blue = 255 * math.sin(math.radians(new_angle))
                else:
                    new_angle = map_range(angle, 210, 270, 0, 90)
                    blue = 255 * math.cos(math.radians(new_angle))
            else:
                blue = 0

            if r == 0:
                red, green, blue = 255, 255, 255

            color = (int(red), int(green), int(blue))
            
            # calcolo vertici dello spicchio
            angle_rad1 = math.radians(angle)
            angle_rad2 = math.radians(angle + step)

            x1 = int(center[0] + r * math.cos(angle_rad1))
            y1 = int(center[1] + r * math.sin(angle_rad1))
            x2 = int(center[0] + r * math.cos(angle_rad2))
            y2 = int(center[1] + r * math.sin(angle_rad2))

            # spicchio = triangolo [centro, punto1, punto2]
            pygame.draw.polygon(surface, color, [center, (x1, y1), (x2, y2)])

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
        draw_color_wheel(screen)
        pygame.display.flip()

    # color_wheel = pygame.draw.circle(screen, (255, 255, 255), (300, 300), 250)

    # r_max = pygame.draw.circle(screen, (255, 0, 0), (300, 50), 5)
    # g_max = pygame.draw.circle(screen, (0, 255, 0), (550, 300), 5)
    # b_max = pygame.draw.circle(screen, (0, 0, 255), (300, 550), 5)

    

if __name__ == "__main__":
    main()