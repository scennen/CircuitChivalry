import pygame
import sys
import os
from utils.constants import (
    WIDTH, HEIGHT, FPS, FONT_SIZE_TITLE, FONT_SIZE_TEXT, FONT_SIZE_BUTTON,
    FONT_PATH
)
from utils.music_manager import MusicManager
from scenes.menu import main_menu
from scenes.battle import battle_scene
from scenes.grid import grid_scene


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Circuit Chivalry: The Grid")
    clock = pygame.time.Clock()

    # Инициализация менеджера музыки
    music_manager = MusicManager()

    # Загрузка шрифтов
    font_path = os.path.join(os.path.dirname(os.path.dirname(
        __file__)), "assets", "fonts", "alagard-12px-unicode.ttf")
    font_title = pygame.font.Font(font_path, FONT_SIZE_TITLE)
    font_text = pygame.font.Font(font_path, FONT_SIZE_TEXT)
    font_button = pygame.font.Font(font_path, FONT_SIZE_BUTTON)

    # Игровой цикл
    running = True
    current_scene = None

    while running:
        if current_scene is None:
            # Воспроизводим музыку главного меню
            music_manager.play("main_menu")
            if not main_menu(screen, font_title, font_button, clock):
                running = False
            else:
                current_scene = 0
        elif current_scene == 0:
            music_manager.play("battle")  # Воспроизводим музыку боевой сцены
            next_scene = battle_scene(screen, font_text, font_button, clock)
            if next_scene is False:
                running = False
            else:
                current_scene = next_scene
        elif current_scene == 1:
            # Воспроизводим музыку первого сектора
            music_manager.play("sector1")
            next_scene = grid_scene(screen, font_text, font_button, clock)
            if next_scene is False:
                running = False
            else:
                current_scene = next_scene
        elif current_scene == 2:
            # Воспроизводим музыку второго сектора
            music_manager.play("sector2")
            next_scene = grid_scene(screen, font_text, font_button, clock)
            if next_scene is False:
                running = False
            else:
                current_scene = next_scene
        elif current_scene == 3:
            # Воспроизводим музыку третьего сектора
            music_manager.play("sector3")
            next_scene = grid_scene(screen, font_text, font_button, clock)
            if next_scene is False:
                running = False
            else:
                current_scene = next_scene
        elif current_scene == 4:
            music_manager.play("boss")  # Воспроизводим музыку босса
            next_scene = grid_scene(screen, font_text, font_button, clock)
            if next_scene is False:
                running = False
            else:
                current_scene = next_scene
        else:
            running = False

    music_manager.stop()  # Останавливаем музыку при выходе
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
