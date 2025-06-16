from entities.platform import Platform
from levels.sector1_gateway import Sector1GatewayLevel
from levels.base_level import BaseLevel


def create_level(level_num):
    # Карта уровней
    level_map = {
        1: Sector1GatewayLevel,
        # Добавим другие уровни позже
        # 2: Sector2DataTunnelLevel,
        # 3: Sector3ArenaLevel,
        # etc.
    }

    # Создаем и возвращаем соответствующий уровень
    level_class = level_map.get(level_num, Sector1GatewayLevel)
    return level_class()
