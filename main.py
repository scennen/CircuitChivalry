import pygame
import sys
import os

WIDTH, HEIGHT = 1080, 720
FPS = 60
FONT_SIZE_TITLE = 64
FONT_SIZE_TEXT = 28
FONT_SIZE_BUTTON = 32
FONT_COLOR = (200, 240, 255)
BG_COLOR = (0, 22, 33)
NEON_BLUE = (51, 252, 252)
NEON_PURPLE = (220, 0, 255)
BLACK = (0, 0, 0)
GRAPHITE = (80, 80, 80)
NEON_BLUE_SILVER = (150, 220, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circuit Chivalry: The Grid")
clock = pygame.time.Clock()

# шрифты
font_path = os.path.join("font", "alagard-12px-unicode.ttf")
font_title = pygame.font.Font(font_path, FONT_SIZE_TITLE)
font_text = pygame.font.Font(font_path, FONT_SIZE_TEXT)
font_button = pygame.font.Font(font_path, FONT_SIZE_BUTTON)

# --- Классы персонажей ---


class Knight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.armor = 50
        self.sword = "Чёрный меч с голубыми трещинами"
        self.neon_armor = False

    def take_damage(self, damage):
        if self.neon_armor:
            self.armor -= damage
            if self.armor < 0:
                self.hp += self.armor
                self.armor = 0
        else:
            self.hp -= damage

    def activate_neon_armor(self):
        self.neon_armor = True
        self.armor = 100


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 50
        self.damage = 10

    def attack(self, knight):
        knight.take_damage(self.damage)


class Shadow:
    def __init__(self, x, y, knight_hp):
        self.x = x
        self.y = y
        self.hp = knight_hp
        self.damage = 15

    def attack(self, knight):
        knight.take_damage(self.damage)


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 20
        self.damage = 5

    def attack(self, knight):
        knight.take_damage(self.damage)


class CoreGuardian:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 200
        self.damage = 30
        self.arms = 4
        self.weapons = ["меч", "топор", "щит", "энергопушка"]

    def attack(self, knight):
        knight.take_damage(self.damage)

    def lose_arm(self):
        self.arms -= 1
        if self.arms == 0:
            self.hp = 0


class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 300
        self.damage = 40
        self.phase = 1

    def attack(self, knight):
        knight.take_damage(self.damage)

    def change_phase(self):
        self.phase += 1
        if self.phase == 2:
            self.damage = 60

# --- Главный экран ---


def main_menu():
    menu_choices = ["Начать игру", "Выход"]
    selected = 0
    running = True
    while running:
        screen.fill(BG_COLOR)
        title = font_title.render("CIRCUIT CHIVALRY", True, NEON_BLUE_SILVER)
        subtitle = font_title.render("THE GRID", True, NEON_BLUE_SILVER)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 170))
        y = 320
        for i, text in enumerate(menu_choices):
            color = NEON_BLUE_SILVER if i == selected else GRAPHITE
            surf = font_button.render(text, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += FONT_SIZE_BUTTON + 24
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_choices)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_choices)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        running = False
                        battle_scene()
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()
        clock.tick(FPS)

# --- Сцена на поле битвы ---


def battle_scene():
    battle_text = [
        "Поле битвы. Вокруг хаос: щиты, стрелы, рыцари под разными гербами.",
        "Ты отбиваешься от трёх врагов. Внезапно удар сбивает шлем, следующий — выбивает меч из рук.",
        "В грязи рядом — чёрный меч с голубыми трещинами. Что делать?"
    ]
    battle_choices = [
        ("Взять чёрный меч", 1),
        ("Попытаться отбиться без оружия", 2)
    ]
    selected = 0
    running = True
    while running:
        screen.fill(BG_COLOR)
        y = 60
        for line in battle_text:
            surf = font_text.render(line, True, FONT_COLOR)
            screen.blit(surf, (60, y))
            y += FONT_SIZE_TEXT + 8
        y = HEIGHT - 120
        for idx, (text, _) in enumerate(battle_choices):
            color = NEON_BLUE_SILVER if idx == selected else GRAPHITE
            surf = font_button.render(f"> {text}", True, color)
            screen.blit(surf, (80, y))
            y += FONT_SIZE_BUTTON + 12
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(battle_choices)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(battle_choices)
                elif event.key == pygame.K_RETURN:
                    _, next_scene = battle_choices[selected]
                    if next_scene == 1:
                        running = False
                        current_scene = 1
                    elif next_scene == 2:
                        running = False
                        current_scene = 2
        clock.tick(FPS)


