import pygame
import sys

WIDTH, HEIGHT = 900, 600
FPS = 60
FONT_SIZE = 28
FONT_COLOR = (180, 220, 255)
BG_COLOR = (10, 10, 30)
NEON_BLUE = (0, 200, 255)
NEON_PURPLE = (180, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circuit Chivalry: The Grid")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)

# --- Главный экран ---


def main_menu():
    menu_choices = ["Начать игру", "Выход"]
    selected = 0
    running = True
    while running:
        screen.fill((15, 15, 40))
        title = font.render("CIRCUIT CHIVALRY", True, NEON_BLUE)
        subtitle = font.render("THE GRID", True, NEON_PURPLE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 170))
        y = 320
        for i, text in enumerate(menu_choices):
            color = NEON_BLUE if i == selected else FONT_COLOR
            surf = font.render(text, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += FONT_SIZE + 24
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
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()
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
        surf = font.render(line, True, FONT_COLOR)
        screen.blit(surf, (60, y))
        y += FONT_SIZE + 8


def draw_choices(choices, selected):
    y = HEIGHT - 120
    for idx, (text, _) in enumerate(choices):
        color = NEON_BLUE if idx == selected else NEON_PURPLE
        surf = font.render(f"> {text}", True, color)
        screen.blit(surf, (80, y))
        y += FONT_SIZE + 12


def main_loop():
    global current_scene, selected_choice
    running = True
    while running:
        screen.fill(BG_COLOR)
        if current_scene is None:
            main_menu()
            current_scene = 0
            selected_choice = 0
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
