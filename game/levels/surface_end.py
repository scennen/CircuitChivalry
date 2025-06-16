from .base_level import BaseLevel


class SurfaceEndLevel(BaseLevel):
    def __init__(self):
        super().__init__("Surface End")

    def start(self):
        # Финал, возвращение на поле битвы
        pass
