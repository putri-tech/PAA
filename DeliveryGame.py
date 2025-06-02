import pygame
import os
import math
import heapq
import random

# Inisialisasi pygam.. ffdffe
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Delivery Game")

# Path folder game
game_folder = r"C:\Users\Asus\OneDrive\Game-2"

# Load gambar
try:
    road_img = pygame.image.load(os.path.join(game_folder, "road4.png"))
    courier_img = pygame.image.load(os.path.join(game_folder, "courier.png"))
    flag_img = pygame.image.load(os.path.join(game_folder, "flag.png"))
except pygame.error as e:
    print("Gagal memuat gambar:", e)
    exit()

# Resize gambar
courier_size = (60, 40)
flag_size = (60, 40)
courier_img = pygame.transform.scale(courier_img, courier_size)
flag_img = pygame.transform.scale(flag_img, flag_size)

# Koordinat awal
x, y = 100, 300
flag_x, flag_y = 700, 300
speed = 2
angle = 0

# Warna jalan
ROAD_COLOR = (100, 100, 100)

# Status kontrol
start = False
path = []

# Fungsi cek apakah pixel di jalan
def is_on_road(x, y):
    if 0 <= x < road_img.get_width() and 0 <= y < road_img.get_height():
        pixel_color = road_img.get_at((int(x), int(y)))
        return pixel_color[:3] == ROAD_COLOR
    return False

# Fungsi pathfinding A*
def find_path(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if math.dist(current, goal) < 5:  # Dianggap sampai tujuan
            goal = current
            break

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_pos = (current[0] + dx * 5, current[1] + dy * 5)
            if is_on_road(next_pos[0], next_pos[1]):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + math.dist(next_pos, goal)
                    heapq.heappush(open_set, (priority, next_pos))
                    came_from[next_pos] = current

    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Acak posisi flag yang valid di jalan
def randomize_flag_position():
    global flag_x, flag_y, path
    while True:
        new_x = random.randint(0, road_img.get_width() - 1)
        new_y = random.randint(0, road_img.get_height() - 1)
        if is_on_road(new_x, new_y):
            flag_x, flag_y = new_x, new_y
            break
    path = find_path((x, y), (flag_x, flag_y))  # Reset path setelah acak
    # Tidak langsung start — tunggu tombol Start ditekan

# Gerakkan kurir ke arah jalur
def move_towards_path():
    global x, y, angle, path, start
    if path:
        next_x, next_y = path.pop(0)
        angle = math.atan2(next_y - y, next_x - x)
        x, y = next_x, next_y
    if not path:
        start = False  # Berhenti jika jalur habis

# Loop utama
running = True
path = find_path((x, y), (flag_x, flag_y))

while running:
    screen.fill((255, 255, 255))
    screen.blit(road_img, (0, 0))
    screen.blit(flag_img, (flag_x, flag_y))

    if start and path:
        move_towards_path()

    rotated_courier = pygame.transform.rotate(courier_img, -math.degrees(angle))
    rect = rotated_courier.get_rect(center=(x, y))
    screen.blit(rotated_courier, rect.topleft)

    # Tombol UI
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (0, 0, 0))
    stop_text = font.render("Stop", True, (0, 0, 0))
    random_text = font.render("Acak", True, (0, 0, 0))

    start_rect = pygame.Rect(800, 500, 80, 40)
    stop_rect = pygame.Rect(900, 500, 80, 40)
    random_rect = pygame.Rect(700, 500, 80, 40)

    pygame.draw.rect(screen, (200, 200, 200), start_rect)
    pygame.draw.rect(screen, (200, 200, 200), stop_rect)
    pygame.draw.rect(screen, (200, 200, 200), random_rect)

    screen.blit(start_text, (820, 510))
    screen.blit(stop_text, (920, 510))
    screen.blit(random_text, (720, 510))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                start = True
                path = find_path((x, y), (flag_x, flag_y))
            elif stop_rect.collidepoint(event.pos):
                start = False
            elif random_rect.collidepoint(event.pos):
                randomize_flag_position()

pygame.quit()
