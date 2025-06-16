import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, hp: int = 1) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp
