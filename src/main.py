import pygame
from entities.player import Player
from levels import create_level
from core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LEVELS, WHITE, BLACK, BUTTON_COLOR, BUTTON_NEON_GLOW,
    FONT_PATH, FONT_TITLE_SIZE, FONT_BUTTON_SIZE, FONT_TEXT_SIZE, MENU_BG_IMAGE, GAME_TITLE
)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def draw_text(surface, text, font, color, pos):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=pos)
    surface.blit(text_obj, rect)
    return rect


def load_font(path, size):
    try:
        font = pygame.font.Font(path, size)
        font.render("test", True, (0, 0, 0))
        return font
    except Exception as e:
        print(
            f"[WARNING] Не удалось загрузить кастомный шрифт: {e}. Используется стандартный.")
        return pygame.font.SysFont(None, size)


def main_menu(screen, clock, can_continue=False, pause_mode=False):
    bg = pygame.image.load(MENU_BG_IMAGE).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    font = load_font(FONT_PATH, FONT_TITLE_SIZE)
    btn_font = load_font(FONT_PATH, FONT_BUTTON_SIZE)
    title_pos = (SCREEN_WIDTH // 2, 180)
    buttons = []
    if can_continue and not pause_mode:
        continue_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, 260, 400, 48)
        buttons.append(('Продолжить игру', continue_btn))
        start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 48)
        buttons.append(('Начать игру', start_btn))
        exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, 380, 400, 48)
        buttons.append(('Выход', exit_btn))
    else:
        start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, 340, 400, 48)
        buttons.append(('Начать игру', start_btn))
        exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, 400, 400, 48)
        buttons.append(('Выход', exit_btn))
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
                    if can_continue and not pause_mode and selected == 0:
                        return 'continue'
                    if (can_continue and not pause_mode and selected == 1) or (not can_continue or pause_mode) and selected == 0:
                        return 'start'
                    else:
                        pygame.quit()
                        sys.exit()
                if pause_mode and event.key == pygame.K_ESCAPE:
                    return 'resume'
        screen.blit(bg, (0, 0))
        draw_text(screen, GAME_TITLE, font, WHITE, title_pos)
        for i, (text, btn) in enumerate(buttons):
            hover = btn.collidepoint(mouse)
            draw_text(
                screen,
                text,
                btn_font,
                BUTTON_NEON_GLOW if selected == i or hover else WHITE,
                btn.center
            )
        pygame.display.flip()
        clock.tick(FPS)
        for i, (_, btn) in enumerate(buttons):
            if btn.collidepoint(mouse) and click:
                if can_continue and not pause_mode and i == 0:
                    return 'continue'
                if (can_continue and not pause_mode and i == 1) or (not can_continue or pause_mode) and i == 0:
                    return 'start'
                else:
                    pygame.quit()
                    sys.exit()


def game_over_screen(screen, clock, font):
    bg_path = os.path.join(os.path.dirname(__file__), '..',
                           'assets', 'images', 'backgrounds', 'game_over.png')
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    title_font = load_font(FONT_PATH, FONT_TITLE_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return  # Вернуться в меню
        screen.blit(bg, (0, 0))
        draw_text(screen, 'Вы погибли!', title_font, BUTTON_NEON_GLOW,
                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        draw_text(screen, 'Нажмите Enter или Esc', font, (255, 255, 255),
                  # Было +60, стало +120
                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    saved_state = None

    while True:
        menu_action = main_menu(
            screen, clock, can_continue=saved_state is not None)

        if menu_action == 'start':
            level_num = 1
            player = Player(100, 400)
            current_level = create_level(level_num)
            current_level.set_player(player)
            current_level.start()  # Важно! Здесь создаются враги
        elif menu_action == 'continue' and saved_state:
            level_num, current_level, player = saved_state
        else:
            continue

        font = load_font(FONT_PATH, FONT_TEXT_SIZE)
        in_game = True

        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Пауза: вызываем меню с pause_mode=True
                    menu_action = main_menu(
                        screen, clock, can_continue=saved_state is not None, pause_mode=True)
                    if menu_action == 'resume':
                        continue  # Просто продолжаем игру
                    elif menu_action == 'start':
                        in_game = False
                        break
                    elif menu_action == 'continue' and saved_state:
                        level_num, current_level, player = saved_state
                        continue
                    else:
                        pygame.quit()
                        sys.exit()
            # Обновление
            player.update(current_level.platforms)  # Передаем платформы уровня
            current_level.update()  # Обновление врагов и их взаимодействий

            # Проверка смерти игрока
            if player.hp <= 0:
                saved_state = None  # После смерти нельзя продолжить
                game_over_screen(screen, clock, font)
                in_game = False
                break

            # Проверка перехода на следующий уровень
            if player.rect.x > SCREEN_WIDTH:
                level_num += 1
                if level_num > LEVELS:
                    print('You win!')
                    pygame.quit()
                    sys.exit()
                player.rect.topleft = (0, 400)
                current_level = create_level(level_num)
                current_level.set_player(player)
                current_level.start()  # Не забываем создать врагов на новом уровне

            # Отрисовка
            screen.fill(WHITE)
            current_level.draw(screen)  # Отрисовка уровня (платформы и враги)
            player.draw(screen)  # Отрисовка игрока поверх всего
            level_text = font.render(f'Level: {level_num}', True, BLACK)
            screen.blit(level_text, (10, 10))
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    main()
