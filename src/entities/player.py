import pygame
import os
import random
from typing import Dict, List, Tuple


class Player(pygame.sprite.Sprite):
    # Количество кадров в каждом спрайт-листе (укажите реальные значения для каждого PNG)
    SPRITE_FRAMES = {
        "IDLE": 7,
        "RUN": 8,
        "WALK": 8,
        "JUMP": 5,
        "ATTACK1": 6,
        "ATTACK2": 5,
        "ATTACK3": 6,
        "DEFEND": 6,
        "HURT": 4,
        "DEATH": 12,
    }
    SCALE = 3  # Увеличить масштаб до 3x
    HITBOX_WIDTH = 32  # ширина хитбокса (подберите под спрайт)
    HITBOX_HEIGHT = 48  # высота хитбокса (подберите под спрайт)
    # Длительность каждого кадра атаки
    ATTACK_FRAME_DURATION = 6

    def __init__(self, x: int, y: int, hp: int = 100):
        super().__init__()
        self.hp = hp  # Инициализируем здоровье сразу
        self.max_hp = hp  # Максимальное здоровье
        # Используем float для более точного позиционирования
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.current_attack = "ATTACK1"  # Текущая атака
        self.attack_timer = 0  # Таймер для смены кадров атаки
        # Путь к assets относительно корня проекта
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))  # type: ignore
        sprite_dir = os.path.join(
            base_dir, "assets", "images", "sprites", "knight")

        self.frames = {}
        self.frame_offsets = {}  # смещения для центрирования
        for state, num_frames in self.SPRITE_FRAMES.items():
            sheet_path = os.path.join(
                sprite_dir, f"{state.replace('ATTACK', 'ATTACK ')}.png")
            if not os.path.exists(sheet_path):
                continue
            sheet = pygame.image.load(sheet_path).convert_alpha()
            frame_width = sheet.get_width() // num_frames
            frame_height = sheet.get_height()
            raw_frames = []
            for i in range(num_frames):
                frame = sheet.subsurface(pygame.Rect(
                    i * frame_width, 0, frame_width, frame_height))
                # --- CROP по альфа-каналу ---
                bbox = frame.get_bounding_rect(min_alpha=1)
                cropped = frame.subsurface(bbox)
                raw_frames.append(cropped)
            # --- Приведение к одному размеру (по максимальному bbox) ---
            max_w = max(f.get_width() for f in raw_frames)
            max_h = max(f.get_height() for f in raw_frames)
            state_frames = []
            state_offsets = []
            for f in raw_frames:
                surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
                # Центрируем по туловищу (по горизонтали — по центру, по вертикали — по низу)
                offset_x = (max_w - f.get_width()) // 2
                offset_y = max_h - f.get_height()
                surf.blit(f, (offset_x, offset_y))
                # Масштабируем
                scaled = pygame.transform.scale(
                    surf, (max_w * self.SCALE, max_h * self.SCALE))
                state_frames.append(scaled)
                state_offsets.append(
                    (offset_x * self.SCALE, offset_y * self.SCALE))
            self.frames[state] = state_frames
            self.frame_offsets[state] = state_offsets
        self.state = "IDLE"
        self.frame_idx = 0
        self.image = self.frames[self.state][self.frame_idx]
        self.rect = self.image.get_rect()
        self.rect.centerx = round(self.pos_x)
        self.rect.bottom = round(self.pos_y)

        # Компактный хитбокс (центрируется по туловищу)
        self.hitbox = pygame.Rect(0, 0, self.HITBOX_WIDTH, self.HITBOX_HEIGHT)
        self._update_hitbox()

        # Физика и состояния
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True

        # Боевые параметры
        self.is_attacking = False
        self.is_defending = False
        self.attack_cooldown = 0
        self.defend_cooldown = 0
        self.attack_frame = 0

        # Параметры анимации
        self.anim_timer = 0
        self.anim_speed = 0.05  # Меньше значение - быстрее анимация
        self.anim_time = 0.5  # Для плавной анимации

    def _update_hitbox(self):
        # Центрируем хитбокс по центру rect
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def update(self, platforms: pygame.sprite.Group) -> None:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        prev_state = self.state

        # Обработка анимации атаки
        if self.is_attacking:
            # Анимация атаки
            if self.attack_timer > 0:
                self.attack_timer -= 1
            else:
                self.frame_idx += 1
                if self.frame_idx >= len(self.frames[self.current_attack]):
                    # Закончили атаку
                    self.is_attacking = False
                    self.state = "IDLE"
                    self.frame_idx = 0
                else:
                    # Следующий кадр атаки
                    self.attack_timer = self.ATTACK_FRAME_DURATION
            return  # Во время атаки блокируем другие действия

        # Обработка движения
        self.vel_x = 0
        if not self.is_defending:  # Движение возможно, если не защищаемся
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vel_x = -self.speed
                self.facing_right = False
                if self.on_ground:
                    self.state = "RUN"
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vel_x = self.speed
                self.facing_right = True
                if self.on_ground:
                    self.state = "RUN"
            elif self.on_ground:
                self.state = "IDLE"            # Прыжок
            if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
                self.vel_y = -self.jump_power
                self.on_ground = False
                self.state = "JUMP"

        # Применяем гравитацию
        self.vel_y += self.gravity
        if self.vel_y > 10:  # Ограничение максимальной скорости падения
            self.vel_y = 10

        # Обновляем позицию
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.midbottom = (round(self.pos_x), round(self.pos_y))
        self._update_hitbox()

        # Обработка коллизий
        self.on_ground = False
        for platform in platforms:
            if self.hitbox.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.hitbox.bottom = platform.rect.top
                    self.pos_y = self.hitbox.bottom
                    self.vel_y = 0
                    self.on_ground = True
        self.rect.midbottom = self.hitbox.midbottom

        # Обработка атаки и защиты
        if mouse[0] and not self.is_attacking and not self.is_defending and self.attack_cooldown == 0:
            self.attack()
        elif mouse[2] and not self.is_attacking and self.defend_cooldown == 0:
            self.defend()

        # Обновление кулдаунов
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.defend_cooldown > 0:
            self.defend_cooldown -= 1
            self.state = "DEFEND"
        elif self.defend_cooldown == 0:
            self.is_defending = False

        # Анимация для состояний кроме атаки
        if not self.is_attacking:
            self.anim_time += self.anim_speed
            if self.anim_time >= 1:
                self.anim_time = 0
                self.frame_idx = (
                    self.frame_idx + 1) % len(self.frames[self.state])

        # Обновляем спрайт
        if self.state != prev_state:
            self.frame_idx = 0
            self.anim_time = 0

        # Обновляем изображение
        old_midbottom = self.rect.midbottom
        self.image = self.frames[self.state if not self.is_attacking else self.current_attack][self.frame_idx]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom
        self._update_hitbox()

    def attack(self):
        if not self.is_attacking and not self.is_defending:
            self.is_attacking = True
            self.attack_cooldown = 45  # Увеличенный кулдаун для полной анимации
            self.attack_frame = 0
            self.frame_idx = 0
            self.anim_time = 0

            # Случайный выбор типа атаки (1, 2 или 3)
            self.current_attack = f"ATTACK{random.randint(1, 3)}"
            self.state = self.current_attack
            self.attack_timer = self.ATTACK_FRAME_DURATION  # Сбрасываем таймер

    def defend(self):
        if not self.is_attacking:
            self.is_defending = True
            self.defend_cooldown = 30
            self.frame_idx = 0
            self.anim_time = 0
            self.state = "DEFEND"

    def draw(self, surface, debug=False):
        # Отрисовка спрайта
        surface.blit(self.image, self.rect)

        # Полоска здоровья
        bar_width = 40
        bar_height = 6
        hp_ratio = max(0, min(1, self.hp / self.max_hp))
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - bar_height - 4

        # Серый фон полоски
        pygame.draw.rect(surface, (70, 70, 70),
                         (bar_x, bar_y, bar_width, bar_height))
        # Синяя заполненная часть (#006E9E)
        if hp_ratio > 0:
            fill_width = int(bar_width * hp_ratio)
            pygame.draw.rect(surface, (0, 110, 158),  # #006E9E в RGB
                             (bar_x, bar_y, fill_width, bar_height))

        # Визуализация хитбокса для отладки
        if debug:
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)
