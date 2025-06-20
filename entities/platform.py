import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, hp: int = 1) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Прозрачный прямоугольник
        self.rect = self.image.get_rect(
            topleft=(x, y))  # Платформа по координатам
        self.hp = hp  # Здоровье платформы


class Heart(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        # Неоновое свечение (внешний контур)
        for r, alpha in [(18, 40), (15, 80), (12, 180)]:
            pygame.draw.ellipse(
                self.image, (0, 255, 255, alpha), (18-r, 18-r+4, 2*r, r+8))
            pygame.draw.circle(self.image, (0, 255, 255, alpha), (10, 18), r)
            pygame.draw.circle(self.image, (0, 255, 255, alpha), (26, 18), r)
        # Основная форма сердца
        pygame.draw.ellipse(self.image, (0, 255, 255), (6, 14, 24, 14))
        pygame.draw.circle(self.image, (0, 255, 255), (14, 20), 8)
        pygame.draw.circle(self.image, (0, 255, 255), (22, 20), 8)
        self.rect = self.image.get_rect(center=(x, y))  # Центрируем сердце
        self.heal_amount = 30  # Сколько HP восстанавливает

    def update(self):
        pass  # Здесь можно добавить анимацию


class BlueOrb(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Внешнее свечение
        for r, alpha in [(20, 30), (16, 60), (12, 120)]:
            pygame.draw.circle(self.image, (0, 200, 255, alpha), (20, 20), r)
        # Основной круг
        pygame.draw.circle(self.image, (0, 200, 255), (20, 20), 10)
        self.rect = self.image.get_rect(center=(x, y))  # Центрируем сферу
        self.is_full_heal = True  # Маркер для логики (полное восстановление)

    def update(self):
        pass  # Можно добавить анимацию
