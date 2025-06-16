class BaseLevel:
    def __init__(self, name):
        self.name = name

    def start(self):
        pass  # Запуск уровня

    def update(self):
        pass  # Логика обновления уровня

    def end(self):
        pass  # Завершение уровня
