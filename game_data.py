import random
from settings import *

# --- DATA SUSUN KATA ---
WORDS_DATA = [
    {"word": "BUKU", "hint": "Tempat membaca cerita", "category": "Pendidikan"},
    {"word": "SEKOLAH", "hint": "Tempat belajar siswa", "category": "Pendidikan"},
    {"word": "GURU", "hint": "Pengajar di kelas", "category": "Pendidikan"},
    {"word": "KOMPUTER", "hint": "Alat elektronik bekerja", "category": "Teknologi"},
    {"word": "INTERNET", "hint": "Jaringan dunia maya", "category": "Teknologi"},
    {"word": "PANCASILA", "hint": "Dasar negara Indonesia", "category": "Nasional"},
    {"word": "MERDEKA", "hint": "Bebas dari penjajah", "category": "Nasional"},
    {"word": "MATAHARI", "hint": "Pusat tata surya", "category": "Sains"},
    {"word": "GRAVITASI", "hint": "Gaya tarik bumi", "category": "Sains"},
    {"word": "JUJUR", "hint": "Tidak berbohong", "category": "Sosial"},
]

# --- DATA BENDERA ---
FLAGS_DATA = [
    {"name": "INDONESIA", "type": "h2", "colors": [FLAG_RED, FLAG_WHITE], "hint": "Merah Putih", "region": "Asia"},
    {"name": "POLANDIA", "type": "h2", "colors": [FLAG_WHITE, FLAG_RED], "hint": "Putih Merah", "region": "Eropa"},
    {"name": "UKRAINA", "type": "h2", "colors": [FLAG_BLUE, FLAG_YELLOW], "hint": "Biru Kuning", "region": "Eropa"},
    {"name": "MONAKO", "type": "h2", "colors": [FLAG_RED, FLAG_WHITE], "hint": "Mirip Indonesia", "region": "Eropa"},
    {"name": "JERMAN", "type": "h3", "colors": [FLAG_BLACK, FLAG_RED, FLAG_YELLOW], "hint": "Hitam Merah Kuning", "region": "Eropa"},
    {"name": "BELANDA", "type": "h3", "colors": [FLAG_RED, FLAG_WHITE, FLAG_BLUE], "hint": "Merah Putih Biru", "region": "Eropa"},
    {"name": "RUSIA", "type": "h3", "colors": [FLAG_WHITE, FLAG_BLUE, FLAG_RED], "hint": "Putih Biru Merah", "region": "Eropa"},
    {"name": "AUSTRIA", "type": "h3", "colors": [FLAG_RED, FLAG_WHITE, FLAG_RED], "hint": "Merah Putih Merah", "region": "Eropa"},
    {"name": "BELGIA", "type": "v3", "colors": [FLAG_BLACK, FLAG_YELLOW, FLAG_RED], "hint": "Vertikal hitam kuning merah", "region": "Eropa"},
    {"name": "ITALIA", "type": "v3", "colors": [FLAG_GREEN, FLAG_WHITE, FLAG_RED], "hint": "Hijau Putih Merah", "region": "Eropa"},
    {"name": "PRANCIS", "type": "v3", "colors": [FLAG_BLUE, FLAG_WHITE, FLAG_RED], "hint": "Biru Putih Merah", "region": "Eropa"},
    {"name": "JEPANG", "type": "circle", "colors": [FLAG_WHITE, FLAG_RED], "hint": "Lingkaran merah", "region": "Asia"},
    {"name": "BANGLADESH", "type": "circle", "colors": [FLAG_GREEN, FLAG_RED], "hint": "Lingkaran merah di hijau", "region": "Asia"},
    {"name": "SWISS", "type": "cross", "colors": [FLAG_RED, FLAG_WHITE], "hint": "Salib putih", "region": "Eropa"},
]

# --- ACHIEVEMENTS ---
ACHIEVEMENTS = [
    {"id": "first_word", "name": "Kata Pertama", "desc": "Selesaikan kata pertama", "icon": "🏆"},
    {"id": "speed_demon", "name": "Kilat", "desc": "Selesaikan kata dalam 60 detik", "icon": "⚡"},
    {"id": "flag_master", "name": "Master Bendera", "desc": "Jawab 5 bendera berturut-turut", "icon": "🚩"},
    {"id": "math_genius", "name": "Genius Matematika", "desc": "Jawab 20 soal matematika", "icon": "🧮"},
    {"id": "perfect_score", "name": "Sempurna", "desc": "Dapatkan skor 1000+", "icon": "💯"},
]

# --- MATEMATIKA ---
class MathProblem:
    @staticmethod
    def generate(level):
        if level <= 3:
            a = random.randint(1, 20 + level * 5)
            b = random.randint(1, 20 + level * 5)
            return {"question": f"{a} + {b}", "answer": a + b, "type": "Penjumlahan"}
        elif level <= 6:
            a = random.randint(10 + level * 5, 50 + level * 10)
            b = random.randint(1, a)
            return {"question": f"{a} - {b}", "answer": a - b, "type": "Pengurangan"}
        elif level <= 9:
            a = random.randint(2, min(12, 5 + level))
            b = random.randint(2, min(12, 5 + level))
            return {"question": f"{a} × {b}", "answer": a * b, "type": "Perkalian"}
        else:
            b = random.randint(2, 12)
            answer = random.randint(2, 15 + level)
            a = b * answer
            return {"question": f"{a} ÷ {b}", "answer": answer, "type": "Pembagian"}