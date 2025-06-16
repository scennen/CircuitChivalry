import pygame
import os
import random


class Enemy(pygame.sprite.Sprite):
    # Количество кадров в каждом спрайт-листе
    SPRITE_FRAMES = {
        "IDLE": 8,
        "RUN": 8,
        "WALK": 8,
        "ATTACK 1": 6,
        "ATTACK 2": 6,
        "ATTACK 3": 6,
        "HURT": 4,
        "DEATH": 6,
    }
    SCALE = 3  # Тот же масштаб, что и у игрока
    HITBOX_WIDTH = 32  # Такой же хитбокс, как у игрока
    HITBOX_HEIGHT = 48

    def __init__(self, x, y, hp=100, speed=2, sprite_type="enemy"):
        super().__init__()
        # Базовые параметры
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_attacking = False
        self.is_dead = False
        self.facing_right = True
        self.attack_range = 60
        self.attack_cooldown = 0
        self.attack_damage = 10
        self.gravity = 0.8
        self.jump_power = 15

        # Анимация
        self.state = "IDLE"
        self.frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.frame_offsets = {}

        # Загрузка спрайтов
        self.sprite_type = sprite_type  # "enemy", "enemy_neon" и т.д.
        self.frames = {}
        self.load_sprites()

        # Инициализация хитбоксов
        self.image = self.frames[self.state][self.frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (round(self.pos_x), round(self.pos_y))
        self.hitbox = pygame.Rect(0, 0, self.HITBOX_WIDTH, self.HITBOX_HEIGHT)
        self.attack_hitbox = pygame.Rect(0, 0, 60, 60)  # Область атаки
        self._update_hitboxes()

        self.damage_dealt_in_attack = False  # Флаг для контроля урона за анимацию

    def _update_hitboxes(self):
        # Обновление хитбоксов
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

        # Обновление зоны атаки
        attack_width = 60
        if self.facing_right:
            self.attack_hitbox.left = self.hitbox.right
        else:
            self.attack_hitbox.right = self.hitbox.left
        self.attack_hitbox.centery = self.hitbox.centery

    def load_sprites(self):
        # Use absolute path like Player class
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))

        base_path = os.path.join(
            base_dir, "assets", "images", "sprites", self.sprite_type)

        for state in self.SPRITE_FRAMES.keys():
            try:
                file_name = f"{state}.png"
                if state.startswith("ATTACK"):
                    file_name = f"ATTACK {state[-1]}.png"

                sheet = pygame.image.load(os.path.join(
                    base_path, file_name)).convert_alpha()
                num_frames = self.SPRITE_FRAMES[state]

                # Нарезка спрайтов
                frame_width = sheet.get_width() // num_frames
                frame_height = sheet.get_height()

                raw_frames = []
                for i in range(num_frames):
                    frame = sheet.subsurface(pygame.Rect(
                        i * frame_width, 0, frame_width, frame_height))
                    # Обрезка по альфа-каналу
                    bbox = frame.get_bounding_rect(min_alpha=1)
                    cropped = frame.subsurface(bbox)
                    raw_frames.append(cropped)

                # Приведение к одному размеру
                max_w = max(f.get_width() for f in raw_frames)
                max_h = max(f.get_height() for f in raw_frames)

                state_frames = []
                state_offsets = []

                for f in raw_frames:
                    surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
                    # Центрирование по туловищу
                    offset_x = (max_w - f.get_width()) // 2
                    offset_y = max_h - f.get_height()
                    surf.blit(f, (offset_x, offset_y))
                    # Масштабирование
                    scaled = pygame.transform.scale(
                        surf, (max_w * self.SCALE, max_h * self.SCALE))
                    state_frames.append(scaled)
                    state_offsets.append(
                        (offset_x * self.SCALE, offset_y * self.SCALE))

                self.frames[state] = state_frames
                self.frame_offsets[state] = state_offsets
            except Exception as e:
                print(
                    f"Error loading {state} sprites for {self.sprite_type}: {e}")
                # Создаем цветной прямоугольник если спрайт не загрузился
                self.frames[state] = [pygame.Surface(
                    (40 * self.SCALE, 80 * self.SCALE))]
                self.frames[state][0].fill((255, 0, 0))
                self.frame_offsets[state] = [(0, 0)]

    def update(self, player=None, platforms=None):
        if self.is_dead and self.frame >= len(self.frames["DEATH"]) - 1:
            self.kill()
            return

        # Обработка кулдауна атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # AI поведение
        if player and not self.is_dead and not self.is_attacking:
            dist_x = player.rect.centerx - self.rect.centerx
            dist_y = abs(player.rect.centery - self.rect.centery)

            # Поворот в сторону игрока
            self.facing_right = dist_x > 0

            # Атака если игрок близко
            if abs(dist_x) < self.attack_range and dist_y < 50 and self.attack_cooldown <= 0:
                self.attack()
            # Движение к игроку
            elif not self.is_attacking and dist_y < 100:  # Только если примерно на той же высоте
                if abs(dist_x) > self.attack_range:
                    self.vel_x = self.speed if dist_x > 0 else -self.speed
                    if self.on_ground:
                        self.state = "RUN"
                else:
                    self.vel_x = 0
                    if self.on_ground:
                        self.state = "IDLE"
            else:
                self.vel_x = 0
                if self.on_ground:
                    self.state = "IDLE"

        # Применение гравитации
        if not self.on_ground:
            self.vel_y = min(self.vel_y + self.gravity, 15)

        # Обновление позиции
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        # Обновление rect и хитбоксов
        self.rect.midbottom = (round(self.pos_x), round(self.pos_y))
        self._update_hitboxes()

        # Обработка коллизий с платформами
        self.on_ground = False
        if platforms:
            for platform in platforms:
                if self.hitbox.colliderect(platform.rect):
                    if self.vel_y > 0:  # Падаем на платформу
                        self.hitbox.bottom = platform.rect.top
                        self.rect.bottom = self.hitbox.bottom
                        self.pos_y = self.hitbox.bottom
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Прыжок в платформу сверху
                        self.hitbox.top = platform.rect.bottom
                        self.rect.bottom = self.hitbox.bottom
                        self.pos_y = self.hitbox.bottom
                        self.vel_y = 0
                    # Боковые столкновения
                    elif self.vel_x > 0:  # Движение вправо
                        self.hitbox.right = platform.rect.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos_x = self.rect.centerx
                        self.vel_x = 0
                    elif self.vel_x < 0:  # Движение влево
                        self.hitbox.left = platform.rect.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos_x = self.rect.centerx
                        self.vel_x = 0

        # Анимация
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            max_frames = len(self.frames[self.state])
            self.frame = (self.frame + 1) % max_frames

            # Завершение атаки
            if self.is_attacking and self.frame >= max_frames - 1:
                self.is_attacking = False
                self.state = "IDLE"
                self.frame = 0
                self.damage_dealt_in_attack = False  # Сбросить флаг после анимации

        # Обновление спрайта
        self.image = self.frames[self.state][self.frame]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def attack(self):
        if not self.is_attacking and not self.is_dead and self.on_ground:
            self.is_attacking = True
            self.attack_cooldown = 45
            self.state = f"ATTACK {random.randint(1, 3)}"
            self.frame = 0
            self.vel_x = 0
            self.damage_dealt_in_attack = False  # Сбросить флаг при начале атаки

    def take_damage(self, amount):
        if not self.is_dead:
            self.hp -= amount
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
                self.state = "DEATH"
                self.frame = 0
                self.animation_timer = 0
            else:
                self.state = "HURT"
                self.frame = 0
                self.animation_timer = 0

    def draw(self, surface):
        # Отрисовка спрайта
        surface.blit(self.image, self.rect)

        # Полоска здоровья (только если есть урон и враг жив)
        if self.hp < self.max_hp and not self.is_dead:
            bar_width = 40
            bar_height = 5
            hp_ratio = max(0, self.hp / self.max_hp)

            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 10

            # Серый фон
            pygame.draw.rect(surface, (70, 70, 70),
                             (bar_x, bar_y, bar_width, bar_height))
            # Красная полоска здоровья
            if hp_ratio > 0:
                fill_width = int(bar_width * hp_ratio)
                pygame.draw.rect(surface, (220, 40, 40),
                                 (bar_x, bar_y, fill_width, bar_height))


