import pygame
import random
import math
from settings import *

class Letter:
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self.width = 65
        self.height = 75
        self.original_x = x
        self.original_y = y
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.in_slot = False
        self.slot_index = -1
        self.shake = 0
        self.scale = 1.0
        self.target_scale = 1.0
        self.glow = 0
        
    def update(self):
        self.scale += (self.target_scale - self.scale) * 0.2
        self.glow = max(0, self.glow - 2)
        if self.shake > 0: self.shake -= 1
        
    def draw(self, surface):
        self.update()
        shake_x = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        
        draw_x = self.x + shake_x
        draw_y = self.y
        
        rect = pygame.Rect(draw_x, draw_y, self.width, self.height)
        
        if self.in_slot:
            color = GREEN
        elif self.dragging:
            color = CYAN
        else:
            color = YELLOW
            
        # Shadow
        s_rect = rect.move(4, 4)
        pygame.draw.rect(surface, (0,0,0,50), s_rect, border_radius=12)
        
        # Base
        pygame.draw.rect(surface, color, rect, border_radius=12)
        
        # Gradient (FIXED ERROR VALUE COLOR)
        for i in range(self.height):
            ratio = i / self.height
            # Pastikan nilai RGB tidak melebihi 255
            r = min(255, int(color[0] * (1 - ratio * 0.2)))
            g = min(255, int(color[1] * (1 - ratio * 0.2)))
            b = min(255, int(color[2] * (1 - ratio * 0.2)))
            pygame.draw.line(surface, (r,g,b), (rect.left, rect.top + i), (rect.right, rect.top + i))
            
        # Border
        pygame.draw.rect(surface, BLACK, rect, 2, border_radius=12)
        
        # Text
        txt = FONT_LARGE.render(self.char, True, BLACK)
        txt_r = txt.get_rect(center=rect.center)
        surface.blit(txt, txt_r)
        
        # Glow
        if self.glow > 0:
            s = pygame.Surface((rect.width+20, rect.height+20), pygame.SRCALPHA)
            alpha = min(255, self.glow)
            pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=15)
            surface.blit(s, (rect.x-10, rect.y-10))

class Slot:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 85
        self.index = index
        self.letter = None
        self.pulse = 0
        
    def draw(self, surface):
        self.pulse += 0.1
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Glow animation for empty slots
        if not self.letter:
            glow = int(abs(math.sin(self.pulse)) * 50)
            s = pygame.Surface((self.width+10, self.height+10), pygame.SRCALPHA)
            pygame.draw.rect(s, (*BLUE, glow), s.get_rect(), border_radius=15)
            surface.blit(s, (self.x-5, self.y-5))
            
        pygame.draw.rect(surface, WHITE, rect, border_radius=12)
        col = GREEN if self.letter else BLUE
        pygame.draw.rect(surface, col, rect, 3, border_radius=12)
        
    def check_collision(self, letter_rect):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(letter_rect)

class FallingNumber:
    def __init__(self, num, x, y, correct):
        self.number = num
        self.x = x
        self.y = y
        self.speed = random.uniform(2, 4)
        self.is_correct = correct
        self.clicked = False
        self.size = 50
        
    def update(self):
        self.y += self.speed
        
    def draw(self, surface):
        if not self.clicked:
            col = GREEN if self.is_correct else RED
            pygame.draw.circle(surface, col, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.size, 3)
            
            txt = FONT_LARGE.render(str(self.number), True, WHITE)
            tr = txt.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(txt, tr)
            
    def check_click(self, pos):
        return math.hypot(pos[0]-self.x, pos[1]-self.y) < self.size