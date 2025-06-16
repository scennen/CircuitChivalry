import pygame


class BaseLevel:
    def __init__(self, name):
        self.name = name
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

    def set_player(self, player):
        self.player = player

    def start(self):
        pass  # Переопределяется в конкретных уровнях

    def update(self):
        pass  # Переопределяется в конкретных уровнях

    def draw(self, screen):
        # Базовая отрисовка уровня
        # Переопределяется в конкретных уровнях для добавления специфических элементов
        for platform in self.platforms:
            pygame.draw.rect(screen, (128, 128, 128), platform.rect)

        for enemy in self.enemies:
            enemy.draw(screen)

    def end(self):
        pass  # Переопределяется в конкретных уровнях
