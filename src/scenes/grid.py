import pygame
from ..utils.constants import (
    WIDTH, HEIGHT, FONT_SIZE_TEXT, FONT_SIZE_BUTTON,
    FONT_COLOR, BG_COLOR, NEON_BLUE_SILVER, GRAPHITE
)


def grid_scene(screen, font_text, font_button, clock):
    grid_text = [
        "Ты хватаешь меч — и всё замирает. Звуки боя глохнут, земля превращается в цифровую сетку.",
        "Вокруг — световая буря из синих и фиолетовых пикселей. Ты в The Grid!",
        "Твои доспехи покрыты неоновыми полосами, меч светится цифровыми символами."
    ]
    grid_choices = [
        ("Осмотреться", 3),
        ("Двигаться вперёд", 4)
    ]
    selected = 0
    running = True

    while running:
        screen.fill(BG_COLOR)
        y = 60
        for line in grid_text:
            surf = font_text.render(line, True, FONT_COLOR)
            screen.blit(surf, (60, y))
            y += FONT_SIZE_TEXT + 8

        y = HEIGHT - 120
        for idx, (text, _) in enumerate(grid_choices):
            color = NEON_BLUE_SILVER if idx == selected else GRAPHITE
            surf = font_button.render(f"> {text}", True, color)
            screen.blit(surf, (80, y))
            y += FONT_SIZE_BUTTON + 12

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(grid_choices)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(grid_choices)
                elif event.key == pygame.K_RETURN:
                    _, next_scene = grid_choices[selected]
                    return next_scene

        clock.tick(60)
