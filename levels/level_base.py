import pygame
from typing import List, Tuple
import os
import random


class BaseLevel:
    def __init__(
        self,
        background_path: str,
        enemy_count: int = 5,
        enemy_type: str = 'medieval',
        level_name: str = "Уровень",
        caption_color: Tuple[int, int, int] = (255, 255, 255),
        caption_font_path: str = "assets/fonts/alagard-12px-unicode.otf",
        caption_font_size: int = 32,
        caption_pos: Tuple[int, int] = (20, 20),
        floor_offset_from_bottom: int = 100,
        floor_alpha: int = 0,
        floor_color: Tuple[int, int, int] = (100, 100, 100),
        screen_size: Tuple[int, int] = (1280, 720),
    ):
        self.background_path = background_path  # Путь к фону
        self.enemy_count = enemy_count  # Количество врагов
        self.enemy_type = enemy_type  # Тип врагов
        self.level_name = level_name  # Название уровня
        self.caption_color = caption_color  # Цвет надписи
        self.caption_font_path = caption_font_path  # Путь к шрифту
        self.caption_font_size = caption_font_size  # Размер шрифта
        self.caption_pos = caption_pos  # Позиция надписи
        self.floor_offset_from_bottom = floor_offset_from_bottom  # Высота пола от низа
        self.floor_alpha = floor_alpha  # Прозрачность пола
        self.floor_color = floor_color  # Цвет пола
        self.screen_size = screen_size  # Размеры экрана
        self._enemy_spawn_positions: List[int] = self._random_enemy_positions(
            enemy_count)
        self.enemies = self.create_enemies(
            enemy_count, self._enemy_spawn_positions)
        # Сохраняем стартовые параметры только для обычных врагов, не для боссов
        if self.enemies and not hasattr(self.enemies[0], 'core_open'):
            self._enemy_start_params: List[Tuple[int, int, int, int]] = [
                (e.pos_x, e.pos_y, e.hp, e.max_hp) for e in self.enemies]
        else:
            self._enemy_start_params: List[Tuple[int, int, int, int]] = []
        self.background = pygame.image.load(
            self.background_path).convert()  # Загружаем фон
        self.background = pygame.transform.scale(
            self.background,
            self.screen_size
        )
        self.caption_font = self.load_font(
            self.caption_font_path,
            self.caption_font_size
        )
        self.platforms = self.create_platforms()  # Платформы уровня
        self.hearts = self.create_hearts()  # Сердечки на уровне
        self.blue_orb = self.create_blue_orb()  # Голубая сфера
        self.kills = 0  # Счетчик убитых врагов
        self.extra_blue_orbs = []  # Дополнительные сферы

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

    def _random_enemy_positions(self, count: int):
        min_x = 120
        max_x = self.screen_size[0] - 120
        positions = []
        for _ in range(count):
            for _ in range(100):
                x = random.randint(min_x, max_x)
                if all(abs(x - px) > 80 for px in positions):
                    positions.append(x)
                    break
            else:
                # Если не нашли уникальное место
                positions.append(random.randint(min_x, max_x))
        return positions

    def create_enemies(self, count: int, positions: List[int]) -> List[pygame.sprite.Sprite]:
        from entities.knight import Enemy, EnemyNeon
        from entities.entities import CoreGuardian, ShadowCopy
        enemy_type = getattr(self, 'enemy_type', 'medieval')
        enemies = []
        if enemy_type == 'boss':
            boss = CoreGuardian(self.screen_size[0] // 2, self.floor_y - 100)
            enemies.append(boss)
            return enemies
        enemy_class = {
            'medieval': Enemy,
            'neon': EnemyNeon,
            'shadow': ShadowCopy
        }.get(enemy_type, Enemy)
        for x in positions:
            if enemy_type == 'shadow':
                enemy = ShadowCopy(x, self.floor_y, player_hp=100)
            else:
                enemy = enemy_class(x, self.floor_y)
            enemies.append(enemy)
        return enemies

    def create_platforms(self):
        return []  # Удаляем все платформы, кроме пола (пол рисуется отдельно)

    def create_hearts(self):
        return []  # Сердечки по умолчанию отсутствуют

    def create_blue_orb(self):
        from entities.platform import BlueOrb
        x = self.screen_size[0] - 80  # Появляется справа
        y = self.floor_y - 20  # На полу
        return BlueOrb(x, y)

    def draw_background(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))  # Рисуем фон

    def draw_floor(self, screen: pygame.Surface):
        floor_surface = pygame.Surface(
            (self.screen_size[0], self.floor_offset_from_bottom),
            pygame.SRCALPHA
        )
        floor_surface.fill((*self.floor_color, self.floor_alpha))
        y = self.screen_size[1] - self.floor_offset_from_bottom
        screen.blit(floor_surface, (0, y))  # Рисуем пол

    def draw_caption(self, screen: pygame.Surface):
        caption_text = f"Уровень {self.level_name}"
        caption_surface = self.caption_font.render(
            caption_text, True, self.caption_color)
        screen.blit(caption_surface, self.caption_pos)  # Рисуем надпись

    def draw_enemies(self, screen: pygame.Surface):
        for enemy in self.enemies:
            enemy.draw(screen)  # Рисуем каждого врага

    def update_enemies(self, platforms, player):
        for enemy in self.enemies[:]:  # Копируем список для безопасного удаления
            if hasattr(enemy, 'update'):
                try:
                    enemy.update(platforms=platforms, player=player)
                except TypeError:
                    try:
                        enemy.update(platforms=platforms)
                    except TypeError:
                        try:
                            enemy.update()
                        except Exception:
                            pass

            # Удаляем врага если он мертв и анимация смерти закончена
            if hasattr(enemy, 'is_dead') and enemy.is_dead:
                if hasattr(enemy, 'animation_frame'):
                    if enemy.animation_frame >= len(enemy.animations.get('DEATH', [])) - 1:
                        self.enemies.remove(enemy)
                        self.kills += 1
                        if self.kills == 2:
                            from entities.platform import BlueOrb
                            orb = BlueOrb(
                                self.screen_size[0] // 2, self.floor_y - 20)
                            self.extra_blue_orbs.append(orb)
                else:
                    self.enemies.remove(enemy)
                    self.kills += 1
                    if self.kills == 2:
                        from entities.platform import BlueOrb
                        orb = BlueOrb(
                            self.screen_size[0] // 2, self.floor_y - 20)
                        self.extra_blue_orbs.append(orb)

        return len(self.enemies) == 0  # True если все враги побеждены

    def draw(self, screen: pygame.Surface):
        self.draw_background(screen)
        self.draw_floor(screen)
        self.draw_caption(screen)
        for p in getattr(self, 'platforms', []):
            screen.blit(p.image, p.rect)  # Рисуем платформы
        for h in getattr(self, 'hearts', []):
            screen.blit(h.image, h.rect)  # Рисуем сердечки
        if hasattr(self, 'blue_orb') and self.blue_orb:
            # Рисуем голубую сферу
            screen.blit(self.blue_orb.image, self.blue_orb.rect)
        for orb in getattr(self, 'extra_blue_orbs', []):
            screen.blit(orb.image, orb.rect)  # Рисуем дополнительные сферы
        self.draw_enemies(screen)

    @property
    def floor_y(self):
        # Y-координата пола
        return self.screen_size[1] - self.floor_offset_from_bottom

    def reset_enemies(self):
        pass
