import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, font,toggle=True, interval=0.1, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.interval = interval
        self.label = label

        self.handle_width = 20
        self.handle_height = height + 10
        self.handle_color = (200, 200, 200, 180)  # semi-transparent
        self.track_color = (100, 100, 100, 180)   # semi-transparent
        self.font = font

        self.current_val = initial_val
        self.calculate_handle_position()

        self.toggle = toggle
        self.is_dragging = False
        

    def calculate_handle_position(self):
        normalized = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + normalized * (self.rect.width - self.handle_width)
        self.handle_rect = pygame.Rect(
            self.handle_x,
            self.rect.y - (self.handle_height - self.rect.height) // 2,
            self.handle_width,
            self.handle_height
        )

    def invert_toggle(self):
        self.toggle = not self.toggle

    def draw(self, screen):
        if self.toggle:
            # Draw semi-transparent track and handle
            track_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(track_surface, self.track_color, track_surface.get_rect())
            screen.blit(track_surface, self.rect.topleft)

            handle_surface = pygame.Surface((self.handle_width, self.handle_height), pygame.SRCALPHA)
            pygame.draw.rect(handle_surface, self.handle_color, handle_surface.get_rect())
            screen.blit(handle_surface, self.handle_rect.topleft)

            # Draw label above the slider
            label_text = self.font.render(self.label, True, (255, 255, 255))
            screen.blit(label_text, (self.rect.x, self.rect.y - 30))

            # Draw current value to the right
            val_text = self.font.render(f"{self.current_val}", True, (255, 255, 255))
            screen.blit(val_text, (self.rect.right + 10, self.rect.y - 5))

    def handle_event(self, event):
        if not self.toggle:
            return self.current_val

        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            mouse_x = max(self.rect.x, min(event.pos[0], self.rect.right - self.handle_width))
            normalized = (mouse_x - self.rect.x) / (self.rect.width - self.handle_width)
            self.current_val = int(round((self.min_val + normalized * (self.max_val - self.min_val)) / self.interval) * self.interval)
            self.calculate_handle_position()
        elif event.type == pygame.KEYDOWN and self.handle_rect.collidepoint(pygame.mouse.get_pos()):
            if event.key == pygame.K_LEFT:
                self.current_val = int(max(self.min_val, self.current_val - 1))
            if event.key == pygame.K_RIGHT:
                self.current_val = int(min(self.max_val, self.current_val + 1))
        return self.current_val
    

class NumberInput:
    def __init__(self, x, y, width, height, color, font, initial_text="0"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.font = font
        self.text = initial_text
        self.active = False  # se l'input è attivo per la scrittura

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif not self.active:
            if self.text == "":
                self.text = "0"
                
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Delete last character
            elif event.unicode.isdigit():
                new_text = self.text + event.unicode
                
                if new_text[0] == "0" and len(new_text) > 1:
                    new_text = new_text[1:]

                if 0 <= int(new_text) <= 255:
                    self.text = new_text

            if event.key == pygame.K_RETURN:
                self.active = False
                if self.text == "":
                    self.text = "0"

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (100, 100, 100), (self.rect.x+2, self.rect.y+2, self.rect.width-2, self.rect.height-2))  # Highlight border if active
        # Draw rectangle
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2)
        # Render text
        txt_surface = self.font.render(self.text, True, (255, 255, 255))
        # Centra il testo
        text_rect = txt_surface.get_rect(center=self.rect.center)
        screen.blit(txt_surface, text_rect)
