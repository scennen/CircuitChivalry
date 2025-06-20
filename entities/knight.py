from entities.base_fighter import BaseFighter
import pygame
from typing import Any, Optional
import random

PLAYER_SPRITE_FRAMES = {
    "IDLE": 7,
    "RUN": 8,
    "WALK": 8,
    "JUMP": 5,
    "ATTACK1": 6,
    "ATTACK2": 5,
    "DEFEND": 6,
    "HURT": 4,
    "DEATH": 12,
}
ENEMY_SPRITE_FRAMES = {
    "IDLE": 8,
    "RUN": 8,
    "WALK": 8,
    "ATTACK 1": 6,
    "ATTACK 2": 6,
    "HURT": 4,
    "DEATH": 6,
}


class Player(BaseFighter):
    def __init__(self, x: int, y: int, hp: int = 100, sprite_type: str = "knight"):
        # Sprite_type задаёт папку спрайтов
        super().__init__(x, y, sprite_type, PLAYER_SPRITE_FRAMES, hp)
        self.vel_x = 0  # Горизонтальная скорость
        self.vel_y = 0  # Вертикальная скорость
        self.speed = 5  # Скорость передвижения
        self.jump_power = 15  # Сила прыжка
        self.gravity = 0.8  # Гравитация
        self.on_ground = False  # Находится ли на земле
        self.facing_right = True  # Смотрит вправо
        self.is_attacking = False  # Атакует ли сейчас
        self.is_defending = False  # Защищается ли сейчас
        self.attack_cooldown = 0  # Кулдаун атаки
        self.defend_cooldown = 0  # Кулдаун защиты
        self.attack_frame = 0  # Кадр атаки
        self.anim_timer = 0  # Таймер анимации
        self.anim_speed = 0.22  # Скорость анимации
        self.attack_anim_speed = 0.28  # Скорость анимации атаки
        self.anim_time = 0.5  # Время анимации
        self.current_attack = "ATTACK1"  # Текущая атака
        self.attack_timer = 6  # Таймер атаки
        self.max_jump_count = 2  # Максимум прыжков подряд
        self.jump_count = 0  # Сколько прыжков сделано
        self.damage_dealt_this_attack = False  # Был ли нанесён урон в этой атаке
        self.jump_pressed = False  # Нажата ли кнопка прыжка
        self.jump_was_pressed = False  # Была ли нажата кнопка прыжка
        self.jump_time = 0  # Время прыжка
        self.max_jump_time = 14  # Максимальное время прыжка
        self.jump_buffer = 0  # Буфер прыжка
        self.jump_buffer_max = 8  # 8 кадров
        self.coyote_time = 0
        self.coyote_time_max = 8  # 8 кадров

    def handle_input(self, keys: Any, mouse_buttons: Optional[Any] = None) -> None:
        self.vel_x = 0
        if not self.is_defending:
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
                self.state = "IDLE"
            # Прыжок с буферизацией
            jump_now = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]
            if jump_now and not self.jump_was_pressed:
                self.jump_buffer = self.jump_buffer_max
            self.jump_pressed = jump_now
            self.jump_was_pressed = jump_now
        # Атака и защита
        attack_pressed = False
        if mouse_buttons and mouse_buttons[0]:
            attack_pressed = True
        if keys[pygame.K_PERIOD]:
            attack_pressed = True
        if keys[pygame.K_SLASH]:
            attack_pressed = True
        if attack_pressed and not self.is_attacking and not self.is_defending and self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 45
            self.attack_frame = 0
            self.frame_idx = 0
            self.anim_time = 0
            self.current_attack = random.choice(["ATTACK1", "ATTACK2"])
            self.state = self.current_attack
            self.attack_timer = 6
            self.damage_dealt_this_attack = False
        elif mouse_buttons and mouse_buttons[2] and not self.is_attacking and self.defend_cooldown == 0:
            self.is_defending = True
            self.defend_cooldown = 30
            self.frame_idx = 0
            self.anim_time = 0
            self.state = "DEFEND"

    def update(self, platforms) -> None:
        if self.state == "DEATH":
            self.update_death_animation()
            return
        # COYOTE TIME
        if self.on_ground:
            self.coyote_time = self.coyote_time_max
        else:
            self.coyote_time = max(0, self.coyote_time - 1)
        # JUMP BUFFER
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        do_jump = False
        if self.jump_buffer > 0 and (self.coyote_time > 0 or self.jump_count < self.max_jump_count):
            do_jump = True
        if do_jump:
            self.vel_y = -self.jump_power
            self.jump_time = 0
            self.jump_count += 1
            self.on_ground = False
            self.jump_buffer = 0
            self.state = "JUMP"
        # Гравитация и переменная высота прыжка
        if self.vel_y < 0:
            self.jump_time += 1
            if not self.jump_pressed or self.jump_time > self.max_jump_time:
                self.vel_y += self.gravity * 1.8
            else:
                self.vel_y += self.gravity * 0.5
        else:
            self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        # Перемещение
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.midbottom = (round(self.pos_x), round(self.pos_y))
        self._update_hitbox()
        # Проверка на землю и платформы
        prev_on_ground = self.on_ground
        self.on_ground = False
        for platform in platforms:
            platform: pygame.sprite.Sprite
            if self.hitbox.colliderect(platform.rect):
                if self.vel_y > 0 and self.hitbox.bottom - self.vel_y <= platform.rect.top:
                    self.hitbox.bottom = platform.rect.top
                    self.pos_y = self.hitbox.bottom
                    self.vel_y = 0
                    self.on_ground = True
        self.rect.midbottom = self.hitbox.midbottom
        # Сброс прыжков при касании платформы
        if self.on_ground:
            self.jump_count = 0
            self.jump_time = 0
        # Кулдауны
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.defend_cooldown > 0:
            self.defend_cooldown -= 1
            self.state = "DEFEND"
        elif self.defend_cooldown == 0:
            self.is_defending = False
        # Анимация удара
        if self.is_attacking:
            frames = self.frames[self.current_attack]
            self.anim_time += self.attack_anim_speed
            if self.anim_time >= 1:
                self.anim_time = 0
                self.frame_idx += 1
                if self.frame_idx >= len(frames):
                    self.is_attacking = False
                    self.state = "IDLE"
                    self.frame_idx = 0
            old_midbottom = self.rect.midbottom
            self.image = frames[self.frame_idx % len(frames)]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom
            self._update_hitbox()
            if not self.is_attacking:
                self.damage_dealt_this_attack = False
            return
        # Обычная анимация
        # JUMP/FALL спрайты
        if not self.on_ground:
            if self.vel_y < 0 and "JUMP" in self.frames:
                self.state = "JUMP"
            elif self.vel_y > 0 and "FALL" in self.frames:
                self.state = "FALL"
        self.anim_time += self.anim_speed
        if self.anim_time >= 1:
            self.anim_time = 0
            frames = self.frames[self.state] if self.state in self.frames else self.frames["IDLE"]
            if self.frame_idx + 1 >= len(frames):
                self.frame_idx = 0
            else:
                self.frame_idx += 1
        old_midbottom = self.rect.midbottom
        frames = self.frames[self.state] if self.state in self.frames else self.frames["IDLE"]
        self.image = frames[self.frame_idx % len(frames)]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom
        self._update_hitbox()
        if not self.is_attacking:
            self.damage_dealt_this_attack = False

    def attack_enemies(self, enemies):
        if self.is_attacking:
            # Урон наносится только на 3-м кадре анимации удара и только один раз за атаку
            if self.frame_idx == 2 and not self.damage_dealt_this_attack:
                attack_rect = self.hitbox.copy()
                if self.facing_right:
                    attack_rect.x += 30
                else:
                    attack_rect.x -= 30
                attack_rect.width += 30
                for enemy in enemies:
                    if attack_rect.colliderect(enemy.hitbox) and not getattr(enemy, 'is_dead', False):
                        damage = max(1, enemy.max_hp // 4)
                        enemy.take_damage(damage)
                self.damage_dealt_this_attack = True

    def take_damage(self, amount):
        super().take_damage(amount)
        # Можно добавить отбрасывание или эффекты

    def draw(self, surface, debug=False, is_enemy=False):
        super().draw(surface, debug=debug, is_enemy=is_enemy)


class Enemy(BaseFighter):
    def __init__(self, x: int, y: int, hp: int = 100, speed: int = 2, sprite_type: str = "enemy"):
        super().__init__(x, y, sprite_type, ENEMY_SPRITE_FRAMES, hp)
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_range = 60
        self.target = None
        self.anim_speed = 0.22
        self.attack_anim_speed = 0.28
        self.anim_time = 0.5
        self.current_attack = "ATTACK 1"
        self.attack_timer = 6
        self.last_damage_timer = 0  # Ограничение урона по игроку
        self.damage_dealt_this_attack = False
        self.jump_cooldown = 0

    def update(self, platforms: pygame.sprite.Group, player: Optional[BaseFighter] = None) -> None:
        if self.state == "DEATH":
            self.update_death_animation()
            return
        # Рандомный прыжок
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if not self.is_attacking and self.on_ground and self.jump_cooldown == 0:
            if random.random() < 1/90:  # шанс прыжка примерно раз в 1.5 сек
                self.vel_y = -15  # сила прыжка
                self.on_ground = False
                self.jump_cooldown = 60
        if player is not None:
            dx = player.rect.centerx - self.rect.centerx
            if abs(dx) > self.attack_range:
                self.vel_x = self.speed if dx > 0 else -self.speed
                self.facing_right = dx > 0
                if self.on_ground:
                    self.state = "RUN"
            else:
                self.vel_x = 0
                if self.attack_cooldown == 0 and not self.is_attacking:
                    self.is_attacking = True
                    self.attack_cooldown = 80
                    self.frame_idx = 0
                    self.anim_time = 0
                    self.current_attack = random.choice(
                        ["ATTACK 1", "ATTACK 2"])
                    self.state = self.current_attack
                    self.attack_timer = 6
                    self.damage_dealt_this_attack = False
        # Гравитация
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        # Перемещение
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.midbottom = (round(self.pos_x), round(self.pos_y))
        self._update_hitbox()
        # Проверка на землю
        self.on_ground = False
        for platform in platforms:
            platform: pygame.sprite.Sprite
            if self.hitbox.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.hitbox.bottom = platform.rect.top
                    self.pos_y = self.hitbox.bottom
                    self.vel_y = 0
                    self.on_ground = True
        self.rect.midbottom = self.hitbox.midbottom
        # Кулдаун атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.last_damage_timer > 0:
            self.last_damage_timer -= 1
        # Анимация удара
        if self.is_attacking:
            frames = self.frames[self.current_attack] if self.current_attack in self.frames else self.frames["IDLE"]
            self.anim_time += self.attack_anim_speed
            if self.anim_time >= 1:
                self.anim_time = 0
                self.frame_idx += 1
                if self.frame_idx >= len(frames):
                    self.is_attacking = False
                    self.state = "IDLE"
                    self.frame_idx = 0
            old_midbottom = self.rect.midbottom
            self.image = frames[self.frame_idx % len(frames)]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom
            self._update_hitbox()
            # Урон на 3-м кадре
            if player and self.frame_idx == 2 and not self.damage_dealt_this_attack:
                attack_rect = self.hitbox.copy()
                if self.facing_right:
                    attack_rect.x += 30
                else:
                    attack_rect.x -= 30
                attack_rect.width += 30
                if attack_rect.colliderect(player.hitbox):
                    if self.last_damage_timer == 0:
                        player.take_damage(15)
                        self.last_damage_timer = 30
                self.damage_dealt_this_attack = True
            if not self.is_attacking:
                self.damage_dealt_this_attack = False
            return
        # Обычная анимация
        self.anim_time += self.anim_speed
        if self.anim_time >= 1:
            self.anim_time = 0
            frames = self.frames[self.state] if self.state in self.frames else self.frames["IDLE"]
            if self.frame_idx + 1 >= len(frames):
                self.frame_idx = 0
            else:
                self.frame_idx += 1
        old_midbottom = self.rect.midbottom
        frames = self.frames[self.state] if self.state in self.frames else self.frames["IDLE"]
        self.image = frames[self.frame_idx % len(frames)]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom
        self._update_hitbox()
        if not self.is_attacking:
            self.damage_dealt_this_attack = False

    def take_damage(self, amount):
        super().take_damage(amount)

    def draw(self, surface, debug=False, is_enemy=True):
        super().draw(surface, debug=debug, is_enemy=is_enemy)


class PlayerNeon(Player):
    def __init__(self, x: int, y: int, hp: int = 100):
        super().__init__(x, y, hp, sprite_type="knight_neon")

    def update(self, platforms) -> None:
        if self.state == "DEATH":
            self.update_death_animation()
            return
        super().update(platforms)

    def draw(self, surface, debug=False, is_enemy=False):
        super().draw(surface, debug=debug, is_enemy=is_enemy)


class EnemyNeon(Enemy):
    def __init__(self, x: int, y: int, hp: int = 100, speed: int = 2):
        super().__init__(x, y, hp, speed, sprite_type="enemy_neon")

    def update(self, platforms, player=None) -> None:
        if self.state == "DEATH":
            self.update_death_animation()
            return
        super().update(platforms, player)

    def draw(self, surface, debug=False, is_enemy=True):
        super().draw(surface, debug=debug, is_enemy=is_enemy)
