import pygame
import math
from settings import *
from ui_elements import Button

def draw_gradient_background(surface, c1, c2):
    for y in range(0, HEIGHT, 2):
        r = y / HEIGHT
        col = (
            int(c1[0]*(1-r) + c2[0]*r),
            int(c1[1]*(1-r) + c2[1]*r),
            int(c1[2]*(1-r) + c2[2]*r)
        )
        pygame.draw.line(surface, col, (0,y), (WIDTH,y), 2)

def draw_animated_header(surface, text, color, ticks):
    pygame.draw.rect(surface, color, (0,0,WIDTH,120))
    # Wave
    for x in range(0, WIDTH, 10):
        y = 120 + math.sin((x+ticks)*0.02)*5
        pygame.draw.line(surface, (255,255,255), (x,120), (x,y), 2)
    
    txt = FONT_LARGE.render(text, True, WHITE)
    shad = FONT_LARGE.render(text, True, (0,0,0,50))
    pos = txt.get_rect(center=(WIDTH//2, 60))
    surface.blit(shad, (pos.x+3, pos.y+3))
    surface.blit(txt, pos)

def draw_stats_bar(surface, score, time=None, lives=None, extra=""):
    y = 140
    sc = FONT_MEDIUM.render(f"Skor: {score}", True, BLACK)
    surface.blit(sc, (30, y))
    
    if extra:
        ex = FONT_MEDIUM.render(extra, True, PURPLE)
        surface.blit(ex, (WIDTH//2 - ex.get_width()//2, y))
        
    if time is not None:
        col = RED if time < 10 else BLACK
        tm = FONT_MEDIUM.render(f"⏱️ {int(time)}s", True, col)
        surface.blit(tm, (WIDTH-150, y))
    elif lives is not None:
        lv = FONT_MEDIUM.render(f"❤️ {lives}", True, RED)
        surface.blit(lv, (WIDTH-150, y))

def draw_message_box(surface, msg):
    if not msg: return
    col = GREEN if "✅" in msg else RED
    surf = FONT_LARGE.render(msg, True, col)
    bg = pygame.Rect(WIDTH//2 - surf.get_width()//2 - 20, 620, surf.get_width()+40, 70)
    pygame.draw.rect(surface, WHITE, bg, border_radius=15)
    pygame.draw.rect(surface, col, bg, 4, border_radius=15)
    surface.blit(surf, (bg.x+20, bg.y+20))

def draw_menu(surface, game):
    draw_gradient_background(surface, BG_GRADIENT_START, BG_GRADIENT_END)
    game.draw_bg_particles()
    
    tit = FONT_TITLE.render("🎮 GAME EDUKASI", True, WHITE)
    y = 100 + math.sin(pygame.time.get_ticks()/500)*10
    surface.blit(tit, tit.get_rect(center=(WIDTH//2, y)))
    
    sub = FONT_SMALL.render("Python Pygame Project", True, BLACK)
    surface.blit(sub, sub.get_rect(center=(WIDTH//2, 180)))
    
    btns = [
        Button(WIDTH//2-250, 250, 500, 90, "Susun Kata", GREEN, GREEN_DARK, "📝"),
        Button(WIDTH//2-250, 360, 500, 90, "Tebak Bendera", ORANGE, ORANGE_DARK, "🚩"),
        Button(WIDTH//2-250, 470, 500, 90, "Matematika", PURPLE, PURPLE_DARK, "🔢"),
        Button(WIDTH//2-250, 600, 500, 70, "Keluar", RED, RED_DARK, "❌")
    ]
    for b in btns: b.draw(surface)
    
    # High Score
    info = FONT_TINY.render(f"High Scores: Kata={game.high_score_kata} | Bendera={game.high_score_flag} | Math={game.high_score_math}", True, YELLOW)
    surface.blit(info, info.get_rect(center=(WIDTH//2, 750)))
    
    return btns