import pygame
from ..utils.constants import (
    WIDTH, HEIGHT, FONT_SIZE_TITLE, FONT_SIZE_BUTTON,
    FONT_COLOR, BG_COLOR, NEON_BLUE_SILVER, GRAPHITE
)


def main_menu(screen, font_title, font_button, clock):
    menu_choices = ["Начать игру", "Выход"]
    selected = 0
    running = True

    while running:
        screen.fill(BG_COLOR)
        title = font_title.render("CIRCUIT CHIVALRY", True, NEON_BLUE_SILVER)
        subtitle = font_title.render("THE GRID", True, NEON_BLUE_SILVER)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 170))

        y = 320
        for i, text in enumerate(menu_choices):
            color = NEON_BLUE_SILVER if i == selected else GRAPHITE
            surf = font_button.render(text, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += FONT_SIZE_BUTTON + 24

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_choices)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_choices)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return True
                    elif selected == 1:
                        pygame.quit()
                        return False

        clock.tick(60)
