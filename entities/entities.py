import pygame
from entities.base_fighter import BaseFighter
from entities.knight import Enemy, EnemyNeon, PlayerNeon
import os
from typing import Any, Optional, List
import random
from core.constants import FONT_PATH

ENEMY_SPRITE_FRAMES = {
    "IDLE": 8,
    "RUN": 8,
    "WALK": 8,
    "ATTACK 1": 6,
    "ATTACK 2": 6,
    "HURT": 4,
    "DEATH": 6,
}


class Enemy(BaseFighter):
    def __init__(self, x: int, y: int, hp: int = 100, speed: int = 2, sprite_type: str = "enemy"):
        super().__init__(x, y, sprite_type, ENEMY_SPRITE_FRAMES, hp)
        self.speed = speed  # Скорость врага
        # Здесь можно добавить логику AI, атаки и т.д.


class ShadowCopy(EnemyNeon):
    def __init__(self, x: int, y: int, player_hp: int):
        super().__init__(x, y, hp=player_hp, speed=3)
        self.sprite_type = "shadow"  # Используем спрайты тени
        self.load_sprites()  # Перезагружаем спрайты


class Drone(Enemy):
    def __init__(self, x: int, y: int, speed: int = 4):
        super().__init__(x, y, hp=1, speed=speed)
        self.image.fill((0, 255, 255))  # Неоновый цвет

    def update(self) -> None:
        self.rect.x += self.speed  # Дрон летает по горизонтали
        if self.rect.right > 800 or self.rect.left < 0:
            self.speed = -self.speed  # Меняет направление


