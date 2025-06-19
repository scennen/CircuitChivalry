import pygame
from typing import Tuple
import os
import math

# Класс для экрана перехода между уровнями


class TransitionScreen:
    def __init__(
        self,
        title: str = "",
        description: str = "",
        title_color: Tuple[int, int, int] = (255, 255, 255),
        desc_color: Tuple[int, int, int] = (200, 200, 200),
        bg_color: Tuple[int, int, int] = (0, 0, 0),
        title_font_path: str = "assets/fonts/alagard-12px-unicode.otf",
        desc_font_path: str = "assets/fonts/alagard-12px-unicode.otf",
        title_font_size: int = 48,
        desc_font_size: int = 28,
        title_pos: Tuple[int, int] = (60, 60),
        desc_pos: Tuple[int, int] = (60, 140),
        screen_size: Tuple[int, int] = (1280, 720),
    ):
        self.title = title  # Заголовок экрана
        self.description = description  # Описание экрана
        self.title_color = title_color  # Цвет заголовка
        self.desc_color = desc_color  # Цвет описания
        self.bg_color = bg_color  # Цвет фона
        self.title_font_path = title_font_path  # Путь к шрифту заголовка
        self.desc_font_path = desc_font_path  # Путь к шрифту описания
        self.title_font_size = title_font_size  # Размер шрифта заголовка
        self.desc_font_size = desc_font_size  # Размер шрифта описания
        self.title_pos = title_pos  # Позиция заголовка
        self.desc_pos = desc_pos  # Позиция описания
        self.screen_size = screen_size  # Размер экрана
        self.title_font = self.load_font(
            self.title_font_path, self.title_font_size)
        self.desc_font = self.load_font(
            self.desc_font_path, self.desc_font_size)
        self.anim_time = 0.0
        self._last_tick = pygame.time.get_ticks()

    def load_font(self, path: str, size: int):
        try:
            if os.path.exists(path):
                return pygame.font.Font(path, size)
            else:
                print(
                    f"[WARNING] Font file not found: {path}. Using default font.")
                return pygame.font.SysFont(None, size)
        except Exception as e:
            print(
                f"[WARNING] Could not load font '{path}': {e}. Using default font.")
            return pygame.font.SysFont(None, size)

    def draw(self, screen: pygame.Surface):
        # Обновляем анимационное время
        now = pygame.time.get_ticks()
        dt = (now - self._last_tick) / 1000.0
        self.anim_time += dt
        self._last_tick = now
        screen.fill(self.bg_color)  # Заливаем фон
        rendered_lines: list[tuple[pygame.Surface, int]] = []
        total_height = 0
        # Render title if present
        if self.title:
            # Анимация: покачивание по Y (синусоида)
            wave_offset = int(math.sin(self.anim_time * 2.0) * 8)
            title_surface = self.title_font.render(
                self.title, True, self.title_color
            )
            rendered_lines.append((title_surface, wave_offset))
            total_height += title_surface.get_height()
        # Render description lines if present
        # пульсация прозрачности
        desc_alpha = int(180 + 60 * math.sin(self.anim_time * 1.5))
        if self.description:
            desc_lines = self.description.split('\n')
            for line in desc_lines:
                desc_surface = self.desc_font.render(
                    line, True, self.desc_color
                ).convert_alpha()
                # Применяем альфа-канал
                desc_surface.set_alpha(desc_alpha)
                rendered_lines.append((desc_surface, 0))
                total_height += desc_surface.get_height()
        # Calculate starting y to center the block
        screen_w, screen_h = self.screen_size
        y = (screen_h - total_height) // 2
        for surf, offset in rendered_lines:
            rect = surf.get_rect(centerx=screen_w // 2, y=y + offset)
            screen.blit(surf, rect)
            y += surf.get_height()

    def handle_event(self, event):
        # Здесь можно обработать события, например, нажатие клавиш
        pass
