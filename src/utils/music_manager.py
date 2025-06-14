import pygame
import os


class MusicManager:
    def __init__(self):
        self.music_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))), "assets", "music")
        self.current_track = None
        self.volume = 0.5

        # Загрузка всех треков
        self.tracks = {
            "main_menu": os.path.join(self.music_path, "armory.mp3"),
            "battle": os.path.join(self.music_path, "outlands.mp3"),
            "sector1": os.path.join(self.music_path, "disc_wars.mp3"),
            "sector2": os.path.join(self.music_path, "castor.mp3"),
            "sector3": os.path.join(self.music_path, "derezzed.mp3"),
            "boss": os.path.join(self.music_path, "end_of_line.mp3")
        }

        # Инициализация микшера
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

    def play(self, track_name: str, loop: int = -1) -> None:
        """
        Воспроизводит указанный трек
        :param track_name: Название трека из словаря tracks
        :param loop: Количество повторений (-1 для бесконечного цикла)
        """
        if track_name in self.tracks and self.current_track != track_name:
            pygame.mixer.music.load(self.tracks[track_name])
            pygame.mixer.music.play(loop)
            self.current_track = track_name

    def stop(self) -> None:
        """Останавливает воспроизведение музыки"""
        pygame.mixer.music.stop()
        self.current_track = None

    def pause(self) -> None:
        """Ставит музыку на паузу"""
        pygame.mixer.music.pause()

    def unpause(self) -> None:
        """Снимает музыку с паузы"""
        pygame.mixer.music.unpause()

    def set_volume(self, volume: float) -> None:
        """
        Устанавливает громкость музыки
        :param volume: Громкость от 0.0 до 1.0
        """
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
