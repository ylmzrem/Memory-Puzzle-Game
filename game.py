import pygame
import sys
import os
import random
import time
import sqlite3  # SQLite kütüphanesi

# Pygame'i başlat
pygame.init()
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font("fonts/OkayJelly.otf", 30)


# Ekran boyutu
WIDTH, HEIGHT = 950, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")

# Renk tanımlamaları
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Tema Renkleri
current_theme = "default"
theme_colors = {
    "default": {
        "BACKGROUND": (173, 216, 230), # Açık mavi
        "BUTTON": (255, 165, 0),       # Canlı turuncu
        "TEXT": WHITE,
        "CARD_BACK": (135, 206, 235),  # Orta mavi
        "CARD_FRONT": WHITE,
        "MATCHED": (0, 128, 0)
    },
    "pink": {
        "BACKGROUND": (255, 182, 193),
        "BUTTON": (155, 89, 182),
        "TEXT": WHITE,
        "CARD_BACK": (255, 153, 255),
        "CARD_FRONT": WHITE,
        "MATCHED": (0, 204, 0)
    },
    "blue": {
        "BACKGROUND": (173, 216, 230),
        "BUTTON": (65, 105, 225),
        "TEXT": WHITE,
        "CARD_BACK": (135, 206, 235),
        "CARD_FRONT": WHITE,
        "MATCHED": (0, 128, 0),
    },
    "nature": {
        "BACKGROUND": (204, 255, 204), # Açık yeşil
        "BUTTON": (60, 179, 113),    # Orta yeşil
        "TEXT": WHITE,
        "CARD_BACK": (144, 238, 144), # Açık lime yeşili
        "CARD_FRONT": (255, 255, 240), # Fildişi
        "MATCHED": (0, 128, 0)       # Koyu yeşil
    },
    "night": {
        "BACKGROUND": (30, 30, 50),   # Koyu lacivert
        "BUTTON": (70, 70, 120),      # Orta lacivert
        "TEXT": (220, 220, 220),      # Açık gri metin
        "CARD_BACK": (50, 50, 80),    # Daha koyu lacivert
        "CARD_FRONT": (240, 248, 255), # Alice mavisi
        "MATCHED": (0, 191, 255)      # Açık mavi (aqua)
    },
    "retro": {
        "BACKGROUND": (240, 220, 190), # Açık bej
        "BUTTON": (205, 92, 92),     # Hint kırmızısı
        "TEXT": (50, 50, 50),        # Koyu gri metin
        "CARD_BACK": (255, 160, 122), # Açık mercan
        "CARD_FRONT": WHITE,
        "MATCHED": (255, 215, 0)      # Altın rengi
    }
}

# Font ve ikonlar
font_path = os.path.join("fonts", "OkayJelly.otf")
title_font = pygame.font.Font(font_path, 64)
button_font = pygame.font.Font(font_path, 32)
instruction_font = pygame.font.Font(font_path, 24)

# Müzik
pygame.mixer.music.load(os.path.join("assets", "Cold Sober.mp3"))
pygame.mixer.music.play(-1)
volume = 0.5
pygame.mixer.music.set_volume(volume)

sound_flip = pygame.mixer.Sound(os.path.join("assets", "flipcard.mp3"))
sound_correct = pygame.mixer.Sound(os.path.join("assets", "correct.mp3"))
sound_incorrect = pygame.mixer.Sound(os.path.join("assets", "incorrect.mp3"))
sound_congrats = pygame.mixer.Sound(os.path.join("assets", "congrats.mp3"))
sound_gameover = pygame.mixer.Sound(os.path.join("assets", "gameover.mp3"))
sound_flip.set_volume(0.5)
sound_correct.set_volume(0.5)
sound_incorrect.set_volume(0.5)
sound_congrats.set_volume(0.7)
sound_gameover.set_volume(0.7)

# Ayarlar ve ses ikonları
settings_icon = pygame.image.load(os.path.join("assets", "settings.png"))
settings_icon = pygame.transform.scale(settings_icon, (40, 40))
theme_icon = pygame.image.load(os.path.join("assets", "themes.png"))
theme_icon = pygame.transform.scale(theme_icon, (50, 50))
volume_icon_large = pygame.image.load(os.path.join("assets", "volume.png"))
volume_icon_large = pygame.transform.scale(volume_icon_large, (50, 50))
volume_icon_small = pygame.image.load(os.path.join("assets", "mute.png"))
volume_icon_small = pygame.transform.scale(volume_icon_small, (50, 50))
pause_icon = pygame.image.load(os.path.join("assets", "pause.png"))
pause_icon = pygame.transform.scale(pause_icon, (50, 50))
scores_icon = pygame.image.load(os.path.join("assets", "scores.png"))
scores_icon = pygame.transform.scale(scores_icon, (50, 50))
back_btn = pygame.Rect(400, 650, 150, 50)

sound_on = True  # Başlangıçta ses açık
volume_icon_rect = volume_icon_large.get_rect(topleft=(780, 20))  # Ses ikonu konumu

# Global durumlar
score = 0
start_time = None
current_screen = "main_menu"
selected_theme = None
is_mini_game = False
difficulty = None
elapsed_before_pause = 0
pause_start_time = 0
is_paused = False  # Global olarak tanımla
moves = 0
cards = []  # Oyun kartlarını tutan global liste
grid_size = 0  # Oyun grid boyutunu tutan global değişken
flipped = []  # Açılan kartları tutan global liste
wait_time = 0  # Kart çevirme bekleme süresini tutan global değişken
clock = pygame.time.Clock()  # Oyunun saatini kontrol eden global nesne
pause_button_rect = None  # Pause butonunun dikdörtgenini tutan global değişken
username = ""
user_text = ""
input_active = False
error_message = ""  # kullanıcı ismi boşsa hata mesajı göster
selected_game_mode = None  # "normal" ya da "penalty"
current_difficulty_filter = None
difficulty = None



stars = []
for _ in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(-HEIGHT, 0)
    speed = random.uniform(1, 3)
    stars.append([x, y, speed])


