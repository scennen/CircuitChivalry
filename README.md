# Платформер: запуск игры

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск игры

```bash
python main.py
```

## Управление

- Стрелки влево/вправо или A/D — движение рыцаря
- / / ЛКМ - удар
- ENTER — переход на следующий экран/уровень на экранах перехода

## Примечания

- Все уровни и переходы можно менять в файле `main.py`.
- Для корректной работы убедитесь, что структура папок и файлов соответствует проекту.

## SOLID
S — Single Responsibility Principle
Platform — только платформа, не содержит логики врагов или игрока.
BaseFighter — только логика бойца, не занимается, например, генерацией уровней.

O — Open/Closed Principle
BaseFighter открыт для расширения (через наследование), но закрыт для модификации.
Player/Enemy/PlayerNeon/EnemyNeon расширяют поведение, не меняя базовый класс.

L — Liskov Substitution Principle
PlayerNeon может быть использован вместо Player (например, в get_player_for_level).
EnemyNeon может быть использован вместо Enemy.

I — Interface Segregation Principle
draw и update реализованы отдельно, можно использовать только нужные методы.
handle_input реализован только там, где нужен (например, у игрока, но не у врага).

D — Dependency Inversion Principle
BaseLevel не зависит от конкретных классов врагов, а использует абстракции (через параметры enemy_type).
main.py использует абстракции уровней и игроков, не завязан на конкретные реализации.

## ООП
Инкапсуляция — все параметры и методы, относящиеся к бойцу, инкапсулированы в классе BaseFighter и его наследниках.

Наследование — Player, Enemy, PlayerNeon, EnemyNeon наследуют BaseFighter, переопределяя или расширяя поведение.

Полиморфизм — методы draw, update, take_damage могут быть вызваны для любого объекта-наследника BaseFighter, и поведение будет корректным.

Абстракция — BaseFighter задаёт абстрактную сущность бойца, не реализуя конкретную логику управления (handle_input реализуется только в Player).