# --- Текстовые сцены ---
scenes = [
    # 0: Интро битвы
    {
        "text": [
            "Поле битвы. Вокруг хаос: щиты, стрелы, рыцари под разными гербами.",
            "Ты отбиваешься от трёх врагов. Внезапно удар сбивает шлем, следующий — выбивает меч из рук.",
            "В грязи рядом — чёрный меч с голубыми трещинами. Что делать?"
        ],
        "choices": [
            ("Взять чёрный меч", 1),
            ("Попытаться отбиться без оружия", 2)
        ]
    },
    # 1: Перенос в The Grid
    {
        "text": [
            "Ты хватаешь меч — и всё замирает. Звуки боя глохнут, земля превращается в цифровую сетку.",
            "Вокруг — световая буря из синих и фиолетовых пикселей. Ты в The Grid!",
            "Твои доспехи покрыты неоновыми полосами, меч светится цифровыми символами."
        ],
        "choices": [
            ("Осмотреться", 3),
            ("Двигаться вперёд", 4)
        ]
    },
    # 2: Game Over
    {
        "text": [
            "Ты пытаешься отбиться, но враги окружают тебя. Последний удар — и всё гаснет...",
            "GAME OVER"
        ],
        "choices": [
            ("Начать сначала", 0)
        ]
    },
    # 3: Оглядеться в The Grid
    {
        "text": [
            "Вокруг башни-микросхемы, мосты из света, платформы. Саундтрек: басовые синтезаторы, электронные биты.",
            "Впереди — разрушенный шлюз. Путь только один: вперёд!"
        ],
        "choices": [
            ("Войти в шлюз", 4)
        ]
    },
    # 4: Сектор 1 — Разрушенный шлюз
    {
        "text": [
            "Сектор 1: Разрушенный шлюз. Цель: активировать 4 энергогенератора.",
            "Платформы исчезают, враги нападают. Ты готов?"
        ],
        "choices": [
            ("Прыгнуть на платформу", 5),
            ("Сразиться с врагом", 6)
        ]
    },
    # 5: Прыжок по платформам (placeholder)
    {
        "text": [
            "Ты прыгаешь на платформу. Она начинает исчезать под ногами!",
            "Впереди виден первый энергогенератор."
        ],
        "choices": [
            ("Бежать к генератору", 7)
        ]
    },
    # 6: Бой с врагом (placeholder)
    {
        "text": [
            "Враг бросается на тебя. Ты отражаешь удар неоновым мечом!",
            "Враг повержен, но впереди ещё опасности."
        ],
        "choices": [
            ("Двигаться дальше", 5)
        ]
    },
    # 7: Первый генератор (placeholder)
    {
        "text": [
            "Ты добрался до первого энергогенератора. Он окружён искрящимися кабелями.",
            "Ты активируешь его — вспышка света освещает сектор."
        ],
        "choices": [
            ("Искать следующий генератор", 8)
        ]
    },
    # 8: Продолжение сектора 1 (placeholder)
    {
        "text": [
            "Впереди ещё три генератора и всё больше врагов...",
            "(Дальнейшее развитие сектора 1 и переход к сектору 2 будет добавлено)"
        ],
        "choices": [
            ("Продолжить", 9)
        ]
    },
    # 9: Заглушка для следующих секторов
    {
        "text": [
            "Спасибо за игру! Продолжение следует..."
        ],
        "choices": [
            ("Выйти в главное меню", -1)
        ]
    },
]

current_scene = None  # None = главный экран
selected_choice = 0


def draw_text_lines(lines, y_start):
    y = y_start
    for line in lines:
        surf = font_text.render(line, True, FONT_COLOR)
        screen.blit(surf, (60, y))
        y += FONT_SIZE_TEXT + 8


def draw_choices(choices, selected):
    y = HEIGHT - 120
    for idx, (text, _) in enumerate(choices):
        color = NEON_BLUE_SILVER if idx == selected else GRAPHITE
        surf = font_button.render(f"> {text}", True, color)
        screen.blit(surf, (80, y))
        y += FONT_SIZE_BUTTON + 12


def main_loop():
    global current_scene, selected_choice
    running = True
    while running:
        screen.fill(BG_COLOR)
        if current_scene is None:
            main_menu()
            continue
        scene = scenes[current_scene]
        draw_text_lines(scene["text"], 60)
        draw_choices(scene["choices"], selected_choice)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_choice = (selected_choice -
                                       1) % len(scene["choices"])
                elif event.key == pygame.K_DOWN:
                    selected_choice = (selected_choice +
                                       1) % len(scene["choices"])
                elif event.key == pygame.K_RETURN:
                    _, next_scene = scene["choices"][selected_choice]
                    if next_scene == -1:
                        current_scene = None
                        selected_choice = 0
                    else:
                        current_scene = next_scene
                        selected_choice = 0
        clock.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_loop()