# Kart sınıfı
class Card:
    def __init__(self, x, y, icon, icon_name):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.icon = pygame.transform.smoothscale(icon, (80, 80))
        self.icon_name = icon_name
        self.flipped = False
        self.matched = False

    def draw(self, surface):
        if self.flipped or self.matched:
            pygame.draw.rect(surface, theme_colors[current_theme]["MATCHED"] if self.matched else theme_colors[current_theme]["CARD_FRONT"], self.rect, border_radius=8)
            surface.blit(self.icon, (self.rect.centerx - 40, self.rect.centery - 40))
        else:
            pygame.draw.rect(surface, theme_colors[current_theme]["CARD_BACK"], self.rect, border_radius=8)


# Yardımcı fonksiyonlar
def get_theme_icons(theme, pair_count):
    path = os.path.join("assets", theme)
    files = sorted(os.listdir(path))
    icons = [(pygame.image.load(os.path.join(path, f)).convert_alpha(), f.split('.')[0]) for f in files if
             f.endswith(".png")]
    icon_pairs = {}
    for icon, name in icons:
        pair_id = name.split('-')[0]
        icon_pairs.setdefault(pair_id, []).append((icon, name))
    selected = list(icon_pairs.items())[:pair_count]
    flat = [item for pair in selected for item in pair[1]]
    return flat


# Skor ve süreyi ekranda gösterme
def draw_score_and_time():
    global start_time, pause_button_rect
    elapsed_time = 0
    if start_time and not is_paused:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Saniye cinsinden süre
    elif start_time and is_paused and pause_start_time > 0:
        elapsed_time = (pause_start_time - start_time) // 1000

    score_text = button_font.render(f"Score: {score}", True, theme_colors[current_theme]["TEXT"])
    time_text = button_font.render(f"Time: {elapsed_time}s", True, theme_colors[current_theme]["TEXT"])
    moves_text = button_font.render(f"Moves: {moves}", True, theme_colors[current_theme]["TEXT"])

    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (420, 20))
    screen.blit(moves_text, (20, 60))

    # Ses ikonunu çiz
    if sound_on:
        screen.blit(volume_icon_large, volume_icon_rect)
    else:
        screen.blit(volume_icon_small, volume_icon_rect)

    pause_rect = pause_icon.get_rect(topleft=(850, 20))
    screen.blit(pause_icon, pause_rect.topleft)
    pause_button_rect = pause_rect  # Global değişkene atama

    return pause_rect


def draw_pause_screen():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])  # Arkaplanı temadan al

    pause_text = title_font.render("Game Paused", True, theme_colors[current_theme]["TEXT"])
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 100))

    # Slider özellikleri
    bar_x = WIDTH // 2 - 150
    bar_y = 250
    bar_width = 300
    bar_height = 20
    handle_x = int(bar_x + bar_width * volume)

    # Sliderı çiz
    volume_icons_rect = draw_slider(bar_x, bar_y, bar_width, bar_height, handle_x, volume, "Volume", volume_icon_small,volume_icon_large)
    slider_rect = (bar_x, bar_y, bar_width, bar_height)

    new_game_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 220, 50)
    draw_button("New Game", new_game_btn, theme_colors[current_theme]["BUTTON"])

    resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 220, 50)
    draw_button("Resume", resume_button, theme_colors[current_theme]["BUTTON"])

    exit_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 170, 220, 50)
    draw_button("Exit", exit_btn, theme_colors[current_theme]["BUTTON"])

    return bar_x, bar_y, bar_width, bar_height, new_game_btn, resume_button, exit_btn, slider_rect, volume_icons_rect


def create_game_board(pair_count=8, theme=None):
    icons = get_theme_icons(theme, pair_count)
    random.shuffle(icons)
    cards_local = []
    grid_size_local = int((pair_count * 2) ** 0.5)
    padding_x = (WIDTH - grid_size_local * 110) // 2
    padding_y = (HEIGHT - grid_size_local * 110) // 2
    for i in range(grid_size_local):
        for j in range(grid_size_local):
            if icons:
                icon, name = icons.pop()
                x = padding_x + j * 110
                y = padding_y + i * 110
                cards_local.append(Card(x, y, icon, name))
    return cards_local, grid_size_local


def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=12)
    label = button_font.render(text, True, theme_colors[current_theme]["TEXT"])
    screen.blit(label, label.get_rect(center=rect.center))


