from .base_level import BaseLevel


class TransitionLevel(BaseLevel):
    def __init__(self, name="Transition"):
        super().__init__(name)

    def start(self):
        # Общая логика переходного уровня
        pass