class CoreGuardian(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        sprite_path = os.path.join(
            "assets", "images", "sprites", "core_guardian", "core_guardian.png")
        size = 240
        if os.path.exists(sprite_path):
            self.image = pygame.image.load(sprite_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (size, size))
        else:
            self.image = pygame.Surface((size, size))
            self.image.fill((50, 50, 255))  # Синий квадрат если нет картинки
        self.rect = self.image.get_rect(center=(x, y))
        # Параметры для боевой системы
        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.bottom
        self.hitbox = pygame.Rect(0, 0, size-40, size-80)
        self._update_hitbox()
        self.hp = 100
        self.max_hp = 100
        self.is_dead = False
        self.state = "IDLE"
        self.frame_idx = 0
        self.core_open = False
        self.core_timer = 0
        self.arms = [BossArm(x-80, y, "sword"), BossArm(x+80, y, "shield"),
                     BossArm(x-80, y+80, "axe"), BossArm(x+80, y+80, "gun")]
        self.vel_x = 3
        self.direction = 1  # 1 — вправо, -1 — влево
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_range = 180
        self.heal_timer = 0  # Таймер для восстановления здоровья
        self.vel_y = 0
        self.gravity = 0.8
        self.on_ground = False
        self.jump_power = 18
        self.jump_cooldown = 0

    def _update_hitbox(self) -> None:
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def take_damage(self, amount: int) -> None:
        self.hp -= amount  # Уменьшаем HP
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            self.state = "DEATH"
        else:
            self.state = "HURT"

    def update(self, platforms: Optional[List[Any]] = None, player: Optional[Any] = None) -> None:
        if self.is_dead:
            return  # Если мертв, ничего не делаем
        # Восстановление здоровья раз в 60 update (примерно 1 секунда)
        if self.hp < self.max_hp:
            self.heal_timer += 1
            if self.heal_timer >= 60:
                self.hp = min(self.max_hp, self.hp + 3)
                self.heal_timer = 0
        else:
            self.heal_timer = 0
        # Рандомные прыжки
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if not self.is_attacking and self.on_ground and self.jump_cooldown == 0:
            if random.random() < 1/60:  # Шанс прыжка примерно раз в секунду
                self.vel_y = -self.jump_power * 1.2  # Прыгает выше обычного
                self.on_ground = False
                self.jump_cooldown = 45  # Кулдаун между прыжками
        # Гравитация и приземление
        floor_y = None
        if platforms is not None:
            self.vel_y += self.gravity
            if self.vel_y > 10:
                self.vel_y = 10
            self.pos_y += self.vel_y
            self.rect.bottom = int(self.pos_y)
            self._update_hitbox()
            self.on_ground = False
            for platform in platforms:
                if hasattr(platform, 'rect') and self.hitbox.colliderect(platform.rect):
                    if self.vel_y > 0 and self.hitbox.bottom - self.vel_y <= platform.rect.top:
                        self.hitbox.bottom = platform.rect.top
                        self.pos_y = self.hitbox.bottom
                        self.vel_y = 0
                        self.on_ground = True
                        floor_y = platform.rect.top
            self.rect.bottom = self.hitbox.bottom
        # Ограничение по полу
        if floor_y is None and platforms is not None and len(platforms) > 0:
            floor_y = max(
                getattr(p, 'rect', p).bottom for p in platforms if hasattr(p, 'rect'))
        if floor_y is not None and self.rect.bottom > floor_y:
            self.rect.bottom = floor_y
            self.pos_y = self.rect.bottom
            self.vel_y = 0
            self.on_ground = True
        # Движение босса: ходит влево-вправо по экрану
        if not self.is_attacking:
            self.pos_x += self.vel_x * self.direction
            if self.pos_x < 200:
                self.pos_x = 200
                self.direction = 1
            elif self.pos_x > 1080:
                self.pos_x = 1080
                self.direction = -1
            self.rect.centerx = int(self.pos_x)
            self._update_hitbox()
        # Атака, если игрок рядом
        if player and not self.is_attacking and not self.is_dead:
            dx = player.rect.centerx - self.rect.centerx
            if abs(dx) < self.attack_range and self.attack_cooldown == 0:
                self.is_attacking = True
                self.attack_cooldown = 90
                self.state = "ATTACK"
        if self.is_attacking:
            self.attack_cooldown -= 1
            if self.attack_cooldown < 60 and self.attack_cooldown > 50:
                if player and hasattr(player, 'hitbox') and self.hitbox.colliderect(player.hitbox):
                    if hasattr(player, 'take_damage'):
                        player.take_damage(30)  # Наносим урон игроку
            if self.attack_cooldown <= 0:
                self.is_attacking = False
                self.state = "IDLE"

    def draw(self, surface: pygame.Surface, debug: bool = False) -> None:
        surface.blit(self.image, self.rect)
        # Полоска HP сверху экрана
        bar_width = 400
        bar_height = 18
        hp_ratio = max(0, min(1, self.hp / self.max_hp))
        bar_x = (surface.get_width() - bar_width) // 2
        bar_y = 30
        pygame.draw.rect(surface, (70, 70, 70),
                         (bar_x, bar_y, bar_width, bar_height))
        if hp_ratio > 0:
            fill_width = int(bar_width * hp_ratio)
            color = (200, 30, 30) if self.hp < self.max_hp * \
                0.5 else (255, 140, 0)
            pygame.draw.rect(surface, color,
                             (bar_x, bar_y, fill_width, bar_height))
        # Надпись с именем босса под полоской HP
        font = pygame.font.Font(FONT_PATH, 36)
        name_text = font.render("Core Guardian", True, (255, 255, 255))
        name_rect = name_text.get_rect(
            center=(surface.get_width() // 2, bar_y + bar_height + 18))
        surface.blit(name_text, name_rect)
        if debug:
            # Зеленый прямоугольник для отладки
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)


class BossArm(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, weapon_type: str, hp: int = 5):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill((200, 200, 200))  # Серый цвет для руки
        self.rect = self.image.get_rect(center=(x, y))
        self.weapon_type = weapon_type  # Тип оружия
        self.destroyed = False
        self.hp = hp

    def update(self):
        pass  # Здесь можно добавить анимацию или атаку


class Ally(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, hp: int = 3):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # Зеленый союзник
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp

    def update(self):
        pass  # Логика союзника (например, движение за игроком)


# Переопределяем цвет полоски HP для неоновых врагов и игрока
old_enemy_draw = EnemyNeon.draw
old_player_draw = PlayerNeon.draw


def neon_enemy_draw(self, surface, debug=False, is_enemy=True):
    super(EnemyNeon, self).draw(surface, debug=debug, is_enemy=is_enemy)
    # Оранжевая полоска HP
    bar_width = 40
    bar_height = 6
    hp_ratio = max(0, min(1, self.hp / self.max_hp))
    bar_x = self.rect.centerx - bar_width // 2
    bar_y = self.rect.top - bar_height - 4
    pygame.draw.rect(surface, (70, 70, 70),
                     (bar_x, bar_y, bar_width, bar_height))
    if hp_ratio > 0:
        fill_width = int(bar_width * hp_ratio)
        pygame.draw.rect(surface, (255, 140, 0),
                         (bar_x, bar_y, fill_width, bar_height))


EnemyNeon.draw = neon_enemy_draw


def neon_player_draw(self, surface, debug=False, is_enemy=False):
    super(PlayerNeon, self).draw(surface, debug=debug, is_enemy=is_enemy)
    # Голубая полоска HP
    bar_width = 40
    bar_height = 6
    hp_ratio = max(0, min(1, self.hp / self.max_hp))
    bar_x = self.rect.centerx - bar_width // 2
    bar_y = self.rect.top - bar_height - 4
    pygame.draw.rect(surface, (70, 70, 70),
                     (bar_x, bar_y, bar_width, bar_height))
    if hp_ratio > 0:
        fill_width = int(bar_width * hp_ratio)
        pygame.draw.rect(surface, (0, 255, 255),
                         (bar_x, bar_y, fill_width, bar_height))
    if debug:
        pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)


PlayerNeon.draw = neon_player_draw