class Drone(Enemy):
    def __init__(self, x, y, speed=4):
        super().__init__(x, y, hp=1, speed=speed)
        self.image.fill((0, 255, 255))  # Неоновый цвет

    def update(self):
        # Дрон летает по горизонтали
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > 1080:
            self.speed = -self.speed


class ShadowCopy(Enemy):
    def __init__(self, x, y, player_hp):
        super().__init__(x, y, hp=player_hp, speed=3)
        self.image.fill((100, 0, 100))  # Фиолетовый

    def update(self, player_rect):
        # Преследует игрока
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed


class CoreGuardian(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((120, 120))
        self.image.fill((50, 50, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 20
        self.arms = [BossArm(x-80, y, "sword"), BossArm(x+80, y, "shield"),
                     BossArm(x-80, y+80, "axe"), BossArm(x+80, y+80, "gun")]
        self.core_open = False
        self.core_timer = 0

    def update(self):
        # Открытие ядра после уничтожения рук
        if all(arm.destroyed for arm in self.arms):
            self.core_open = True
            self.core_timer = 300  # Ядро открыто 5 секунд (если FPS=60)
        if self.core_open:
            self.core_timer -= 1
            if self.core_timer <= 0:
                self.core_open = False


class BossArm(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type, hp=5):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(center=(x, y))
        self.weapon_type = weapon_type
        self.destroyed = False
        self.hp = hp

    def update(self):
        # Можно добавить анимацию или атаку
        pass


class Ally(pygame.sprite.Sprite):
    def __init__(self, x, y, hp=3):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp

    def update(self):
        # Логика союзника (например, движение за игроком)
        pass
