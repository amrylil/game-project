import pygame
import random
from settings import *
from game_data import WORDS_DATA, FLAGS_DATA, MathProblem, ACHIEVEMENTS
from ui_elements import Button, InputBox, Particle, ConfettiParticle, ProgressBar
from game_objects import Letter, Slot, FallingNumber
from game_rendering import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "MENU"
        self.score = 0
        self.high_score_kata = 0
        self.high_score_flag = 0
        self.high_score_math = 0
        
        self.message = ""
        self.message_timer = 0
        
        self.bg_particles = []
        self.particles = []
        self.init_bg_particles()
        
        # Kata
        self.level_kata = 0
        self.time_kata = 0
        self.letters = []
        self.slots = []
        self.current_word = ""
        self.hint = ""
        self.time_progress = None
        
        # Flag
        self.flag_round = 0
        self.max_flag_round = 10
        self.current_flag = None
        self.flag_answered = False
        self.input_box = InputBox(WIDTH//2-200, 500, 400, 60)
        self.time_flag = 0
        self.flag_streak = 0
        
        # Math
        self.math_level = 1
        self.current_math = None
        self.falling_numbers = []
        self.spawn_timer = 0
        self.lives = 3
        self.math_solved = 0
        self.combo = 0
        
        # Achievements
        self.unlocked_achievements = set()
        self.ach_notify = None
        self.ach_timer = 0

    def init_bg_particles(self):
        for _ in range(30):
            self.bg_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'v': random.uniform(0.5, 2),
                's': random.randint(2, 5),
                'c': random.choice([WHITE, YELLOW, CYAN])
            })

    def draw_bg_particles(self):
        for p in self.bg_particles:
            s = pygame.Surface((p['s']*2, p['s']*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['c'], 50), (p['s'], p['s']), p['s'])
            self.screen.blit(s, (p['x'], int(p['y'])))
            p['y'] -= p['v']
            if p['y'] < 0:
                p['y'] = HEIGHT
                p['x'] = random.randint(0, WIDTH)

    def spawn_particles(self, x, y, col, count=20, type="default"):
        for _ in range(count):
            if type == "confetti": self.particles.append(ConfettiParticle(x, y))
            else: self.particles.append(Particle(x, y, col))

    def check_achievement(self, id):
        if id not in self.unlocked_achievements:
            self.unlocked_achievements.add(id)
            for a in ACHIEVEMENTS:
                if a['id'] == id:
                    self.ach_notify = a
                    self.ach_timer = 180
                    self.spawn_particles(WIDTH//2, 100, YELLOW, 50, "confetti")

    def draw_achievement(self):
        if self.ach_timer > 0:
            self.ach_timer -= 1
            y = 20 if self.ach_timer > 20 else 20 - (20-self.ach_timer)*5
            r = pygame.Rect(WIDTH//2-150, y, 300, 60)
            pygame.draw.rect(self.screen, BLACK, r, border_radius=10)
            pygame.draw.rect(self.screen, YELLOW, r, 2, border_radius=10)
            
            icon = FONT_LARGE.render(self.ach_notify['icon'], True, WHITE)
            name = FONT_SMALL.render(self.ach_notify['name'], True, WHITE)
            self.screen.blit(icon, (r.x+10, r.y+10))
            self.screen.blit(name, (r.x+60, r.y+20))

    def update(self):
        # Particles
        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)
            
        # Logic Timer
        if self.state == "PLAY_KATA":
            if self.time_kata > 0:
                self.time_kata -= 1/60
                if self.time_progress: self.time_progress.set_value(self.time_kata)
            else:
                self.state = "GAME_OVER_KATA"
                
        elif self.state == "PLAY_FLAG":
            if self.time_flag > 0 and not self.flag_answered:
                self.time_flag -= 1/60
                if self.time_flag <= 0:
                    self.flag_answered = True
                    self.message = f"Waktu Habis! {self.current_flag['name']}"
                    self.message_timer = 120
                    
        elif self.state == "PLAY_MATH":
            self.update_math_game()

        # --- LOGIC TRANSISI LEVEL (BUG FIX) ---
        if self.message_timer > 0:
            self.message_timer -= 1
            # Saat timer pesan habis, cek apakah harus pindah level
            if self.message_timer == 0:
                is_correct_msg = "✅" in self.message
                self.message = ""
                
                if self.state == "PLAY_FLAG":
                    # Selalu lanjut ronde (baik benar atau salah)
                    self.flag_round += 1
                    if self.flag_round < self.max_flag_round:
                        self.setup_flag_round()
                    else:
                        self.high_score_flag = max(self.high_score_flag, self.score)
                        self.state = "COMPLETE_FLAG"
                        
                elif self.state == "PLAY_KATA" and is_correct_msg:
                    # Hanya lanjut jika benar
                    if self.level_kata < len(WORDS_DATA) - 1:
                        self.setup_kata_level(self.level_kata + 1)
                    else:
                        self.high_score_kata = max(self.high_score_kata, self.score)
                        self.state = "COMPLETE_KATA"

    def draw(self):
        btns = []
        if self.state == "MENU": btns = draw_menu(self.screen, self)
        elif self.state == "PLAY_KATA": btns = self.draw_game_kata()
        elif self.state == "PLAY_FLAG": btns = self.draw_game_flag()
        elif self.state == "PLAY_MATH": btns = self.draw_game_math()
        else: btns = self.draw_game_over()
        
        for p in self.particles: p.draw(self.screen)
        self.draw_achievement()
        
        return btns

    # --- KATA ---
    def setup_kata_level(self, level):
        self.level_kata = level
        d = WORDS_DATA[level]
        self.current_word = d["word"]
        self.hint = d["hint"]
        self.time_kata = 60
        self.letters = []
        self.slots = []
        self.time_progress = ProgressBar(50, 700, WIDTH-100, 20, 60)
        
        chars = list(self.current_word)
        random.shuffle(chars)
        
        sx = (WIDTH - len(chars)*80)//2
        for i, c in enumerate(chars): self.letters.append(Letter(c, sx + i*80, 250))
        
        slx = (WIDTH - len(self.current_word)*85)//2
        for i in range(len(self.current_word)): self.slots.append(Slot(slx + i*85, 500, i))

    def check_word(self):
        f = "".join([s.letter.char for s in self.slots if s.letter])
        if len(f) != len(self.current_word):
            self.message = "❌ Lengkapi Huruf!"
            self.message_timer = 60
            return
        
        if f == self.current_word:
            self.score += 100 + int(self.time_kata)
            self.message = "✅ BENAR!"
            self.message_timer = 90
            self.spawn_particles(WIDTH//2, 400, GREEN, 50, "confetti")
            if self.level_kata == 0: self.check_achievement("first_word")
        else:
            self.message = "❌ SALAH!"
            self.message_timer = 60
            self.spawn_particles(WIDTH//2, 400, RED, 30)
            for l in self.letters:
                l.in_slot = False
                l.x, l.y = l.original_x, l.original_y
            for s in self.slots: s.letter = None

    def draw_game_kata(self):
        draw_gradient_background(self.screen, BG_COLOR, WHITE)
        draw_animated_header(self.screen, f"Level {self.level_kata+1} - {WORDS_DATA[self.level_kata]['category']}", GREEN, pygame.time.get_ticks())
        draw_stats_bar(self.screen, self.score, int(self.time_kata))
        
        h_surf = FONT_SMALL.render(f"💡 {self.hint}", True, BLACK)
        self.screen.blit(h_surf, h_surf.get_rect(center=(WIDTH//2, 180)))
        
        for s in self.slots: s.draw(self.screen)
        for l in self.letters: l.draw(self.screen)
        if self.time_progress: self.time_progress.draw(self.screen)
        draw_message_box(self.screen, self.message)
        
        c = Button(WIDTH//2-220, 730, 200, 60, "CEK", GREEN, GREEN_DARK)
        m = Button(WIDTH//2+20, 730, 200, 60, "MENU", RED, RED_DARK)
        c.draw(self.screen)
        m.draw(self.screen)
        return [c, m]

    # --- FLAG ---
    def setup_flag_round(self):
        self.current_flag = random.choice(FLAGS_DATA)
        self.flag_answered = False
        self.time_flag = 30
        self.input_box.text = ""
        self.message = ""

    def check_flag_answer(self, txt):
        if self.flag_answered: return
        
        if txt.upper() == self.current_flag["name"]:
            self.score += 150 + int(self.time_flag)
            self.message = "✅ BENAR!"
            self.flag_streak += 1
            self.spawn_particles(WIDTH//2, 400, GREEN, 50, "confetti")
            if self.flag_streak >= 5: self.check_achievement("flag_master")
        else:
            self.message = f"❌ Salah! {self.current_flag['name']}"
            self.flag_streak = 0
            self.spawn_particles(WIDTH//2, 400, RED, 30)
            
        self.flag_answered = True
        self.message_timer = 120

    def draw_flag_shape(self, x, y, w, h, data):
        pygame.draw.rect(self.screen, BLACK, (x-3, y-3, w+6, h+6), 3)
        c = data["colors"]
        t = data["type"]
        if t == "h2":
            pygame.draw.rect(self.screen, c[0], (x,y,w,h//2))
            pygame.draw.rect(self.screen, c[1], (x,y+h//2,w,h//2))
        elif t == "v3":
            pygame.draw.rect(self.screen, c[0], (x,y,w//3,h))
            pygame.draw.rect(self.screen, c[1], (x+w//3,y,w//3,h))
            pygame.draw.rect(self.screen, c[2], (x+2*w//3,y,w//3,h))
        elif t == "circle":
            pygame.draw.rect(self.screen, c[0], (x,y,w,h))
            pygame.draw.circle(self.screen, c[1], (x+w//2, y+h//2), h//3)
        else:
            pygame.draw.rect(self.screen, c[0], (x,y,w,h))
            if len(c) > 1:
                pygame.draw.rect(self.screen, c[1], (x+w//2-15, y, 30, h))
                pygame.draw.rect(self.screen, c[1], (x, y+h//2-15, w, 30))

    def draw_game_flag(self):
        draw_gradient_background(self.screen, (255,248,225), (255,236,179))
        draw_animated_header(self.screen, f"Ronde {self.flag_round+1}/10", ORANGE, pygame.time.get_ticks())
        draw_stats_bar(self.screen, self.score, int(self.time_flag), extra=f"Streak: {self.flag_streak}")
        
        q = FONT_LARGE.render("Negara apa ini?", True, BLACK)
        self.screen.blit(q, q.get_rect(center=(WIDTH//2, 200)))
        
        self.draw_flag_shape(WIDTH//2-150, 240, 300, 200, self.current_flag)
        self.input_box.draw(self.screen)
        draw_message_box(self.screen, self.message)
        
        k = Button(WIDTH//2-100, 580, 200, 60, "KIRIM", BLUE, BLUE_DARK)
        m = Button(50, 700, 150, 60, "MENU", RED, RED_DARK)
        k.draw(self.screen)
        m.draw(self.screen)
        return [k, m]

    # --- MATH ---
    def setup_math_game(self):
        self.score = 0
        self.lives = 3
        self.math_level = 1
        self.math_solved = 0
        self.generate_math_problem()
        
    def generate_math_problem(self):
        self.current_math = MathProblem.generate(self.math_level)
        self.falling_numbers = []
        
    def update_math_game(self):
        self.spawn_timer += 1
        if self.spawn_timer > 90:
            self.spawn_timer = 0
            self.falling_numbers.append(FallingNumber(self.current_math["answer"], random.randint(50, WIDTH-50), -50, True))
            w = self.current_math["answer"] + random.choice([-1, 1, -2, 2, 10])
            self.falling_numbers.append(FallingNumber(w, random.randint(50, WIDTH-50), -50, False))
            
        for n in self.falling_numbers[:]:
            n.update()
            if n.y > HEIGHT:
                self.falling_numbers.remove(n)
                if n.is_correct and not n.clicked:
                    self.lives -= 1
                    self.spawn_particles(WIDTH//2, HEIGHT-50, RED, 20)
                    if self.lives <= 0: self.state = "GAME_OVER_MATH"

    def draw_game_math(self):
        draw_gradient_background(self.screen, (240,230,250), WHITE)
        draw_animated_header(self.screen, f"Level {self.math_level}", PURPLE, pygame.time.get_ticks())
        draw_stats_bar(self.screen, self.score, lives=self.lives)
        
        qb = pygame.Rect(WIDTH//2-200, 200, 400, 100)
        pygame.draw.rect(self.screen, WHITE, qb, border_radius=20)
        pygame.draw.rect(self.screen, PURPLE, qb, 5, border_radius=20)
        qs = FONT_TITLE.render(self.current_math["question"], True, BLACK)
        self.screen.blit(qs, qs.get_rect(center=qb.center))
        
        for n in self.falling_numbers: n.draw(self.screen)
        
        m = Button(50, 700, 150, 60, "MENU", RED, RED_DARK)
        m.draw(self.screen)
        return [m]

    def draw_game_over(self):
        draw_gradient_background(self.screen, BLACK, (50,0,0))
        t = FONT_TITLE.render("GAME OVER", True, WHITE)
        s = FONT_LARGE.render(f"Final Score: {self.score}", True, YELLOW)
        self.screen.blit(t, t.get_rect(center=(WIDTH//2, 300)))
        self.screen.blit(s, s.get_rect(center=(WIDTH//2, 400)))
        
        m = Button(WIDTH//2-100, 550, 200, 80, "MENU UTAMA", BLUE, BLUE_DARK)
        m.draw(self.screen)
        return [m]