import pygame
import random
import math
from settings import *

# --- PARTICLE SYSTEM ---
class Particle:
    def __init__(self, x, y, color, particle_type="default"):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -2)
        self.color = color
        self.life = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME
        self.size = random.randint(3, 8)
        self.rotation = random.uniform(0, 360)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        self.vx *= 0.98 # Air resistance
        
    def draw(self, surface):
        if self.life > 0 and self.size > 0:
            alpha = int(255 * (self.life / self.max_life))
            s = pygame.Surface((int(self.size*4), int(self.size*4)), pygame.SRCALPHA)
            color_alpha = (*self.color, alpha)
            pygame.draw.circle(s, color_alpha, (int(self.size*2), int(self.size*2)), int(self.size))
            surface.blit(s, (int(self.x - self.size*2), int(self.y - self.size*2)))

class ConfettiParticle(Particle):
    def __init__(self, x, y):
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, CYAN, PINK]
        super().__init__(x, y, random.choice(colors), "confetti")
        self.width = random.randint(8, 15)
        self.height = random.randint(3, 6)
        
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.rect(s, color_with_alpha, (0, 0, self.width, self.height))
            rotated = pygame.transform.rotate(s, self.rotation)
            surface.blit(rotated, (self.x, self.y))
            self.rotation += 5

class InputBox:
    def __init__(self, x, y, width, height, placeholder="Ketik..."):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = INPUT_BOX_COLOR
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.shake = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = INPUT_ACTIVE_COLOR if self.active else INPUT_BOX_COLOR
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return "SUBMIT"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 20:
                char = event.unicode.upper()
                if char.isalnum() or char.isspace():
                    self.text += char
        return None
    
    def trigger_shake(self):
        self.shake = SHAKE_INTENSITY

    def draw(self, surface):
        shake_x = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        draw_rect = self.rect.move(shake_x, 0)
        
        # Shadow & Box
        shadow = draw_rect.move(3, 3)
        pygame.draw.rect(surface, (200, 200, 200), shadow, border_radius=10)
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=10)
        pygame.draw.rect(surface, BLUE if self.active else (180,180,180), draw_rect, 3, border_radius=10)
        
        # Text
        display = self.text if self.text else self.placeholder
        col = BLACK if self.text else (150, 150, 150)
        surf = FONT_MEDIUM.render(display, True, col)
        surface.blit(surf, (draw_rect.x + 15, draw_rect.y + 12))
        
        if self.shake > 0: self.shake -= 1
    
    def clear(self): self.text = ""

class Button:
    def __init__(self, x, y, w, h, text, color, hover_col, icon=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_col
        self.curr_color = color
        self.icon = icon
        self.scale = 1.0
        
    def handle_event(self, event):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEMOTION:
            self.curr_color = self.hover_color if hover else self.color
            self.scale = 1.05 if hover else 1.0
        if event.type == pygame.MOUSEBUTTONDOWN and hover:
            return True
        return False
        
    def draw(self, surface):
        w = int(self.rect.width * self.scale)
        h = int(self.rect.height * self.scale)
        r = pygame.Rect(0, 0, w, h)
        r.center = self.rect.center
        
        # Shadow
        s_rect = r.move(0, 5)
        pygame.draw.rect(surface, (0,0,0,50), s_rect, border_radius=15)
        
        pygame.draw.rect(surface, self.curr_color, r, border_radius=15)
        pygame.draw.rect(surface, BLACK, r, 3, border_radius=15)
        
        text_surf = FONT_MEDIUM.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=r.center)
        
        if self.icon:
            icon_surf = FONT_LARGE.render(self.icon, True, WHITE)
            surface.blit(icon_surf, (r.x + 20, r.y + 15))
            text_rect.x += 15
            
        surface.blit(text_surf, text_rect)

class ProgressBar:
    def __init__(self, x, y, w, h, max_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.max_val = max_val
        self.val = max_val
    
    def set_value(self, v): self.val = v
    def update(self): pass 
    def draw(self, surface):
        pygame.draw.rect(surface, (200,200,200), self.rect, border_radius=10)
        width = int((self.val / self.max_val) * self.rect.width)
        if width > 0:
            fill = pygame.Rect(self.rect.x, self.rect.y, width, self.rect.height)
            col = GREEN if width > self.rect.width*0.5 else RED
            pygame.draw.rect(surface, col, fill, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)