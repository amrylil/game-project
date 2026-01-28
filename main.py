import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, GREEN, RED
from game_engine import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎮 Game Edukasi Premium V2 (Fixed)")
    clock = pygame.time.Clock()
    
    game = Game(screen)
    
    while True:
        clock.tick(FPS)
        
        # Draw & Update
        current_buttons = game.draw()
        game.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Input Box (Flag Game)
            if game.state == "PLAY_FLAG":
                if game.input_box.handle_event(event) == "SUBMIT":
                    game.check_flag_answer(game.input_box.text)
            
            # Button Clicks
            for i, btn in enumerate(current_buttons):
                if btn.handle_event(event):
                    if game.state == "MENU":
                        if i == 0: game.setup_kata_level(0); game.state = "PLAY_KATA"; game.score=0
                        elif i == 1: game.setup_flag_round(); game.state = "PLAY_FLAG"; game.score=0
                        elif i == 2: game.setup_math_game(); game.state = "PLAY_MATH"; game.score=0
                        elif i == 3: pygame.quit(); sys.exit()
                    
                    elif game.state == "PLAY_KATA":
                        if i == 0: game.check_word()
                        elif i == 1: game.state = "MENU"
                        
                    elif game.state == "PLAY_FLAG":
                        if i == 0: game.check_flag_answer(game.input_box.text)
                        elif i == 1: game.state = "MENU"
                        
                    elif game.state == "PLAY_MATH":
                        if i == 0: game.state = "MENU"
                        
                    elif "GAME_OVER" in game.state or "COMPLETE" in game.state:
                        if i == 0: game.state = "MENU"
            
            # Drag Drop Kata
            if game.state == "PLAY_KATA":
                for l in game.letters:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.Rect(l.x, l.y, l.width, l.height).collidepoint(event.pos):
                            l.dragging = True; l.offset_x = l.x - event.pos[0]; l.offset_y = l.y - event.pos[1]; l.target_scale = 1.1
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if l.dragging:
                            l.dragging = False; l.target_scale = 1.0; placed = False
                            for s in game.slots:
                                if s.check_collision(pygame.Rect(l.x, l.y, l.width, l.height)) and (not s.letter or s.letter == l):
                                    l.x = s.x+5; l.y = s.y+5; l.in_slot = True; l.slot_index = s.index; s.letter = l; placed = True; break
                            if not placed:
                                if l.in_slot:
                                    for s in game.slots:
                                        if s.letter == l: s.letter = None
                                l.x = l.original_x; l.y = l.original_y; l.in_slot = False
                    elif event.type == pygame.MOUSEMOTION and l.dragging:
                        l.x = event.pos[0] + l.offset_x; l.y = event.pos[1] + l.offset_y

            # Math Game Clicks
            if game.state == "PLAY_MATH" and event.type == pygame.MOUSEBUTTONDOWN:
                for n in game.falling_numbers[:]:
                    if n.check_click(event.pos):
                        n.clicked = True
                        game.falling_numbers.remove(n)
                        if n.is_correct:
                            game.score += 50; game.math_solved += 1; game.spawn_particles(n.x, n.y, GREEN, 30)
                            if game.math_solved % 5 == 0: game.math_level = min(12, game.math_level + 1)
                            game.generate_math_problem(); game.spawn_timer = 0
                        else:
                            game.lives -= 1; game.spawn_particles(n.x, n.y, RED, 30)
                            if game.lives <= 0: game.state = "GAME_OVER_MATH"

        pygame.display.flip()

if __name__ == "__main__":
    main()