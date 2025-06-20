from levels.level_base import BaseLevel
from levels.transition_screen import TransitionScreen
import pygame
from typing import Tuple



class SurfaceLevel(BaseLevel):
    def __init__(
        self,
        name: str,
        enemy_count: int = 5,
        enemy_type: str = 'medieval',
        floor_offset_from_bottom: int = 100,
        caption_color: Tuple[int, int, int] = (255, 255, 255),
        caption_font_path: str = "assets/fonts/alagard-12px-unicode.otf"
    ):
        super().__init__(
            background_path="assets/images/backgrounds/surface.png",
            enemy_count=enemy_count,
            enemy_type=enemy_type,
            level_name=name,
            floor_offset_from_bottom=floor_offset_from_bottom,
            caption_color=caption_color,
            caption_font_path=caption_font_path
        )


class TransitionLevel(BaseLevel):
    def __init__(
        self,
        background_path: str,
        enemy_count: int = 5,
        enemy_type: str = 'medieval'
    ):
        # нет надписи слева сверху
        super().__init__(
            background_path=background_path,
            enemy_count=enemy_count,
            enemy_type=enemy_type,
            level_name="",
            caption_color=(0, 0, 0),
            caption_font_path="assets/fonts/alagard-12px-unicode.otf"
        )

    def draw_caption(self, screen: pygame.Surface):
        pass  # Не рисуем надпись


class DestroyedGatewayLevel(BaseLevel):
    def __init__(
        self,
        enemy_count: int = 7,
        enemy_type: str = 'medieval',
        floor_offset_from_bottom: int = 100
    ):
        super().__init__(
            background_path="assets/images/backgrounds/destroyed_gateway.png",
            enemy_count=enemy_count,
            enemy_type=enemy_type,
            level_name="3: Разрушенный шлюз",
            floor_offset_from_bottom=floor_offset_from_bottom,
            caption_color=(255, 255, 255),
            caption_font_path="assets/fonts/alagard-12px-unicode.otf"
        )


class DataTunnelLevel(BaseLevel):
    def __init__(
        self,
        enemy_count: int = 8,
        enemy_type: str = 'medieval',
        floor_offset_from_bottom: int = 100
    ):
        super().__init__(
            background_path="assets/images/backgrounds/data_tunnel.png",
            enemy_count=enemy_count,
            enemy_type=enemy_type,
            level_name="5: Туннель данных",
            floor_offset_from_bottom=floor_offset_from_bottom,
            caption_color=(255, 255, 255),
            caption_font_path="assets/fonts/alagard-12px-unicode.otf"
        )


class ArenaLevel(BaseLevel):
    def __init__(
        self,
        enemy_count: int = 10,
        enemy_type: str = 'medieval',
        floor_offset_from_bottom: int = 100
    ):
        super().__init__(
            background_path="assets/images/backgrounds/arena.png",
            enemy_count=enemy_count,
            enemy_type=enemy_type,
            level_name="7: Арена",
            floor_offset_from_bottom=floor_offset_from_bottom,
            caption_color=(255, 255, 255),
            caption_font_path="assets/fonts/alagard-12px-unicode.otf"
        )


class BossLevel(BaseLevel):
    def __init__(
        self,
        enemy_count: int = 1,
        enemy_type: str = 'boss',
        floor_offset_from_bottom: int = 100
    ):
        super().__init__(
            background_path="assets/images/backgrounds/boss_fight.png",
            enemy_count=enemy_count,
            enemy_type=enemy_type,
            level_name="9: Босс",
            floor_offset_from_bottom=floor_offset_from_bottom,
            caption_color=(255, 255, 255),
            caption_font_path="assets/fonts/alagard-12px-unicode.otf"
        )


class BattleIntroTransition(TransitionScreen):
    def __init__(self):
        super().__init__(
            title="Битва начинается!",
            description=(
                "Наш герой-рыцарь вступает в бой с врагами.\n"
                "Победи их всех, чтобы пройти дальше!\n"
                "\nНажмите ENTER для начала игры."
            ),
            title_color=(180, 40, 40),
            desc_color=(255, 255, 255),
            bg_color=(30, 40, 70),
            title_font_path="assets/fonts/alagard-12px-unicode.otf",
            desc_font_path="assets/fonts/alagard-12px-unicode.otf"
        )


class SimpleTransition(TransitionScreen):
    def __init__(
        self,
        title: str,
        description: str = "",
        bg_color: Tuple[int, int, int] = (30, 40, 70)
    ):
        super().__init__(
            title=title,
            description=description,
            title_color=(180, 40, 40),
            desc_color=(255, 255, 255),
            bg_color=bg_color,
            title_font_path="assets/fonts/alagard-12px-unicode.otf",
            desc_font_path="assets/fonts/alagard-12px-unicode.otf"
        )


class MedievalTransition(SimpleTransition):
    def __init__(self):
        super().__init__(
            title="Уровень 1: Королевство",
            description="",
            bg_color=(80, 30, 30),  # Глубокий бордовый цвет
        )
        self.title_color = (255, 215, 0)  # Золотой цвет
        self.desc_color = (245, 245, 220)  # Светло-бежевый


class NeonTransition(SimpleTransition):
    def __init__(self, title: str, description: str = ""):
        super().__init__(
            title=title,
            description=description,
            bg_color=(10, 15, 40),  # Темно-синий фон
        )
        self.title_color = (0, 255, 255)  # Неоново-голубой
        self.desc_color = (180, 255, 255)  # Светлый неоновый


class EndTransition(SimpleTransition):
    def __init__(self):
        super().__init__(
            title="Уровень 10: Конец",
            description="",
            bg_color=(80, 30, 30),  # Глубокий бордовый цвет
        )
        self.title_color = (255, 215, 0)  # Золотой цвет
        self.desc_color = (245, 245, 220)  # Светло-бежевый
