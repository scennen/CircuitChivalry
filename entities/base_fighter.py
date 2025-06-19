import pygame
import os
from typing import Dict, List, Tuple, Optional, Any


class BaseFighter(pygame.sprite.Sprite):
    SCALE = 4  # Универсальный масштаб для всех рыцарей и врагов
    HITBOX_WIDTH = 32  # Ширина хитбокса
    HITBOX_HEIGHT = 48  # Высота хитбокса

    def __init__(self, x: int, y: int, sprite_type: str, sprite_frames: Dict[str, int], hp: int = 100):
        super().__init__()
        self.hp = hp  # Текущее здоровье
        self.max_hp = hp  # Максимальное здоровье
        self.pos_x = float(x)  # Позиция по X (float для плавности)
        self.pos_y = float(y)  # Позиция по Y
        self.sprite_type = sprite_type  # Тип спрайта (папка)
        # Словарь с количеством кадров для каждого состояния
        self.SPRITE_FRAMES = sprite_frames
        self.frames: Dict[str, List[pygame.Surface]] = {}  # Кадры анимаций
        # Смещения для центрирования
        self.frame_offsets: Dict[str, List[Tuple[int, int]]] = {}
        self.state = "IDLE"  # Начальное состояние
        self.frame_idx = 0  # Индекс текущего кадра
        self.load_sprites()  # Загружаем спрайты
        # Текущий кадр
        self.image: pygame.Surface = self.frames[self.state][self.frame_idx]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.centerx = round(self.pos_x)
        self.rect.bottom = round(self.pos_y)
        self.hitbox: pygame.Rect = pygame.Rect(
            0, 0, self.HITBOX_WIDTH, self.HITBOX_HEIGHT)  # Хитбокс для коллизий
        self.is_dead = False  # Флаг смерти
        self._update_hitbox()

    def load_sprites(self) -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(
            base_dir, "assets", "images", "sprites", self.sprite_type)
        for state, num_frames in self.SPRITE_FRAMES.items():
            file_name = f"{state}.png"
            if state.startswith("ATTACK"):  # Для атак особое имя файла
                file_name = f"ATTACK {state[-1]}.png"
            sheet_path = os.path.join(base_path, file_name)
            if not os.path.exists(sheet_path):
                continue  # Если файла нет, пропускаем
            sheet = pygame.image.load(sheet_path).convert_alpha()
            frame_width = sheet.get_width() // num_frames
            frame_height = sheet.get_height()
            raw_frames: List[pygame.Surface] = []
            for i in range(num_frames):
                frame = sheet.subsurface(pygame.Rect(
                    i * frame_width, 0, frame_width, frame_height))
                bbox = frame.get_bounding_rect(min_alpha=1)
                cropped = frame.subsurface(bbox)
                raw_frames.append(cropped)
            max_w = max(f.get_width() for f in raw_frames)
            max_h = max(f.get_height() for f in raw_frames)
            state_frames: List[pygame.Surface] = []
            state_offsets: List[Tuple[int, int]] = []
            for f in raw_frames:
                surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
                offset_x = (max_w - f.get_width()) // 2
                offset_y = max_h - f.get_height()
                surf.blit(f, (offset_x, offset_y))
                scaled = pygame.transform.scale(
                    surf, (max_w * self.SCALE, max_h * self.SCALE))
                state_frames.append(scaled)
                state_offsets.append(
                    (offset_x * self.SCALE, offset_y * self.SCALE))
            self.frames[state] = state_frames
            self.frame_offsets[state] = state_offsets
        # Проверка наличия IDLE
        if "IDLE" not in self.frames:
            raise RuntimeError(
                f"Не найден спрайт IDLE для {self.sprite_type}!")

    def _update_hitbox(self) -> None:
        self.hitbox.centerx = self.rect.centerx  # Центрируем хитбокс по X
        self.hitbox.bottom = self.rect.bottom  # Нижняя граница совпадает с rect

    def set_floor_y(self, floor_y: int) -> None:
        self.pos_y = float(floor_y)
        self.rect.bottom = round(self.pos_y)
        self._update_hitbox()

    def handle_input(self, keys: Any, mouse_buttons: Optional[Any] = None) -> None:
        pass  # Здесь реализуется управление в наследниках

    def take_damage(self, amount):
        self.hp -= amount  # Уменьшаем здоровье
        if self.hp <= 0:
            self.hp = 0
            self.state = "DEATH"  # Состояние смерти
            self.is_dead = True
        else:
            self.state = "HURT"  # Состояние получения урона
            self.is_dead = False

    def update_death_animation(self):
        if self.state == "DEATH" and "DEATH" in self.frames:
            if self.frame_idx < len(self.frames["DEATH"]) - 1:
                self.frame_idx += 1
                self.image = self.frames["DEATH"][self.frame_idx]
            # После окончания анимации можно скрыть или удалить объект

    def draw(self, surface: pygame.Surface, debug: bool = False, is_enemy: bool = False) -> None:
        surface.blit(self.image, self.rect)  # Рисуем спрайт
        # Полоска здоровья
        bar_width = 40
        bar_height = 6
        hp_ratio = max(0, min(1, self.hp / self.max_hp))
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - bar_height - 4
        pygame.draw.rect(surface, (70, 70, 70),
                         (bar_x, bar_y, bar_width, bar_height))
        if hp_ratio > 0:
            fill_width = int(bar_width * hp_ratio)
            color = (200, 30, 30) if is_enemy else (0, 110, 158)
            pygame.draw.rect(surface, color,
                             (bar_x, bar_y, fill_width, bar_height))
        if debug:
            # Зеленый прямоугольник для отладки
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)
