import pygame
from levels.base_level import BaseLevel
from entities.entities import Enemy
from entities.platform import Platform


class Sector1GatewayLevel(BaseLevel):
    def __init__(self):
        super().__init__("Sector 1: Gateway")
        self.enemies = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # Основная платформа (пол)
        floor = Platform(0, 500, 1200, 40)
        self.platforms.add(floor)

        # Платформы для вертикального геймплея
        platform1 = Platform(200, 350, 200, 20)
        platform2 = Platform(500, 250, 200, 20)
        platform3 = Platform(800, 400, 200, 20)
        self.platforms.add(platform1, platform2, platform3)

        # Точки появления врагов
        self.enemy_spawn_points = [
            (300, 450),  # На земле
            (500, 200),  # На верхней платформе
            (800, 350)   # На правой платформе
        ]

    def start(self):
        # Создаем врагов
        for pos in self.enemy_spawn_points:
            enemy = Enemy(pos[0], pos[1], hp=100, speed=2)
            self.enemies.add(enemy)

    def update(self):
        if self.player:
            # Обновляем врагов
            enemy_list = list(self.enemies)
            for i, enemy in enumerate(enemy_list):
                # Передаем игрока и платформы в update
                enemy.update(self.player, self.platforms)

                # --- Раздвигаем врагов, если они пересекаются ---
                for j, other in enumerate(enemy_list):
                    if i != j and enemy.hitbox.colliderect(other.hitbox):
                        dx = enemy.rect.centerx - other.rect.centerx
                        if dx == 0:
                            dx = 1  # чтобы не делить на 0
                        push = 2  # сила раздвигания
                        enemy.pos_x += push * (dx / abs(dx))
                        enemy.rect.centerx = round(enemy.pos_x)
                        enemy._update_hitboxes()

                # Проверяем попадание атаки игрока по врагу
                if (self.player.is_attacking and
                        enemy.hitbox.colliderect(self.player.hitbox)):
                    enemy.take_damage(20)  # Урон от атаки игрока

                # Проверяем попадание атаки врага по игроку (только 1 раз за анимацию)
                if (enemy.is_attacking and
                        self.player.hitbox.colliderect(enemy.hitbox) and
                        not enemy.damage_dealt_in_attack):
                    self.player.hp -= enemy.attack_damage
                    enemy.damage_dealt_in_attack = True

            # Обновление игрока с передачей платформ
            self.player.update(self.platforms)

    def draw(self, screen):
        # Отрисовка платформ
        for platform in self.platforms:
            pygame.draw.rect(screen, (128, 128, 128), platform.rect)

        # Отрисовка врагов
        for enemy in self.enemies:
            enemy.draw(screen)