def draw_main_menu():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])

    # Metinleri tek tek render et ve alt alta yazdır
    title_text1 = title_font.render("<Memory", True, theme_colors[current_theme]["TEXT"])
    title_text2 = title_font.render("Puzzle", True, theme_colors[current_theme]["TEXT"])
    title_text3 = title_font.render("Game>", True, theme_colors[current_theme]["TEXT"])
    screen.blit(title_text1, (WIDTH // 2 - title_text1.get_width() // 2, HEIGHT // 3 - 100))
    screen.blit(title_text2, (WIDTH // 2 - title_text2.get_width() // 2, HEIGHT // 3 - 100 + title_text1.get_height()))
    screen.blit(title_text3, (
        WIDTH // 2 - title_text3.get_width() // 2, HEIGHT // 3 - 100 + title_text1.get_height() + title_text2.get_height()))

    start_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 60)
    draw_button("START", start_btn, theme_colors[current_theme]["BUTTON"])

    how_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 160, 300, 60)
    draw_button("HOW TO PLAY", how_btn, theme_colors[current_theme]["BUTTON"])

    settings_btn_radius = 30
    settings_btn_center = (WIDTH - 100, HEIGHT - 90)
    pygame.draw.circle(screen, theme_colors[current_theme]["BUTTON"], settings_btn_center, settings_btn_radius)
    icon_rect = settings_icon.get_rect(center=settings_btn_center)
    screen.blit(settings_icon, icon_rect)


    settings_btn_radius = 30
    settings_btn_center = (WIDTH - 100, HEIGHT - 90)
    pygame.draw.circle(screen, theme_colors[current_theme]["BUTTON"], settings_btn_center, settings_btn_radius)
    icon_rect = settings_icon.get_rect(center=settings_btn_center)
    screen.blit(settings_icon, icon_rect)
    settings_btn = pygame.Rect(settings_btn_center[0] - settings_btn_radius,
                               settings_btn_center[1] - settings_btn_radius,
                               settings_btn_radius * 2, settings_btn_radius * 2)

    scores_btn_radius = 35
    scores_btn_center = (850, 50)
    pygame.draw.circle(screen, theme_colors[current_theme]["BUTTON"], scores_btn_center, scores_btn_radius)
    icon_rect = scores_icon.get_rect(center=scores_btn_center)
    screen.blit(scores_icon, icon_rect)
    scores_btn = pygame.Rect(scores_btn_center[0] - scores_btn_radius,
                               scores_btn_center[1] - scores_btn_radius,
                               scores_btn_radius * 2, scores_btn_radius * 2)

    theme_btn_radius = 35
    theme_btn_center = (100, HEIGHT - 90)
    pygame.draw.circle(screen, theme_colors[current_theme]["BUTTON"], theme_btn_center, theme_btn_radius)
    theme_icon_rect = theme_icon.get_rect(center=theme_btn_center)
    screen.blit(theme_icon, theme_icon_rect)
    game_theme_btn = pygame.Rect(theme_btn_center[0] - theme_btn_radius,
                                 theme_btn_center[1] - theme_btn_radius,
                                 theme_btn_radius * 2, theme_btn_radius * 2)

    # Ses açma/kapama butonu
    sound_btn_radius = 35
    sound_btn_center = (100, 50)
    pygame.draw.circle(screen, theme_colors[current_theme]["BUTTON"], sound_btn_center, sound_btn_radius)
    sound_icon = volume_icon_large if sound_on else volume_icon_small
    icon_rect = sound_icon.get_rect(center=sound_btn_center)
    screen.blit(sound_icon, icon_rect)
    sound_button_rect = pygame.Rect(sound_btn_center[0] - sound_btn_radius,
                                    sound_btn_center[1] - sound_btn_radius,
                                    sound_btn_radius * 2, sound_btn_radius * 2)


    return start_btn, how_btn, settings_btn, game_theme_btn, scores_btn, sound_button_rect



def draw_username_screen():
    global user_text, input_active, error_message
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    label = title_font.render("Enter your username", True, theme_colors[current_theme]["TEXT"])
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 3 - 50))

    # Input kutusu
    input_rect = pygame.Rect(WIDTH // 2 - 250 , HEIGHT // 3 + 50, 450, 60)
    pygame.draw.rect(screen, GRAY, input_rect, border_radius=10)
    pygame.draw.rect(screen, theme_colors[current_theme]["BUTTON"], input_rect, 3, border_radius=10)

    text_surface = button_font.render(user_text, True, theme_colors[current_theme]["BUTTON"])
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

    # İleri butonu
    next_btn = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 30, 150, 60)
    draw_button("NEXT", next_btn, theme_colors[current_theme]["BUTTON"])

    # Geri butonu
    back_btn = pygame.Rect(WIDTH // 2 - 165, HEIGHT // 2 + 30, 150, 60)


    draw_button("BACK", back_btn, theme_colors[current_theme]["BUTTON"])

    if error_message:
        error_text = button_font.render(error_message, True, RED)
        screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 2 + 110))

    return input_rect, next_btn, back_btn


def handle_username_input(event):
    global user_text, input_active
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Eğer kullanıcı input kutusuna tıklarsa, aktif hale gelsin
        input_rect, next_btn, back_btn = draw_username_screen()
        if input_rect.collidepoint(event.pos):
            input_active = True
        else:
            input_active = False

    if event.type == pygame.KEYDOWN and input_active:
        if event.key == pygame.K_BACKSPACE:
            user_text = user_text[:-1]  # Backspace ile son harfi sil
        elif len(user_text) < 30:  # Maksimum 10 karaktere izin ver
            user_text += event.unicode  # Tuşu 'user_text' stringine ekle


def draw_how_to_play():
    global is_mini_game
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    title = title_font.render("HOW TO PLAY", True, theme_colors[current_theme]["TEXT"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    instructions = [
        "1. Choose a theme.",
        "2. Choose a difficulty level.",
        "3. Click two cards.",
        "4. Match pairs.",
        "5. Finish all to win!"
    ]
    for i, line in enumerate(instructions):
        txt = instruction_font.render(line, True, theme_colors[current_theme]["TEXT"])
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 150 + i * 40))
    back = pygame.Rect(WIDTH // 2 - 110, HEIGHT - 100, 200, 60)
    mini = pygame.Rect(WIDTH // 2 - 110, HEIGHT - 180, 200, 60)
    draw_button("LET'S TRY", mini, theme_colors[current_theme]["BUTTON"])
    draw_button("BACK", back, theme_colors[current_theme]["BUTTON"])
    return back, mini


def draw_theme_selection():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    label = title_font.render("Select Theme", True, theme_colors[current_theme]["TEXT"])
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 50))
    themes = ["weather", "magic", "space", "animal", "law", "hallowen"]
    icons = ["assets/Weather/1-1.png", "assets/Magic/1-1.png", "assets/Space/1-1.png", "assets/Animal/1-1.png", "assets/Law/1-1.png", "assets/Hallowen/1-1.png"]
    buttons = []
    button_width = 250
    button_height = 60
    button_spacing_vertical = 40
    button_spacing_horizontal = 50
    icon_size = 50
    # Sol sütun butonları
    for i in range(3):
        r = pygame.Rect(WIDTH // 4 - button_width // 2, 250 + i * (button_height + button_spacing_vertical),
                        button_width, button_height)
        draw_button(themes[i].upper(), r, theme_colors[current_theme]["BUTTON"])

        icon = pygame.image.load(icons[i])
        icon = pygame.transform.scale(icon, (icon_size, icon_size))
        icon_rect = icon.get_rect(center=(r.left - icon_size // 1 + 50, r.centery))  # İkonu sola yasla

        screen.blit(icon, icon_rect)
        buttons.append((r, themes[i]))

    # Sağ sütun butonları
    for i in range(3, 6):
        r = pygame.Rect(3 * WIDTH // 4 - button_width // 2, 250 + (i - 3) * (button_height + button_spacing_vertical),
                        button_width, button_height)
        draw_button(themes[i].upper(), r, theme_colors[current_theme]["BUTTON"])

        icon = pygame.image.load(icons[i])
        icon = pygame.transform.scale(icon, (icon_size, icon_size))
        icon_rect = icon.get_rect(center=(r.left - icon_size // 1 + 50, r.centery))  # İkonu sola yasla

        screen.blit(icon, icon_rect)
        buttons.append((r, themes[i]))

    # Geri butonu
    back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
    draw_button("BACK", back_btn, theme_colors[current_theme]["BUTTON"])

    return buttons, back_btn

def draw_difficulty_selection():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    label = title_font.render("Select Difficulty", True, theme_colors[current_theme]["TEXT"])
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 50))

    difficulties = ["Easy (2x2)", "Medium (4x4)", "Hard (6x6)"]
    buttons = []
    for i, diff in enumerate(difficulties):
        r = pygame.Rect(WIDTH // 2 - 150, 150 + i * 100, 300, 60)
        draw_button(diff, r, theme_colors[current_theme]["BUTTON"])
        buttons.append((r, diff))

    # Create a back button
    back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
    draw_button("Back", back_btn, theme_colors[current_theme]["BUTTON"])

    return buttons, back_btn  # Ensure you return both buttons and back button


def draw_game_mode_screen():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    label = title_font.render("Select Game Mode", True, theme_colors[current_theme]["TEXT"])
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 100))

    normal_button = pygame.Rect(WIDTH // 2 - 150, 250, 300, 70)
    penalty_button = pygame.Rect(WIDTH // 2 - 150, 360, 300, 70)
    back_btn = pygame.Rect(WIDTH // 2 - 150, 470, 300, 70)

    draw_button("Normal Game", normal_button, theme_colors[current_theme]["BUTTON"])
    draw_button("Penalty Game", penalty_button, theme_colors[current_theme]["BUTTON"])
    draw_button("Back", back_btn, theme_colors[current_theme]["BUTTON"])

    return normal_button, penalty_button, back_btn


def draw_settings_menu():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])

    settings_title = title_font.render("Settings", True, theme_colors[current_theme]["TEXT"])
    screen.blit(settings_title, (WIDTH // 2 - settings_title.get_width() // 2, 100))

    # Slider özellikleri
    bar_x = WIDTH // 2 - 150
    bar_y = 250
    bar_width = 300
    bar_height = 20
    handle_x = int(bar_x + bar_width * volume)

    # Sliderı çiz
    volume_icons_rect = draw_slider(bar_x, bar_y, bar_width, bar_height, handle_x, volume, "Volume", volume_icon_small,volume_icon_large)

    # Geri butonu
    back = pygame.Rect(WIDTH // 2 - 100, 500, 200, 60)
    draw_button("BACK", back, theme_colors[current_theme]["BUTTON"])

    return bar_x, bar_y, bar_width, bar_height, back, volume_icons_rect


# Slider çizimi fonksiyonu
def draw_slider(x, y, width, height, handle_x, volume, label, icon_small, icon_large):
    segment_count = 10
    segment_width = width // segment_count

    # Renk tonu (temadan bağımsız)
    if volume < 0.3:
        slider_color = RED
    elif volume < 0.6:
        slider_color = YELLOW
    else:
        slider_color = GREEN

    # Slider zemin
    pygame.draw.rect(screen, GRAY, (x, y, width, height), border_radius=4)
    pygame.draw.rect(screen, slider_color, (x, y, handle_x - x, height), border_radius=4)

    # Segment efekti
    for i in range(segment_count):
        if i < volume * segment_count:
            pygame.draw.rect(screen, slider_color, (x + i * segment_width, y, segment_width, height), border_radius=4)

    # Kaydırma topu
    pygame.draw.circle(screen, (50, 50, 50), (handle_x + 4, y + height // 2 + 4), 14)
    pygame.draw.circle(screen, (255, 255, 255), (handle_x, y + height // 2), 14)
    pygame.draw.circle(screen, (150, 150, 150), (handle_x, y + height // 2), 12)

    # İkonlar
    icon_small_rect = screen.blit(icon_small, (x - 70, y - 20))
    icon_large_rect = screen.blit(icon_large, (x + width + 20, y - 20))

    # Ses Yüzdesi
    vol_text = pygame.font.Font(None, 28).render(f"{int(volume * 100)}%", True, theme_colors[current_theme]["TEXT"])
    screen.blit(vol_text, (WIDTH // 2 - vol_text.get_width() // 2, y - 35))

    # Etiket
    label_text = pygame.font.Font(None, 30).render(label, True, theme_colors[current_theme]["TEXT"])
    screen.blit(label_text, (WIDTH // 2 - label_text.get_width() // 2, y - 60))

    return icon_small_rect, icon_large_rect


def draw_congrats(score, difficulty=None):
    screen.fill(theme_colors[current_theme]["BACKGROUND"])

    # Yıldızları çiz (temadan bağımsız)
    for star in stars:
        pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), 3)
        star[1] += star[2]
        if star[1] > HEIGHT:
            star[1] = random.randint(-50, -10)
            star[0] = random.randint(0, WIDTH)
            star[2] = random.uniform(1, 3)

    # "CONGRATULATIONS!" yazısı
    congrats_text = title_font.render("CONGRATULATIONS!", True, theme_colors[current_theme]["TEXT"])
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, 50))

    # Oyuncunun kendi skoru
    player_score_text = button_font.render(f"Your Score: {score}", True, theme_colors[current_theme]["TEXT"])
    screen.blit(player_score_text, (WIDTH // 2 - player_score_text.get_width() // 2, 130))

    # Skor Tablosu Başlığı
    score_board_title = button_font.render("HIGH SCORES", True, theme_colors[current_theme]["BUTTON"])
    screen.blit(score_board_title, (WIDTH // 2 - score_board_title.get_width() // 2, 180))

    # Sütun Başlıkları
    column_names = ["NO", "USERNAME", "SCORE", "TIME", "MOVES"]
    column_widths = [50, 200, 100, 100, 150]
    start_x = WIDTH // 2 - sum(column_widths) // 2
    title_y = 250
    header_font = pygame.font.Font(font_path, 25)

    for i, name in enumerate(column_names):
        text = header_font.render(name, True, theme_colors[current_theme]["TEXT"])
        screen.blit(text, (start_x + sum(column_widths[:i]), title_y))

    pygame.draw.line(screen, theme_colors[current_theme]["TEXT"], (start_x, title_y + 30),
                     (start_x + sum(column_widths), title_y + 30), 2)

    # Skorları çiz
    high_scores = get_high_scores(difficulty=difficulty)
    score_y = title_y + 50
    score_font = pygame.font.Font(None, 30)

    for i, score_data in enumerate(high_scores):
        username, score_val, time_val, moves_val = score_data
        row = [f"{i + 1}.", username, str(score_val), f"{time_val}s", str(moves_val)]
        x_offset = 0
        for j, item in enumerate(row):
            text = score_font.render(item, True, theme_colors[current_theme]["TEXT"])
            screen.blit(text, (start_x + x_offset + (column_widths[j] - text.get_width()) // 2, score_y))
            x_offset += column_widths[j]
        score_y += 30
        if score_y > HEIGHT - 150:  # Çok fazla skor göstermeyi engelle
            break

    # Butonlar
    button_y = HEIGHT - 100
    new_game_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 200, 220, 60)
    draw_button("NEW GAME", new_game_btn, theme_colors[current_theme]["BUTTON"])

    exit_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 270, 220, 60)
    draw_button("EXIT", exit_btn, theme_colors[current_theme]["BUTTON"])

    return new_game_btn, exit_btn

def show_congrats_screen(score, difficulty):
    while True:
        new_game_btn, exit_btn = draw_congrats(score, difficulty)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_btn.collidepoint(event.pos):
                    sound_congrats.stop()
                    pygame.mixer.music.play(-1)
                    return "new_game"
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def draw_high_scores():
    global current_screen, current_difficulty_filter
    screen.fill(theme_colors[current_theme]["BACKGROUND"])

    title = title_font.render("HIGH SCORES", True, theme_colors[current_theme]["TEXT"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    difficulties = ["Easy", "Medium", "Hard", "All"]
    buttons = []
    button_width = 160
    button_height = 50
    start_x = 130  # Sol taraftan başlayacak bir boşluk belirle
    button_spacing = 20  # Butonlar arasındaki yatay boşluk
    button_y = 150

    for i, diff in enumerate(difficulties):
        rect = pygame.Rect(start_x + i * (button_width + button_spacing), button_y, button_width, button_height)
        draw_button(diff, rect, theme_colors[current_theme]["BUTTON"])
        buttons.append((rect, diff))

    # Skor Tablosu Başlığı (zorluğa göre değişecek)
    selected_difficulty_text = current_difficulty_filter.upper() if current_difficulty_filter else "ALL"
    score_board_title = button_font.render(f"SCORES ({selected_difficulty_text})", True,
                                           theme_colors[current_theme]["BUTTON"])
    screen.blit(score_board_title, (WIDTH // 2 - score_board_title.get_width() // 2, 220))

    # Sütun Başlıkları
    column_names = ["NO", "USERNAME", "SCORE", "TIME", "MOVES"]
    column_widths = [50, 200, 100, 100, 150]
    start_x_table = WIDTH // 2 - sum(column_widths) // 2
    title_y_table = 280
    header_font = pygame.font.Font(font_path, 25)

    for i, name in enumerate(column_names):
        text = header_font.render(name, True, theme_colors[current_theme]["TEXT"])
        screen.blit(text, (start_x_table + sum(column_widths[:i]), title_y_table))

    pygame.draw.line(screen, theme_colors[current_theme]["TEXT"], (start_x_table, title_y_table + 30),
                     (start_x_table + sum(column_widths), title_y_table + 30), 2)

    high_scores = get_high_scores(difficulty=current_difficulty_filter)
    score_y = title_y_table + 50
    score_font = pygame.font.Font(None, 30)

    for i, score_data in enumerate(high_scores):
        username, score_val, time_val, moves_val = score_data
        row = [f"{i + 1}.", username, str(score_val), f"{time_val}s", str(moves_val)]
        x_offset = 0
        for j, item in enumerate(row):
            text = score_font.render(item, True, theme_colors[current_theme]["TEXT"])
            screen.blit(text, (start_x_table + x_offset + (column_widths[j] - text.get_width()) // 2, score_y))
            x_offset += column_widths[j]
        score_y += 30
        if score_y > HEIGHT - 150:
            break

    # Geri butonu
    back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
    draw_button("BACK", back_button, theme_colors[current_theme]["BUTTON"])

    return buttons, back_button

def show_game_over_screen(message):
    global screen
    pygame.mixer.music.stop()
    sound_gameover.play()
    screen.fill((20, 0, 0))  # Daha koyu arka plan

    # Fontu küçülttüm
    font_size = 70
    font = pygame.font.Font("fonts/OkayJelly.otf", font_size)

    # Mesajı \n ve boşluklardan bölüp satır satır yazdır
    lines = []
    for line in message.split('\n'):
        # Çok uzun satırları kelimelerine böl ve her 15 karakterden sonra yeni satır yap
        words = line.split(' ')
        current_line = ""
        for word in words:
            if len(current_line + word) > 15:
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line += word + " "
        if current_line:
            lines.append(current_line.strip())

    # Yazıları ortalamak için toplam yükseklik
    line_height = font.get_height()
    total_height = line_height * len(lines)

    start_y = HEIGHT // 2 - total_height // 2 - 100

    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 100, 100))
        text_rect = text.get_rect(center=(WIDTH // 2, start_y + i * line_height))
        screen.blit(text, text_rect)

    # Back button
    back_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 100, 300, 70)
    pygame.draw.rect(screen, (150, 0, 0), back_button, border_radius=15)
    pygame.draw.rect(screen, (255, 50, 50), back_button, width=3, border_radius=15)
    button_font = pygame.font.Font("fonts/OkayJelly.otf", 28)
    button_text = button_font.render("BACK TO MENU", True, (255, 180, 180))
    button_text_rect = button_text.get_rect(center=back_button.center)
    screen.blit(button_text, button_text_rect)
    pygame.display.flip()

    # Parçacık animasyonu (aynı şekilde devam eder)
    particles = []
    for _ in range(60):
        x = random.randint(0, WIDTH)
        y = random.randint(-100, 0)
        dx = random.uniform(-0.5, 0.5)
        dy = random.uniform(1, 2)
        size = random.randint(3, 6)
        color = random.choice([
            (255, 30, 30), (180, 0, 0), (255, 80, 80), (120, 0, 0)
        ])
        particles.append([x, y, dx, dy, size, color])

    clock = pygame.time.Clock()
    running_animation = True
    while running_animation:
        screen.fill((20, 0, 0))
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 100, 100))
            text_rect = text.get_rect(center=(WIDTH // 2, start_y + i * line_height))
            screen.blit(text, text_rect)

        pygame.draw.rect(screen, (150, 0, 0), back_button, border_radius=15)
        pygame.draw.rect(screen, (255, 50, 50), back_button, width=3, border_radius=15)
        screen.blit(button_text, button_text_rect)

        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            if p[1] > HEIGHT:
                p[0] = random.randint(0, WIDTH)
                p[1] = random.randint(-100, 0)
                p[2] = random.uniform(-0.5, 0.5)
                p[3] = random.uniform(1, 2)
                p[4] = random.randint(3, 6)
                p[5] = random.choice([
                    (255, 30, 30), (180, 0, 0), (255, 80, 80), (120, 0, 0)
                ])
            pygame.draw.circle(screen, p[5], (int(p[0]), int(p[1])), p[4])

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running_animation = False
                    pygame.mixer.music.play(-1)
                    return "main_menu"


def reset_game_state():
    global score, moves, start_time, matched_pairs, selected_cards
    global current_screen, cards, theme, difficulty, username, is_mini_game
    score = 0
    moves = 0
    matched_pairs = 0
    selected_cards = []
    start_time = pygame.time.get_ticks()
    theme = None
    difficulty = None
    is_mini_game = False
    cards = []
    current_screen = "main_menu"


def initialize_database():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                username TEXT NOT NULL,
                score INTEGER NOT NULL,
                time INTEGER NOT NULL,
                moves INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    conn.close()


initialize_database()  # Oyun başladığında çağırılabilir


def save_score(username, score, elapsed_time, moves, difficulty):
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO high_scores (username, score, time, moves, difficulty) VALUES (?, ?, ?, ?, ?)",
                   (username, score, elapsed_time, moves, difficulty))
    conn.commit()
    conn.close()


def get_high_scores(difficulty=None,limit=5):
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    if difficulty:
        # Eğer zorluk seviyesi belirtildiyse, filtrele
        cursor.execute(
            f"SELECT username, score, time, moves FROM high_scores WHERE difficulty = ? ORDER BY time ASC, moves ASC, score DESC LIMIT {limit}",
            (difficulty,))
    else:
        # Zorluk seviyesi belirtilmezse, tüm skorları getir
        cursor.execute(
            f"SELECT username, score, time, moves FROM high_scores ORDER BY time ASC, moves ASC, score DESC LIMIT {limit}")
    high_scores = cursor.fetchall()
    conn.close()
    return high_scores


def game_loop(pair_count, theme, penalty_mode=False, is_mini_game=False):
    global current_screen, score, start_time, moves, sound_on, is_paused, cards, grid_size, flipped, wait_time, clock, pause_button_rect, username, difficulty

    moves = 0
    score = 0
    cards, grid_size = create_game_board(pair_count, theme)
    flipped = []
    wait_time = 0
    start_time = pygame.time.get_ticks()
    is_paused = False
    pause_button_rect = None
    hint_button_rect = None
    refresh_img = pygame.image.load("assets/refresh.png")
    refresh_img = pygame.transform.scale(refresh_img, (100, 100))
    refresh_rect = refresh_img.get_rect(topright=(SCREEN_WIDTH - 160, -5))

    running = True
    while running:
        screen.fill(theme_colors[current_theme]["BACKGROUND"])
        click = False
        mouse = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                click = True
                if refresh_rect.collidepoint(e.pos):
                    game_loop(pair_count, theme, penalty_mode, is_mini_game)
                    return
                if volume_icon_rect.collidepoint(e.pos):
                    sound_on = not sound_on
                    pygame.mixer.music.set_volume(1.0 if sound_on else 0.0)
                if pause_button_rect and pause_button_rect.collidepoint(e.pos):
                    is_paused = True
                    pause_start_time = pygame.time.get_ticks()

        if is_paused:
            bar_x, bar_y, bar_width, bar_height, pause_new_game_rect, pause_resume_rect, pause_exit_rect, slider_rect, volume_icons_rect = draw_pause_screen()
            icon_small_rect, icon_large_rect = volume_icons_rect
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if pause_new_game_rect.collidepoint(e.pos):
                        current_screen = "main_menu"
                        running = False
                    elif pause_resume_rect.collidepoint(e.pos):
                        is_paused = False
                        start_time = pygame.time.get_ticks() - (pause_start_time - start_time)
                    elif pause_exit_rect.collidepoint(e.pos):
                        pygame.quit()
                        exit()
                    elif slider_rect and slider_rect[0] <= e.pos[0] <= slider_rect[0] + slider_rect[2] and slider_rect[
                        1] <= e.pos[1] <= slider_rect[1] + slider_rect[3]:
                        global volume
                        volume = (e.pos[0] - slider_rect[0]) / slider_rect[2]
                        volume = max(0, min(1, volume))
                        pygame.mixer.music.set_volume(volume)
                        sound_on = True if volume > 0 else False
                        # Ses kapama ikonuna tıklama
                    elif icon_small_rect.collidepoint(e.pos):
                        pygame.mixer.music.set_volume(0.0)
                        volume = 0.0
                        sound_on = False
                        # Ses açma ikonuna tıklama
                    elif icon_large_rect.collidepoint(e.pos):
                        pygame.mixer.music.set_volume(1.0)
                        volume = 1.0
                        sound_on = True

            continue

        for card in cards:
            card.draw(screen)

        # Skor ve zaman
        pause_button_rect = draw_score_and_time()
        screen.blit(refresh_img, refresh_rect)

        # HINT BUTONU
        hint_button_width = 120
        hint_button_height = 50
        hint_button_rect = pygame.Rect(20, SCREEN_HEIGHT - hint_button_height - 100, hint_button_width, hint_button_height)
        shadow_rect = pygame.Rect(hint_button_rect.x + 3, hint_button_rect.y + 3, hint_button_width, hint_button_height)
        pygame.draw.rect(screen, (180, 180, 180), shadow_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 204, 0), hint_button_rect, border_radius=15)
        hint_icon = pygame.image.load("assets/hint_icon.png")
        hint_icon = pygame.transform.scale(hint_icon, (40, 40))
        screen.blit(hint_icon, (hint_button_rect.x + 5, hint_button_rect.y + (hint_button_height - 40) // 2))
        small_font = pygame.font.Font("fonts/OkayJelly.otf", 22)
        hint_text = small_font.render("HINT", True, (0, 0, 0))
        screen.blit(hint_text, (hint_button_rect.x + 50, hint_button_rect.y + 13))

        if click and hint_button_rect and hint_button_rect.collidepoint(mouse):
            if score >= 20:
                score -= 20
                for card in cards:
                    if not card.matched:
                        card.flipped = True
                screen.fill(theme_colors[current_theme]["BACKGROUND"])
                for card in cards:
                    card.draw(screen)
                draw_score_and_time()
                pygame.draw.rect(screen, (255, 204, 0), hint_button_rect, border_radius=15)
                screen.blit(hint_text, (hint_button_rect.x + 50, hint_button_rect.y + 13))
                pygame.display.flip()
                pygame.time.wait(1000)
                for card in cards:
                    if not card.matched:
                        card.flipped = False
            else:
                print("Not enough points for a hint.")

        # Kartlara tıklama
        if click and wait_time == 0:
            for card in cards:
                if card.rect.collidepoint(mouse) and not card.flipped and not card.matched:
                    card.flipped = True
                    flipped.append(card)
                    sound_flip.play()
                    if len(flipped) == 2:
                        a, b = flipped
                        if a.icon_name.split('-')[0] == b.icon_name.split('-')[0]:
                            a.matched = b.matched = True
                            score += 10
                            flipped = []
                            sound_correct.play()
                        else:
                            if penalty_mode:
                                score -= 5
                            wait_time = now + 800
                            sound_incorrect.play()
                        moves += 1
                    break

        if wait_time and now >= wait_time:
            for card in flipped:
                card.flipped = False
            flipped = []
            wait_time = 0

        # 🔚 Oyun Bitti mi Kontrolü
        if all(c.matched for c in cards):
           pygame.display.flip()
           pygame.time.wait(500)
           elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
           if not is_mini_game:
              save_score(username, score, elapsed_time, moves, difficulty)

           if penalty_mode and score < 0:
              result = show_game_over_screen("You lost!    Your score is below 0.")
              if result == "main_menu":
                 current_screen = "main_menu"
                 running = False
           else:
                pygame.mixer.music.stop()
                sound_congrats.play()
                result = show_congrats_screen(score, difficulty)
                if result == "new_game":
                    current_screen = "main_menu"
                    running = False
                sound_incorrect.stop()


        pygame.display.flip()
        clock.tick(60)
    return


def draw_game_mode_selection():
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    label = title_font.render("Select Game Mode", True, theme_colors[current_theme]["TEXT"])
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 50))

    modes = ["Normal", "Penalty"]
    buttons = []

    # Buton konumları ortalanarak yerleştirildi
    total_height = len(modes) * 80 + (len(modes) - 1) * 20  # buton + boşluk yüksekliği
    start_y = (HEIGHT - total_height) // 2

    for i, mode in enumerate(modes):
        r = pygame.Rect(WIDTH // 2 - 100, start_y + i * 80, 200, 60)
        draw_button(mode, r, theme_colors[current_theme]["BUTTON"])  # Beyaz yazı
        buttons.append((r, mode))

    # Back butonu en alta ortalı
    back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
    draw_button("Back", back_btn, theme_colors[current_theme]["BUTTON"])

    return buttons, back_btn


def game_theme_selection():
    global current_screen, current_theme
    running = True
    theme_names = ["default", "pink", "blue", "nature", "night", "retro"]
    theme_icons = {
        "default": "default.png",  # Örnek ikon isimleri, gerçek dosya adlarınızı yazın
        "pink": "pink.png",
        "blue": "blue.png",
        "nature": "nature.png",
        "night": "night.png",
        "retro": "retro.png",
    }
    icon_size = 45  # İkon boyutunu ayarlayabilirsiniz
    while running:
        screen.fill(theme_colors[current_theme]["BACKGROUND"])
        label = title_font.render("Select Game Theme", True, theme_colors[current_theme]["TEXT"])
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 50))

        button_height = 60
        button_width = 300
        start_y = HEIGHT // 3
        button_spacing = 80
        buttons = []

        # Sol alt alta butonlar ve ikonlar
        left_start_x = WIDTH // 4 - button_width // 2
        for i in range(3):
            if i < len(theme_names):
                theme = theme_names[i]
                rect = pygame.Rect(left_start_x, start_y + i * button_spacing, button_width, button_height)
                draw_button(theme.upper(), rect, theme_colors[current_theme]["BUTTON"])
                buttons.append((rect, theme))
                # İkonu yükle ve çiz
                icon_path = os.path.join("assets", theme_icons.get(theme, "default.png")) # İkon yoksa default kullan
                try:
                    icon = pygame.image.load(icon_path)
                    icon = pygame.transform.scale(icon, (icon_size, icon_size))
                    icon_rect = icon.get_rect(center=(rect.left - icon_size // 1 + 80 , rect.centery))
                    screen.blit(icon, icon_rect)
                except pygame.error as e:
                    print(f"Icon loading error: {icon_path} - {e}")

        # Sağ alt alta butonlar ve ikonlar
        right_start_x = 3 * WIDTH // 4 - button_width // 2
        for i in range(3, 6):
            if i < len(theme_names):
                theme = theme_names[i]
                rect = pygame.Rect(right_start_x, start_y + (i - 3) * button_spacing, button_width, button_height)
                draw_button(theme.upper(), rect, theme_colors[current_theme]["BUTTON"])
                buttons.append((rect, theme))
                # İkonu yükle ve çiz
                icon_path = os.path.join("assets", theme_icons.get(theme, "default.png")) # İkon yoksa default kullan
                try:
                    icon = pygame.image.load(icon_path)
                    icon = pygame.transform.scale(icon, (icon_size, icon_size))
                    icon_rect = icon.get_rect(center=(rect.left - icon_size // 1 + 80 , rect.centery))
                    screen.blit(icon, icon_rect)
                except pygame.error as e:
                    print(f"Icon loading error: {icon_path} - {e}")

        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
        draw_button("BACK", back_btn_rect, theme_colors[current_theme]["BUTTON"])

        click = False
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if click:
            for rect, theme in buttons:
                if rect.collidepoint(mouse_pos):
                    current_theme = theme
                    running = False
                    break
            if back_btn_rect.collidepoint(mouse_pos):
                running = False

        pygame.display.flip()
    return

# Ana oyun döngüsü
running = True
while running:
    screen.fill(theme_colors[current_theme]["BACKGROUND"])
    click = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            if volume_icon_rect.collidepoint(event.pos):
                sound_on = not sound_on
                if sound_on:
                    pygame.mixer.music.set_volume(1.0)
                else:
                    pygame.mixer.music.set_volume(0.0)
        if current_screen == "username":
            handle_username_input(event) # Klavyeden girişleri işle

    if current_screen == "main_menu":
        s_btn, h_btn, settings_btn, game_theme_btn, scores_btn, sound_button_rect = draw_main_menu()
        if click:
            if s_btn.collidepoint(mouse_pos):
                current_screen = "username"
            elif h_btn.collidepoint(mouse_pos):
                current_screen = "how_to_play"
            elif settings_btn.collidepoint(event.pos):
                current_screen = "settings"
            elif game_theme_btn.collidepoint(mouse_pos):
                game_theme_selection() # Tema seçim ekranına git
            elif scores_btn.collidepoint(mouse_pos):
                current_screen = "high_score"
            elif sound_button_rect.collidepoint(mouse_pos):
                sound_on = not sound_on
                if sound_on:
                    pygame.mixer.music.set_volume(1.0)
                else:
                    pygame.mixer.music.set_volume(0.0)

    elif current_screen == "username":
        input_box, next_btn, back_btn = draw_username_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    mouse_pos = event.pos
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if user_text.strip() != "":
                            username = user_text.strip()
                            current_screen = "theme_selection"
                            error_message = ""
                        else:
                            error_message = "Please enter a username!"
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        if click:
            if next_btn.collidepoint(mouse_pos):
                if user_text.strip() != "":
                    username = user_text.strip()
                    current_screen = "theme_selection"
                    error_message = ""  # hata mesajı sıfırlanır
                else:
                    error_message = "Please enter a username!"  # hata mesajı
            elif back_btn.collidepoint(mouse_pos):
                current_screen = "main_menu"

        # Ekranlar arası çizim
    elif current_screen == "main_menu":
        start_btn, _, _, _ = draw_main_menu()
    elif current_screen == "username":
        input_box, next_btn, back_btn = draw_username_screen()
    elif current_screen == "theme":
        current_screen = "theme_selection"

    elif current_screen == "how_to_play":
        back, mini = draw_how_to_play()
        if click:
            if back.collidepoint(mouse_pos):
                current_screen = "main_menu"
            elif mini.collidepoint(mouse_pos):
                is_mini_game = True
                game_loop(2, "weather")  # Örnek olarak "weather" teması ve 2x2 kartlar (kolay)

    elif current_screen == "theme_selection":
        buttons, back_btn = draw_theme_selection()
        if click:
            if back_btn.collidepoint(mouse_pos):
               current_screen = "main_menu"

            for btn, theme in buttons:
                if btn.collidepoint(mouse_pos):
                    current_screen = "difficulty_selection"
                    selected_theme = theme
                    break
            if back_btn.collidepoint(mouse_pos):
                current_screen = "username"

 # Difficulty selection screen
    elif current_screen == "difficulty_selection":
        buttons, back_btn = draw_difficulty_selection()
        if click:
            for btn, diff_text in buttons:  # 'diff_text' will be "Easy (2x2)", "Medium (4x4)", etc.
                if btn.collidepoint(mouse_pos):
                    if diff_text == "Easy (2x2)":
                        grid_size = 2  # 2x2 grid
                        pair_count = 2
                        difficulty = "easy"  # Assign the string 'easy' to the global 'difficulty'
                    elif diff_text == "Medium (4x4)":
                        grid_size = 4  # 4x4 grid
                        pair_count = 8
                        difficulty = "medium"  # Assign the string 'medium'
                    elif diff_text == "Hard (6x6)":
                        grid_size = 6  # 6x6 grid
                        pair_count = 18
                        difficulty = "hard"  # Assign the string 'hard'
                    current_screen = "game_mode_selection"
            if back_btn.collidepoint(mouse_pos):
                current_screen = "theme_selection"

            if back_btn.collidepoint(mouse_pos):
                current_screen = "theme_selection"

    # Game mode selection screen
    elif current_screen == "game_mode_selection":
        buttons, back_btn = draw_game_mode_selection()  # Function to draw game mode buttons
        if click:
            for btn, mode in buttons:
                if btn.collidepoint(mouse_pos):
                    if mode == "Normal":
                        game_loop(pair_count, selected_theme, penalty_mode=False)  # Normal game mode
                    elif mode == "Penalty":
                        game_loop(pair_count, selected_theme, penalty_mode=True)  # Penalty mode
                    break
            if back_btn.collidepoint(mouse_pos):
               current_screen = "difficulty_selection"

    elif current_screen == "settings":
        bar_x, bar_y, bar_width, bar_height, back_btn, volume_icons_rect = draw_settings_menu()
        icon_small_rect, icon_large_rect = volume_icons_rect
        if click:
            if back_btn.collidepoint(mouse_pos):
                current_screen = "main_menu"
            # Ses kontrolü
            if bar_x <= mouse_pos[0] <= bar_x + bar_width and bar_y <= mouse_pos[1] <= bar_y + bar_height:
                volume = (mouse_pos[0] - bar_x) / bar_width
                volume = max(0, min(1, volume))  # 0 ile 1 arasında sınırla
                pygame.mixer.music.set_volume(volume)
                sound_on = True if volume > 0 else False
                # Ses kapama ikonuna tıklama
            elif icon_small_rect.collidepoint(mouse_pos):
                pygame.mixer.music.set_volume(0.0)
                volume = 0.0
                sound_on = False
                # Ses açma ikonuna tıklama
            elif icon_large_rect.collidepoint(mouse_pos):
                pygame.mixer.music.set_volume(1.0)
                volume = 1.0
                sound_on = True


    elif current_screen == "congrats":
        new_game_btn, exit_btn = draw_congrats(score)
        if click:
            if new_game_btn.collidepoint(mouse_pos):
                current_screen = "main_menu"
            elif exit_btn.collidepoint(mouse_pos):
                running = False

    elif current_screen == "high_score":
        buttons, back_button = draw_high_scores()
        if click:
            for btn, diff in buttons:
                if btn.collidepoint(mouse_pos):
                    current_difficulty_filter = diff.lower() if diff != "All" else None
                    break
            if back_button.collidepoint(mouse_pos):
                current_screen = "main_menu"

    pygame.display.flip()

pygame.quit()
sys.exit()