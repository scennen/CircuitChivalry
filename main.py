import pygame
from levels.levels_and_transitions import (
    SurfaceLevel, MedievalTransition, NeonTransition, SimpleTransition,
    DestroyedGatewayLevel, DataTunnelLevel, ArenaLevel, BossLevel,
    TransitionLevel
)
from levels.transition_screen import TransitionScreen
from typing import Any
from entities.knight import Player, Enemy, PlayerNeon, EnemyNeon
from entities.entities import CoreGuardian
from entities.platform import Platform
import sys
from core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BUTTON_NEON_GLOW,
    FONT_PATH, FONT_TITLE_SIZE, FONT_BUTTON_SIZE, FONT_TEXT_SIZE, MENU_BG_IMAGE, GAME_TITLE
)
import os
import random


def get_levels():
    return [
        # Переход к битве
        {
            'type': 'transition',
            'title': '',
            'description': (
                'На поле, усеянном щитами и стрелами,\n'
                'сталкиваются рыцари под разными гербами.\n'
                'Главный герой отбивается от трёх врагов.\n'
                '\n'
                'Нажмите ENTER, чтобы продолжить.'
            )
        },
        # Переход к первому уровню
        {'type': 'transition', 'title': 'Уровень 1: Королевство',
            'description': 'Нажмите ENTER, чтобы начать.'},
        # Первый уровень, обычные враги
        {
            'type': 'level',
            'title': '1: Королевство',
            'enemy_count': max(1, 5 // 2),  # Минимум 1 враг
            'enemy_type': 'medieval'
        },
        # Переход после первого уровня
        {
            'type': 'transition',
            'title': '',
            'description': (
                'Внезапно удар сбивает с героя шлем,\n'
                'а следующий, вышибает меч из рук.\n'
                'Меч падает в грязь, и герой замечает рядом другой,\n'
                'лезвие идеально чёрное, с едва заметными голубыми трещинами.\n'
                'Он хватает меч, и всё замирает.\n'
                'Звуки боя глохнут, как будто кто-то выдернул штекер.\n'
                'Земля под ногами превращается в цифровую сетку,\n'
                'а вокруг него взрывается световая буря из синих и фиолетовых пикселей.\n'
                '\n'
                'Нажмите ENTER, чтобы продолжить.'
            )
        },
        # Переход ко второму уровню
        {'type': 'transition', 'title': 'Уровень 2', 'description': ''},
        # Второй уровень, неоновые враги
        {
            'type': 'transitionlevel',
            'enemy_count': max(1, 6 // 2),  # Здесь неоновые враги
            'enemy_type': 'neon'
        },
        # Переход к третьему уровню
        {'type': 'transition', 'title': 'Уровень 3: Разрушенный шлюз', 'description': ''},
        # Третий уровень, неоновые враги
        {
            'type': 'gateway',
            'enemy_count': max(1, 7 // 2),
            'enemy_type': 'neon'
        },
        # Переход к четвертому уровню
        {'type': 'transition', 'title': 'Уровень 4', 'description': ''},
        # Четвертый уровень, неоновые враги
        {
            'type': 'transitionlevel',
            'enemy_count': max(1, 7 // 2),
            'enemy_type': 'neon'
        },
        # Переход к пятому уровню
        {'type': 'transition', 'title': 'Уровень 5: Тунель данных', 'description': ''},
        # Пятый уровень, враги тени
        {
            'type': 'tunnel',
            'enemy_count': max(1, 8 // 2),
            'enemy_type': 'shadow'
        },
        # Переход к шестому уровню
        {'type': 'transition', 'title': 'Уровень 6', 'description': ''},
        # Шестой уровень, неоновые враги
        {
            'type': 'transitionlevel',
            'enemy_count': max(1, 8 // 2),
            'enemy_type': 'neon'
        },
        # Переход к седьмому уровню
        {'type': 'transition', 'title': 'Уровень 7: Арена', 'description': ''},
        # Седьмой уровень, враги тени
        {
            'type': 'arena',
            'enemy_count': max(1, 10 // 2),
            'enemy_type': 'shadow'
        },
        # Переход к восьмому уровню
        {'type': 'transition', 'title': 'Уровень 8', 'description': ''},
        # Восьмой уровень, враги тени
        {
            'type': 'transitionlevel',
            'enemy_count': max(1, 10 // 2),
            'enemy_type': 'shadow'
        },
        # Переход к боссу
        {'type': 'transition', 'title': 'Уровень 9: Босс', 'description': ''},
        # Уровень с боссом
        {
            'type': 'boss',
            'enemy_count': 1,  # Только один босс
            'enemy_type': 'boss'
        },
        # Переход к финалу
        {'type': 'transition', 'title': 'Уровень 10: Конец', 'description': ''},
        # Финальный уровень
        {
            'type': 'level',
            'title': '10: Конец',
            'enemy_count': max(1, 5 // 2),
            'enemy_type': 'medieval'  # Обычные враги
        },
    ]


def is_auto_transition(transition: Any) -> bool:
    return (
        hasattr(transition, 'title') and
        transition.title.strip().lower().startswith("уровень")
    )


def draw_text(surface: "pygame.Surface", text: str, font: "pygame.font.Font", color: tuple[int, int, int], pos: tuple[int, int]) -> "pygame.Rect":
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=pos)
    surface.blit(text_obj, rect)
    return rect


def load_font(path: str, size: int):
    try:
        font = pygame.font.Font(path, size)
        font.render("test", True, (0, 0, 0))
        return font
    except Exception as e:
        print(
            f"[WARNING] Не удалось загрузить кастомный шрифт: {e}. Используется стандартный.")
        return pygame.font.SysFont(None, size)


def play_music(track_or_list):
    if not hasattr(play_music, 'enabled'):
        play_music.enabled = True  # Включаем музыку по умолчанию
    if not play_music.enabled:
        pygame.mixer.music.pause()  # Если музыка выключена, ставим на паузу
        return
    if isinstance(track_or_list, list):
        # Если список, выбираем случайный трек
        track = random.choice(track_or_list)
    else:
        track = track_or_list  # Если строка, просто используем её
    if not hasattr(play_music, 'current') or play_music.current != track:
        try:
            pygame.mixer.music.stop()  # Останавливаем текущую музыку
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.load(track)  # Загружаем новый трек
            pygame.mixer.music.play(-1)
            play_music.current = track  # Запоминаем текущий трек
            if not play_music.enabled:
                pygame.mixer.music.pause()  # Если музыка выключена, ставим на паузу
        except Exception as e:
            # Ошибка при воспроизведении
            print(f'[MUSIC ERROR] Не удалось воспроизвести {track}: {e}')


def main_menu(screen: "pygame.Surface", clock: "pygame.time.Clock", can_continue: bool = False, pause_mode: bool = False):
    bg = pygame.image.load(MENU_BG_IMAGE).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    font = load_font(FONT_PATH, FONT_TITLE_SIZE)
    btn_font = load_font(FONT_PATH, FONT_BUTTON_SIZE)
    # Центрируем заголовок по центру экрана
    title_surface = font.render(GAME_TITLE, True, WHITE)
    title_rect = title_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    button_height = 60
    button_width = 400
    button_gap = 24
    #Музыка: глобальный флаг
    if not hasattr(play_music, 'enabled'):
        play_music.enabled = True
    # Кнопка музыки по центру и внизу
    music_btn = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2,
        SCREEN_HEIGHT - button_height - 60,
        button_width, button_height)
    # Кнопка музыки всегда последняя
    buttons: list[tuple[str, pygame.Rect]] = []
    if pause_mode:
        resume_btn = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - button_gap, button_width, button_height)
        buttons.append(('Продолжить', resume_btn))
        restart_btn = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                  SCREEN_HEIGHT // 2, button_width, button_height)
        buttons.append(('Начать заново', restart_btn))
        exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT //
                               2 + button_height + button_gap, button_width, button_height)
        buttons.append(('Выход', exit_btn))
    elif can_continue:
        continue_btn = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - button_gap, button_width, button_height)
        buttons.append(('Продолжить игру', continue_btn))
        start_btn = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                SCREEN_HEIGHT // 2, button_width, button_height)
        buttons.append(('Начать игру', start_btn))
        exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT //
                               2 + button_height + button_gap, button_width, button_height)
        buttons.append(('Выход', exit_btn))
    else:
        start_btn = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2, button_width, button_height)
        buttons.append(('Начать игру', start_btn))
        exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                               SCREEN_HEIGHT // 2 + button_height // 2 + button_gap, button_width, button_height)
        buttons.append(('Выход', exit_btn))
    # Добавляем кнопку музыки в конец
    buttons.append(
        (f'Музыка: {"ВКЛ" if play_music.enabled else "ВЫКЛ"}', music_btn))
    selected = 0
    while True:
        mouse = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(buttons)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(buttons)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == len(buttons) - 1:
                        # Переключаем музыку
                        play_music.enabled = not play_music.enabled
                        if play_music.enabled:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                        # Обновляем надпись
                        buttons[-1] = (
                            f'Музыка: {"ВКЛ" if play_music.enabled else "ВЫКЛ"}', music_btn)
                        continue
                    idx = selected
                    if pause_mode:
                        if idx == 0:
                            return 'resume'
                        elif idx == 1:
                            return 'restart'
                        else:
                            pygame.quit()
                            sys.exit()
                    elif can_continue and not pause_mode and idx == 0:
                        return 'continue'
                    elif (can_continue and not pause_mode and idx == 1) or (not can_continue and not pause_mode and idx == 0):
                        return 'start'
                    else:
                        pygame.quit()
                        sys.exit()
                if pause_mode and event.key == pygame.K_ESCAPE:
                    return 'resume'
        screen.blit(bg, (0, 0))
        # Центрируем заголовок
        screen.blit(title_surface, title_rect)
        for i, (text, btn) in enumerate(buttons):
            hover = btn.collidepoint(mouse)
            btn_surface = btn_font.render(
                text, True, BUTTON_NEON_GLOW if selected == i or hover else WHITE)
            btn_rect = btn_surface.get_rect(center=btn.center)
            screen.blit(btn_surface, btn_rect)
        pygame.display.flip()
        clock.tick(FPS)
        for i, (_, btn) in enumerate(buttons):
            if btn.collidepoint(mouse) and click:
                if i == len(buttons) - 1:
                    # Переключаем музыку
                    play_music.enabled = not play_music.enabled
                    if play_music.enabled:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    # Обновляем надпись
                    buttons[-1] = (
                        f'Музыка: {"ВКЛ" if play_music.enabled else "ВЫКЛ"}', music_btn)
                    continue
                idx = i
                if pause_mode:
                    if idx == 0:
                        return 'resume'
                    elif idx == 1:
                        return 'restart'
                    else:
                        pygame.quit()
                        sys.exit()
                elif can_continue and not pause_mode and idx == 0:
                    return 'continue'
                elif (can_continue and not pause_mode and idx == 1) or (not can_continue and not pause_mode and idx == 0):
                    return 'start'
                else:
                    pygame.quit()
                    sys.exit()


def get_player_for_level(level: object, floor_y: int, level_idx: int | None = None):
    if (level_idx in [2, 4, 6, 8]) or (hasattr(level, '__class__') and level.__class__.__name__ == 'TransitionLevel'):
        player_cls = PlayerNeon  # Для неоновых уровней используем PlayerNeon
    else:
        player_cls = Player  # Для остальных уровней обычный Player
    return player_cls(100, floor_y)


def game_over_screen(screen: "pygame.Surface", clock: "pygame.time.Clock", font: "pygame.font.Font"):
    bg_path = os.path.join("assets", "images", "backgrounds", "game_over.png")
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    title_font = pygame.font.Font(FONT_PATH, FONT_TITLE_SIZE)
    info_font = pygame.font.Font(FONT_PATH, FONT_TEXT_SIZE)
    title_text = "Поражение!"
    info_text = "Нажмите ENTER, чтобы вернуться в главное меню"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'menu'
        screen.blit(bg, (0, 0))
        # Заголовок
        title_surface = title_font.render(title_text, True, BUTTON_NEON_GLOW)
        title_rect = title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(title_surface, title_rect)
        # Информационный текст (уменьшенный шрифт)
        info_surface = info_font.render(info_text, True, WHITE)
        info_rect = info_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(info_surface, info_rect)
        pygame.display.flip()
        clock.tick(FPS)


def game_win_screen(screen: "pygame.Surface", clock: "pygame.time.Clock", font: "pygame.font.Font"):
    bg_path = os.path.join("assets", "images", "backgrounds", "victory.png")
    if os.path.exists(bg_path):
        bg = pygame.image.load(bg_path).convert()
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((0, 0, 0))
    title_font = pygame.font.Font(FONT_PATH, FONT_TITLE_SIZE)
    text_font = pygame.font.Font(FONT_PATH, FONT_TEXT_SIZE)
    title_text = "ПОБЕДА!"
    info_text = (
        "Вы победили всех врагов и спасли королевство.\n"
        "\n"
        "Но где-то внутри не покидает ощущение, что это ещё не конец...\n"
        "Покой кажется хрупким, словно затишье перед новой бурей.\n"
        "\n"
        "И всё же — вы завершили свой путь.\n"
        "\n"
        "Нажмите ENTER, чтобы вернуться в главное меню."
    )
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                    return
        screen.blit(bg, (0, 0))
        # Заголовок
        title_surface = title_font.render(title_text, True, BUTTON_NEON_GLOW)
        title_rect = title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        screen.blit(title_surface, title_rect)
        # Информационный текст
        lines = info_text.split('\n')
        for i, line in enumerate(lines):
            info_surface = text_font.render(line, True, WHITE)
            info_rect = info_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20 + i * 36))
            screen.blit(info_surface, info_rect)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f'[MIXER ERROR] {e}')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CircuitChivalry")
    clock = pygame.time.Clock()
    font = load_font(FONT_PATH, FONT_TITLE_SIZE)

    # Показываем главное меню перед стартом игры
    play_music(os.path.join('assets', 'music', 'Armory.mp3'))
    action = main_menu(screen, clock)
    if action != 'start':
        pygame.quit()
        sys.exit()

    level_entries = get_levels()

    def update_music_for_level(current):
        # Для TransitionLevel
        if hasattr(current, '__class__') and current.__class__.__name__ == 'TransitionLevel':
            play_music(os.path.join('assets', 'music', 'Derezzed.mp3'))
        # Для шлюза
        elif hasattr(current, '__class__') and current.__class__.__name__ == 'DestroyedGatewayLevel':
            play_music(os.path.join('assets', 'music', 'Castor.mp3'))
        # Для туннеля
        elif hasattr(current, '__class__') and current.__class__.__name__ == 'DataTunnelLevel':
            play_music(os.path.join('assets', 'music', 'Outlands.mp3'))
        # Для арены
        elif hasattr(current, '__class__') and current.__class__.__name__ == 'ArenaLevel':
            play_music(os.path.join('assets', 'music', 'Disc Wars.mp3'))
        # Для босса
        elif hasattr(current, '__class__') and current.__class__.__name__ == 'BossLevel':
            play_music(os.path.join('assets', 'music', 'End of Line.mp3'))
        # Для обычных экранов-переходов выключить музыку
        elif isinstance(current, TransitionScreen):
            pygame.mixer.music.stop()
            play_music.current = None
        # Для обычных уровней — можно добавить свою музыку, если нужно
        else:
            pygame.mixer.music.stop()
            play_music.current = None

    def make_level(entry: dict) -> object:
        # Получаем тип врагов из конфигурации
        enemy_type = entry.get('enemy_type', 'medieval')
        enemy_count = entry.get('enemy_count', 5)

        level = None
        if entry['type'] == 'transition':
            # Первый переход - особые цвета
            if entry['title'] == 'Битва начинается!':
                level = TransitionScreen(
                    title=entry['title'],
                    description=entry['description'],
                    bg_color=entry['bg_color'],
                    title_color=entry['title_color'],
                    desc_color=entry['desc_color'],
                    title_font_path="assets/fonts/alagard-12px-unicode.otf",
                    desc_font_path="assets/fonts/alagard-12px-unicode.otf"
                )
            elif entry['title'] == 'Уровень 1: Королевство':
                level = MedievalTransition()
            elif entry['title'] == 'Уровень 10: Конец':
                from levels.levels_and_transitions import EndTransition
                level = EndTransition()
            elif entry['title'].startswith('Уровень'):
                level = NeonTransition(
                    entry['title'],
                    entry.get('description', '')
                )
            else:
                level = SimpleTransition(
                    entry['title'],
                    entry.get('description', ''),
                    entry.get('bg_color', (30, 40, 70))
                )
        elif entry['type'] == 'transitionlevel':
            level = TransitionLevel(
                'assets/images/backgrounds/transition.png',
                enemy_count=enemy_count,
                enemy_type=enemy_type
            )
        elif entry['type'] == 'gateway':
            level = DestroyedGatewayLevel(
                enemy_count=enemy_count,
                enemy_type=enemy_type,
                floor_offset_from_bottom=100
            )
        elif entry['type'] == 'tunnel':
            level = DataTunnelLevel(
                enemy_count=enemy_count,
                enemy_type=enemy_type,
                floor_offset_from_bottom=100
            )
        elif entry['type'] == 'arena':
            level = ArenaLevel(
                enemy_count=enemy_count,
                enemy_type=enemy_type,
                floor_offset_from_bottom=100
            )
        elif entry['type'] == 'boss':
            level = BossLevel(
                enemy_count=enemy_count,
                enemy_type=enemy_type,
                floor_offset_from_bottom=100
            )
        else:
            # SurfaceLevel для обычных уровней
            level = SurfaceLevel(
                entry.get('title', ''),
                enemy_count=enemy_count,
                enemy_type=enemy_type,
                floor_offset_from_bottom=100
            )

        return level

    LEVELS = [make_level(e) for e in level_entries]
    level_idx = 0
    current = LEVELS[level_idx]
    if isinstance(current, SurfaceLevel):
        floor_y = current.floor_y
    else:
        floor_y = SCREEN_HEIGHT
    knight = get_player_for_level(current, floor_y, level_idx)
    current_player_type = type(knight)
    running = True
    in_transition = isinstance(LEVELS[level_idx], TransitionScreen)
    fade_surface = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    def get_floor_platform(level):
        if hasattr(level, 'floor_y'):
            y = level.floor_y
        else:
            y = SCREEN_HEIGHT
        return Platform(0, y, SCREEN_WIDTH, 20)

    floor_platform = get_floor_platform(current)
    update_music_for_level(current)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Пауза
                pause_action = main_menu(screen, clock, pause_mode=True)
                if pause_action == 'resume':
                    continue
                elif pause_action == 'restart':
                    # Перезапуск уровня
                    level_idx = 0
                    current = LEVELS[level_idx]
                    floor_platform = get_floor_platform(current)
                    knight = get_player_for_level(
                        current, floor_platform.rect.top, level_idx)
                    if hasattr(current, 'reset_enemies'):
                        current.reset_enemies()
                    if hasattr(current, 'start'):
                        current.start()  # Пересоздать врагов
                    continue
                else:
                    running = False
                    break
            # Только на экранах-переходах разрешаем переход по Enter
            if in_transition and not is_auto_transition(LEVELS[level_idx]):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level_idx += 1
                    if level_idx >= len(LEVELS):
                        # Победа! Показываем экран окончания
                        game_win_screen(screen, clock, font)
                        # Возврат в главное меню
                        running = False
                        break
                    else:
                        in_transition = isinstance(
                            LEVELS[level_idx], TransitionScreen)
                        current = LEVELS[level_idx]
                        floor_platform = get_floor_platform(current)
                        knight = get_player_for_level(
                            current, floor_platform.rect.top, level_idx)
                    continue

        if level_idx >= len(LEVELS):
            break

        current = LEVELS[level_idx]
        update_music_for_level(current)

        floor_platform = get_floor_platform(current)

        # Смена типа игрока при необходимости
        required_player_type = PlayerNeon if (
            hasattr(current, 'title') and (
                any(f"{i}:" in str(current.title) for i in range(2, 10)) or
                any(word in str(current.title).lower()
                    for word in ['шлюз', 'туннель', 'арена', 'босс'])
            )
        ) else Player

        if not isinstance(knight, required_player_type):
            # Передаём HP между уровнями
            prev_hp = getattr(knight, 'hp', 100)
            prev_max_hp = getattr(knight, 'max_hp', 100)
            knight = required_player_type(
                100, floor_platform.rect.top, hp=prev_hp)
            knight.max_hp = prev_max_hp
        else:
            knight.set_floor_y(floor_platform.rect.top)
        if hasattr(current, 'reset_enemies'):
            current.reset_enemies()

        if isinstance(current, TransitionScreen):
            # Промотка всех автопереходов подряд
            while (level_idx < len(LEVELS) and
                   isinstance(LEVELS[level_idx], TransitionScreen) and
                   is_auto_transition(LEVELS[level_idx])):
                current = LEVELS[level_idx]
                update_music_for_level(current)
                # Анимация прозрачности
                fade_in_time = 0.5
                show_time = 1.0
                fade_out_time = 0.5
                total_time = fade_in_time + show_time + fade_out_time
                start_time = pygame.time.get_ticks()
                while True:
                    now = pygame.time.get_ticks()
                    t = (now - start_time) / 1000.0
                    if t > total_time:
                        break
                    alpha = 255
                    if t < fade_in_time:
                        alpha = int(255 * (t / fade_in_time))
                    elif t > fade_in_time + show_time:
                        alpha = int(255 * (1 - (t - fade_in_time - show_time) /
                                           fade_out_time))
                    current.draw(screen)
                    fade_surface.fill((0, 0, 0, 255 - alpha))
                    screen.blit(fade_surface, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)
                level_idx += 1
                if level_idx >= len(LEVELS):
                    running = False
                    break
            if level_idx < len(LEVELS) and isinstance(LEVELS[level_idx], TransitionScreen):
                current = LEVELS[level_idx]
                update_music_for_level(current)
                current.draw(screen)
        else:
            # Основной игровой цикл для уровня
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()

            # Обновление игрока и врагов
            knight.handle_input(keys, mouse_buttons)
            knight.update(platforms=[floor_platform] +
                          getattr(current, 'platforms', []))

            # Атака игрока по врагам
            if hasattr(current, 'enemies'):
                knight.attack_enemies(current.enemies)

            # Обновляем врагов через метод уровня
            if hasattr(current, 'update_enemies'):
                current.update_enemies(
                    [floor_platform] + getattr(current, 'platforms', []), knight)
                
            if hasattr(current, 'hearts'):
                for heart in current.hearts[:]:
                    if knight.rect.colliderect(heart.rect) and knight.hp < knight.max_hp:
                        knight.hp = min(
                            knight.max_hp, knight.hp + heart.heal_amount)
                        current.hearts.remove(heart)

            if hasattr(current, 'blue_orb') and current.blue_orb:
                if knight.rect.colliderect(current.blue_orb.rect):
                    knight.hp = knight.max_hp
                    current.blue_orb = None

            if hasattr(current, 'extra_blue_orbs'):
                for orb in current.extra_blue_orbs[:]:
                    if knight.rect.colliderect(orb.rect):
                        knight.hp = knight.max_hp
                        current.extra_blue_orbs.remove(orb)

            # Отрисовка
            current.draw(screen)
            screen.blit(floor_platform.image, floor_platform.rect)

            # Отрисовка врагов через метод уровня
            if hasattr(current, 'draw_enemies'):
                current.draw_enemies(screen)

            knight.draw(screen)

            # Переход на следующий уровень при выходе за границы
            if hasattr(current, 'floor_y'):
                # Проверяем, есть ли живые враги
                enemies_alive = False
                if hasattr(current, 'enemies'):
                    for enemy in current.enemies:
                        if not getattr(enemy, 'is_dead', False):
                            enemies_alive = True
                            break
                if (knight.rect.right < 0 or knight.rect.left > SCREEN_WIDTH or knight.rect.left < 0):
                    if enemies_alive:
                        # Не даём выйти, возвращаем к краю
                        if knight.rect.right < 0:
                            knight.rect.left = 0
                        elif knight.rect.left > SCREEN_WIDTH:
                            knight.rect.right = SCREEN_WIDTH
                        elif knight.rect.left < 0:
                            knight.rect.left = 0
                    else:
                        level_idx += 1
                        if level_idx >= len(LEVELS):
                            # Победа! Показываем экран окончания
                            game_win_screen(screen, clock, font)
                            # Возврат в главное меню
                            running = False
                            break
                        elif level_idx > 20:
                            game_win_screen(screen, clock, font)
                            running = False
                            break
                        else:
                            in_transition = isinstance(
                                LEVELS[level_idx], TransitionScreen)
                            current = LEVELS[level_idx]
                            floor_platform = get_floor_platform(current)
                            knight = required_player_type(
                                100, floor_platform.rect.top)
                        continue

        # Проверка смерти игрока
        if hasattr(knight, 'hp') and knight.hp <= 0:
            font = load_font(FONT_PATH, FONT_TITLE_SIZE)
            result = game_over_screen(screen, clock, font)
            if result == 'menu':
                main()  # Перезапуск главного меню
            return

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
